from typing import List, Any

from scipy.signal import butter, lfilter
import json, sys, numpy as np, matplotlib.pyplot as plt


# Source butter_bandpass http://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html


def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y



def main():


    # get data as an array from read_in()
    datainput = json.loads(sys.stdin.read())
    cmdIdx = datainput['cmdIdx']
    volts = datainput['volts']

    # create a numpy array
    data = np.array(volts)
    #
    # detect P300
    cmd = detectP300(data, cmdIdx)

    # send docommand back to node
    print(cmd)



def detectP300(data, cmdIdx):

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 2
    threshold = 5
    slotSize = 120
    commands = ['playpause', 'next', 'prev', 'volup', 'voldown']
    cmdCount = len(cmdIdx)
    cycles = len(cmdIdx[0])
    useAvg = False # Calc avg or sum

    # ## FILTER DATA
    # double data before filter and cut of first half afterwards
    doubledata = np.concatenate([data, data])
    doubledataFilterd = filterData(doubledata, lowcut, highcut, fs, order)
    dataBP = doubledataFilterd[int(len(doubledataFilterd)/2):]

    # ## SPLIT VOLTS DATA IN COMMAND EPOCHES
     ##  collect volt for each cmd in dataP300[CMD][CYCLE][VOLTS]
    dataP300 =[[],[],[],[],[]]
    for i in range(cmdCount):
        for j in range(cycles):
            dataP300[i].append(dataBP[cmdIdx[i][j]:(cmdIdx[i][j]+slotSize)])

    # AVERAGE CYCLES
    # calculate avg data for each cmd
    if(useAvg):
        dataP300Avg =[[],[],[],[],[]]
        for i in range(cmdCount):
            dataP300Avg[i] =  np.average(dataP300[i], axis=0)

            for j in range(cycles):
                plt.figure(10+i)
                plt.title(' P300 Avg Cycles Cmd: %s ' % (commands[i]))
                plt.plot(dataP300[i][j] * 1000000, color='b')

            plt.figure(10 + i)
            plt.plot(dataP300Avg[i] * 1000000, color='r')
        plt.show()
        return getCmdMaxAmplitude(dataP300Avg, cmdCount, threshold)
    else:
        # SUM CYCLES
        ## calc sum for each cmd over cycles
        dataP300Sum =[[],[],[],[],[]]
        for i in range(cmdCount):
            dataP300Sum[i] =  dataP300[i][0]
            for j in range(cycles):
                plt.figure(20+i)
                plt.title(' P300 Sum Cycles Cmd: %s ' % (commands[i]))
                plt.plot(dataP300[i][j] * 1000000, color='b')
                dataP300Sum[i] = np.sum( np.array([dataP300Sum[i], dataP300[i][j]]), axis=0 )
            plt.figure(20 + i)
            plt.plot(dataP300Sum[i] * 1000000, color='r')
        plt.show()
        return getCmdMaxAmplitude(dataP300Sum,cmdCount,threshold)


def getCmdMaxAmplitude(dataP300, cmdCount,threshold):
    # ONLY ANALYSE DATA BETWEEN 200ms(50) and 400ms(100) AFTER CMD
    for i in range(cmdCount):
        dataP300[i] = dataP300[i][50:100]

    ## CALCULATE AMPLITUDE
    diff = []
    for i in range(cmdCount):
        diff.append(np.max(dataP300[i]) - np.min(dataP300[i]))
    # get index of max diff
    maxdiff = np.max(diff)
    if (not np.isnan(float(maxdiff))):
        idx = diff.index(maxdiff)
        max = np.max(dataP300[idx])
        mean = np.mean(dataP300[idx])
        if (max>mean*threshold):
            return idx
    return "nop"

def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

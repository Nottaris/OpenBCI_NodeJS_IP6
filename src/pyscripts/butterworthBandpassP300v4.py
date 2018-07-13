from typing import List, Any

from scipy.signal import butter, lfilter
import json, sys, numpy as np


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
    # data = np.array(volts)
    print(cmdIdx)
    print(volts)
    #
    # detect P300
    cmd = detectP300(volts, cmdIdx)

    # send docommand back to node
    print(cmd)



def detectP300(data, cmdIdx):

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 4
    threshold = 10
    slotSize = 120
    cmdCount = len(cmdIdx)
    cycles = len(cmdIdx[0])
    print("cmdCount "+str(cmdCount))
    print("cycles "+str(cycles))
    print(cmdIdx[0][0])
     ##  collect volt for each cmd
    dataP300 =[[],[],[],[],[]]
    for i in range(cmdCount):
        for j in range(cycles):
            # print(data[cmdIdx[i][j]:cmdIdx[i][j]+120])
            dataP300[i].push(data[cmdIdx[i][j]:(cmdIdx[i][j]+120)])
            print(str(i)+" j:"+str(cmdIdx[i][j])+" "+str(print(dataP300[i][1:10])))

    # ## FILTER DATA
    # # double data before filter and cut of first half afterwards
    # doubledata = np.concatenate([data, data])
    # doubledataFilterd = filterData(doubledata, lowcut, highcut, fs, order)
    # dataBP = doubledataFilterd[int(len(doubledataFilterd)/2):]
    #
    # ## SPLIT DATA IN COMMAND EPOCHES
    # dataP300 = np.array_split(dataBP, cmdCount)
    #
    # ## SPLIT DATA IN CYCLES
    # #for i in range(cmdCount):
    # #    dataP300[i] = np.array_split(dataP300[i], cycleCount)
    #
    # # AVERAGE 5 CYCLES   or Sum ???
    # for i in range(cmdCount):
    #     dataP300[i] = np.average(dataP300[i], axis=0)
    #     #dataP300[i] = np.sum(dataP300[i], axis=0)
    #
    # # ONLY ANALYSE DATA BETWEEN 320ms(70) and 450ms(111) AFTER CMD
    # for i in range(cmdCount):
    #     dataP300[i] = dataP300[i][70:111]
    #
    # ## CALCULATE AMPLITUDE
    # diff = []
    # for i in range(cmdCount):
    #     diff.append(np.max(dataP300[i]) - np.min(dataP300[i]))
    # # get index of max diff
    # maxdiff = np.max(diff)
    # if (not np.isnan(float(maxdiff))):
    #     idx = diff.index(maxdiff)
    #     max = np.max(dataP300[idx])
    #     mean = np.mean(dataP300[idx])
    #     if (max>mean*threshold):
    #         return commands[idx]
    return "nop"


def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

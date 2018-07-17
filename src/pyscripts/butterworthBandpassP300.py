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
    baseline = datainput['baseline']

    # create a numpy array
    data = np.array(volts)
    baseline = np.array(baseline)

    ## active channels
    channels = [0, 1, 2]  # 0-7 channels

    averageChannels = True
    cmdResult = []

    if (averageChannels):
        # # Split channel Data
        dataChannel3 = []
        dataBaseline3 = []
        for channel in range(len(channels)):
            dataChannel = []
            dataBaseline = []
            # save volts for each channel
            for i in range(len(data)):
                dataChannel.append(data[i][channel])
            # save baseline for each channel
            for i in range(len(baseline)):
                dataBaseline.append(baseline[i][channel])
            dataChannel3.append(dataChannel)
            dataBaseline3.append(dataBaseline)
        # average arrays
        avgDataChannel = np.average(dataChannel3, axis=0)
        avgDataBaseline = np.average(dataBaseline3, axis=0)
        # detect P300 for averaged channels
        cmd = detectP300(avgDataChannel, avgDataBaseline, cmdIdx, 'all averaged')
        cmdResult.append(cmd)
        print("Result idx: " + str(cmdResult[0]))
        # Return cmd (can only be index 0 and will be "nop" if nothing found)
        return cmdResult[0]
    else:
        # # Split channel Data
        for channel in range(len(channels)):
            dataChannel = []
            dataBaseline = []
            # save volts for each channel
            for i in range(len(data)):
                dataChannel.append(data[i][channel])
            # save baseline for each channel
            for i in range(len(baseline)):
                dataBaseline.append(baseline[i][channel])
            # detect P300 for each channel
            cmd = detectP300(dataChannel, dataBaseline, cmdIdx, channel)
            cmdResult.append(cmd)

        print(cmdResult)
        # Return most common cmd
        if (cmdResult[0] == cmdResult[1] or cmdResult[0] == cmdResult[2]):
            print(cmdResult[0])
        elif (cmdResult[1] == cmdResult[2]):
            print(cmdResult[1])
        else:
            print("nop")


def detectP300(data, baseline, cmdIdx, channel):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 30.0
    order = 2
    threshold = 1.5
    slotSize = 120
    commands = ['playpause', 'next', 'prev', 'volup', 'voldown']
    cmdCount = len(cmdIdx)
    cycles = len(cmdIdx[0])
    useAvg = True  # True Calc avg, False Calc sum

    # ## FILTER DATA
    dataWithBaseline = np.concatenate([baseline, data])
    dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
    dataBP = dataFilterd[len(baseline):]

    # Plot filterd data
    plt.figure(1)
    plt.title("filterd data")
    plt.plot(dataBP * 1000000, color='r')

    # ## SPLIT VOLTS DATA IN COMMAND EPOCHES
    ##  collect volt for each cmd in dataP300[CMD][CYCLE][VOLTS]
    dataP300 = [[], [], [], [], []]
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            dataP300[cmd].append(dataBP[cmdIdx[cmd][cycle]:(cmdIdx[cmd][cycle] + slotSize)])

    ## SUBTRACT BASELINE MEAN ( equally ajust height )
    dataP300Baseline = [[], [], [], [], []]
    for i in range(cmdCount):
        for j in range(cycles):
            mean = np.mean(dataP300[i][j])
            dataP300Baseline[i].append(dataP300[i][j] - mean)
    # Overwrite dataP300 array
    dataP300 = dataP300Baseline

    # AVERAGE CYCLES
    # calculate avg data for each cmd
    if (useAvg):
        dataP300Avg = [[], [], [], [], []]
        for i in range(cmdCount):
            dataP300Avg[i] = np.average(dataP300[i], axis=0)

            # for j in range(cycles):
            #     plt.figure(10+i)
            #     plt.title(' P300 Avg Cycles Cmd: %s ' % (commands[i], channel))
            #     plt.plot(dataP300[i][j] * 1000000, color='b')

            plt.figure(10 + i)
            plt.title(' P300 %s Avg Cycles Cmd: %s ' % (channel, commands[i]))
            plt.plot(dataP300Avg[i] * 1000000, color='r')
        # plt.show()
        return getCmdMaxAmplitude(dataP300Avg, cmdCount, threshold)
    else:
        # SUM CYCLES
        ## calc sum for each cmd over cycles
        dataP300Sum = [[], [], [], [], []]
        for i in range(cmdCount):
            dataP300Sum[i] = dataP300[i][0]
            for j in range(cycles):
                plt.figure(20 + i)
                plt.title(' P300 Sum Cycles Cmd: %s ' % (commands[i]))
                plt.plot(dataP300[i][j] * 1000000, color='b')
                dataP300Sum[i] = np.sum(np.array([dataP300Sum[i], dataP300[i][j]]), axis=0)
            plt.figure(20 + i)
            plt.plot(dataP300Sum[i] * 1000000, color='r')
        # plt.show()
        return getCmdMaxAmplitude(dataP300Sum, cmdCount, threshold)


def getCmdMaxAmplitude(dataP300, cmdCount, threshold):
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
        if (max > mean * threshold):
            return idx
    return "nop"


def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

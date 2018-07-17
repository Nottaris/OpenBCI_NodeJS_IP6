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
    with open('../../../data/p300/ex4_cycles5/1531816738843_2_baseline.json') as f:
        baseline = json.load(f)
    with open('../../../data/p300/ex4_cycles5/1531816738826_2_volts.json') as f:
        volts = json.load(f)
    with open('../../../data/p300/ex4_cycles5/1531816738849_2_cmdIdx.json') as f:
        cmdIdx = json.load(f)

    # create a numpy array
    data = np.array(volts)
    baseline = np.array(baseline)
    # # cmd = detectP300(data, cmdIdx)

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
    highcut = 15.0
    order = 4
    threshold = 1.5
    slotSize = 120
    commands = ['playpause', 'next', 'prev', 'volup', 'voldown']
    cmdCount = len(cmdIdx)
    cycles = len(cmdIdx[0])
    baselineLength = len(baseline)
    useAvg = False  # True Calc avg, False Calc sum

    # ## FILTER DATA
    # double data before filter and cut of first half afterwards
    # doubledata = np.concatenate([data, data])
    # doubledataFilterd = filterData(doubledata, lowcut, highcut, fs, order)
    # dataBP = doubledataFilterd[int(len(doubledataFilterd)/2):]

    dataWithBaseline = np.concatenate([baseline, data])
    dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
    dataBP = dataFilterd[len(baseline):]
    baselineBP = dataFilterd[:len(baseline)]
    # Plot filterd data
    plt.figure(1)
    plt.title("filterd data - Channel " + str(channel))
    plt.plot(dataBP, color='r')

    print(data)
    plt.figure(2)
    plt.title("Raw data - Channel " + str(channel))
    plt.plot(data, color='r')

    # ## SPLIT VOLTS DATA IN COMMAND EPOCHES
    ##  collect volt for each cmd in dataP300[CMD][CYCLE][VOLTS]
    dataP300 = [[], [], [], [], []]
    dataBaseline = [[], [], [], [], []]
    print(baselineLength)
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            dataP300[cmd].append(dataBP[cmdIdx[cmd][cycle]:(cmdIdx[cmd][cycle] + slotSize)])
            dataBaseline[cmd].append(dataFilterd[cmdIdx[cmd][cycle] + baselineLength - slotSize + 40:(
                        cmdIdx[cmd][cycle] + baselineLength + 40)])

    ## SUBTRACT BASELINE FROM SLOT BEFORE
    # dataP300Baseline = [[], [], [], [], []]
    # for i in range(cmdCount):
    #     for j in range(cycles):
    #         dataP300Baseline[i].append(dataP300[i][j] - dataBaseline[i][j])
    # # Overwrite dataP300 array
    # dataP300 = dataP300Baseline

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

            for j in range(cycles):
                plt.figure(10 + i)
                plt.title(' P300 %d Avg Cycles Cmd: %s ' % (channel, commands[i]))
                plt.plot(dataP300[i][j] * 1000000, color='b')

            plt.figure(10 + i)
            plt.title(' P300 %d Avg Cycles Cmd: %s ' % (channel, commands[i]))
            plt.plot(dataP300Avg[i] * 1000000, color='r')
        plt.show()
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
                axes = plt.gca()
                axes.set_ylim([-50, 50])
                dataP300Sum[i] = np.sum(np.array([dataP300Sum[i], dataP300[i][j]]), axis=0)
            plt.figure(20 + i)
            axes = plt.gca()
            axes.set_ylim([-50, 50])
            plt.plot(dataP300Sum[i] * 1000000, color='r')
        plt.show()
        return getCmdMaxAmplitude(dataP300Sum, cmdCount, threshold)


def getCmdMaxAmplitude(dataP300, cmdCount, threshold):
    # ONLY ANALYSE DATA BETWEEN 200ms(50) and 400ms(100) AFTER CMD
    for i in range(cmdCount):
        dataP300[i] = dataP300[i][20:80]

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

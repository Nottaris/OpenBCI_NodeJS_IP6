from scipy import sparse
from scipy._lib.six import xrange
from scipy.signal import butter, lfilter
from scipy.sparse.linalg import spsolve
from scipy.stats import norm
from tempfile import TemporaryFile
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
    channel = 0  # channel 0-7

    # load json
    with open('../../test/data/p300_job_06-07-18/data-2018-7-6-14-35-01.json') as f:
        dataJson = json.load(f)
    # Get channel data
    data1 = getChannelData(dataJson, 0)
    data2 = getChannelData(dataJson, 3)
    data3 = getChannelData(dataJson, 5)
    # #VolDown
    # cmdRowFocus=[4561,5124,5687,6250,6813,7376,7937,8502,9065]
    # #prev
    # cmdRowNoFocus=[4786,5349,5912,6475,7038,7602,8165,8728,9291]
    # detectP300MultiChannels(data, data3,data5, cmdRowFocus, cmdRowNoFocus)

    # commands data/data-2018-7-6-14-35-01.json
    # command order: next,voldown,playpause,prev,volup
    # 1 cycles focus onvoldown
    cycle = 1
    focus = 1
    focusCmd = "voldown"
    cmdRow = [4459, 4561, 4674, 4786, 4899]
    # timestamps: [1530880525942,1530880526352,1530880526806,1530880527253,1530880527703,1530880528152]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 2 cycles focus onvoldown
    cycle = 2
    focus = 1
    focusCmd = "voldown"
    cmdRow = [5012, 5124, 5237, 5349, 5462]
    # timestamps: [1530880528602,1530880529052,1530880529503,1530880529954,1530880530403,1530880530854]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 3 cycles focus onvoldown
    cycle = 3
    focus = 1
    focusCmd = "voldown"
    cmdRow = [5575, 5687, 5800, 5912, 6025]
    # timestamps: [1530880531303,1530880531752,1530880532202,1530880532653,1530880533103,1530880533553]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 4 cycles focus onvoldown
    cycle = 4
    focus = 1
    focusCmd = "voldown"
    cmdRow = [6138, 6250, 6363, 6475, 6588]
    # timestamps: [1530880534004,1530880534454,1530880534904,1530880535352,1530880535811,1530880536252]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 5 cycles focus onvoldown
    cycle = 5
    focus = 1
    focusCmd = "voldown"
    cmdRow = [6701, 6813, 6928, 7038, 7151]
    # timestamps: [1530880536703,1530880537153,1530880537603,1530880538053,1530880538504,1530880538954]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 6 cycles focus onvoldown
    cycle = 6
    focus = 1
    focusCmd = "voldown"
    cmdRow = [7264, 7376, 7489, 7602, 7714]
    # timestamps: [1530880539403,1530880539853,1530880540302,1530880540753,1530880541203,1530880541653]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 7 cycles focus onvoldown
    cycle = 7
    focus = 1
    focusCmd = "voldown"
    cmdRow = [7827, 7937, 8052, 8165, 8277]
    # timestamps: [1530880542103,1530880542554,1530880543004,1530880543452,1530880543904,1530880544352]
    # commands: ["next","voldown","playpause","prev","volup"]


def detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd):
    print("----- Cycle " + str(cycle) + " focused command " + str(focusCmd) + " correct pos" + str(focus) + " -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 4
    slotSize = 125  # 0.5s
    cmdCount = 5
    allData = []
    for i in range(len(data1)):
        allData.append(np.mean([data2[i], data3[i]]))

    ## FILTER DATA
    # allDataFilterd = data    // if no bandpass desired
    allDataFilterd1 = filterData(data1, lowcut, highcut, fs, order)
    allDataFilterd2 = filterData(data2, lowcut, highcut, fs, order)
    allDataFilterd3 = filterData(data3, lowcut, highcut, fs, order)
    allDataFilterd = filterData(allData, lowcut, highcut, fs, order)

    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300 = []
    dataP300_2 = []
    dataP300_3 = []
    dataP300all = []
    for i in range(cmdCount):
        dataP300.append(allDataFilterd1[cmdRow[i]:cmdRow[i] + slotSize])
        dataP300_2.append(allDataFilterd2[cmdRow[i]:cmdRow[i] + slotSize])
        dataP300_3.append(allDataFilterd3[cmdRow[i]:cmdRow[i] + slotSize])
        dataP300all.append(allDataFilterd[cmdRow[i]:cmdRow[i] + slotSize])

    ## SUBTRACT BASELINE MEAN ( equally ajust height )
    dataP300Baseline = []
    dataP300Baseline_2 = []
    dataP300Baseline_3 = []
    dataP300Baseline_4 = []
    for i in range(cmdCount):
        mean = np.mean(dataP300[i])
        dataP300Baseline.append(dataP300[i] - mean)
        mean_2 = np.mean(dataP300_2[i])
        dataP300Baseline_2.append(dataP300_2[i] - mean_2)
        mean_3 = np.mean(dataP300_3[i])
        dataP300Baseline_3.append(dataP300_3[i] - mean_3)
        mean_4 = np.mean(dataP300all[i])
        dataP300Baseline_4.append(dataP300all[i] - mean_4)
    # Overwrite dataP300 array

    dataP300 = dataP300Baseline
    dataP300_2 = dataP300Baseline_2
    dataP300_3 = dataP300Baseline_3
    dataP300all = dataP300Baseline_4

    ## CALCULATE AMPLITUDE # ONLY ANALYSE DATA BETWEEN 200ms(50) and 400ms(100) AFTER CMD
    # for i in range(cmdCount):
    #     if (foundP300[i] > 0 and abs(foundP300[i] - foundP300_2[i]) < 2):
    #         print("!! Found amplitude in both channels for cmd: " + str(i) + " diff:" + str(
    #             foundP300[i] - foundP300_2[i]))

    diffMaxMin = getMaxMinDiff(dataP300, cmdCount)
    idx = diffMaxMin.index(np.max(diffMaxMin))
    print("Dataset 1: " + str(idx) + " cmd with biggest diff min/max")
    diffMaxMin = getMaxMinDiff(dataP300_2, cmdCount)
    idx2 = diffMaxMin.index(np.max(diffMaxMin))
    print("Dataset 2: " + str(idx2) + " cmd with biggest diff min/max")

    plt.figure(1)
    dataP300Cycle = np.array(dataP300).flatten()
    plotCycle(dataP300Cycle, lowcut, highcut, cycle, 'y')
    dataP300Cycle_2 = np.array(dataP300_2).flatten()
    plotCycle(dataP300Cycle_2, lowcut, highcut, cycle, 'g')
    plt.figure(2)
    dataP300Cycle_3 = np.array(dataP300_3).flatten()
    plotCycle(dataP300Cycle_3, lowcut, highcut, cycle, 'b')
    dataP300Cycle_all = np.array(dataP300all).flatten()
    plotCycle(dataP300Cycle_all, lowcut, highcut, cycle, 'r')
    # Plot commands
    plt.figure(3)
    for i in range(cmdCount):
        if (i == focus):
            plot(dataP300all[i], cycle, focusCmd, i + 1, 'r', cmdRow[i])
        else:
            plot(dataP300all[i], cycle, ("cmd %s" % (i + 1)), i + 1, 'b', cmdRow[i])

    # plt.figure(4)
    # for i in range(cmdCount):
    #     if(i == focus):
    #         plot(dataP300_2[i], cycle, focusCmd, i+1, 'g', cmdRow[i])
    #     else:
    #         plot(dataP300_2[i], cycle, ("cmd %s"%(i+1)), i+1, 'y', cmdRow[i])
    plt.show()


def getMaxMinDiff(data, cmdCount):
    diff = []
    for i in range(cmdCount):
        diff.append(np.max(data[i][40:80]) - np.min(data[i][40:80]))
    # print("Max Diff: "+str(np.max(diff)*10000000))
    return diff


def compareMaxWithStd(data, cmdCount, foundP300):
    for i in range(cmdCount):
        max = np.max(data[i][40:80])
        maxIdx = np.argmax(data[i][40:80]) + 40
        mean = np.mean(data[i][0:100])
        std = np.std(data[i][0:100])
        diff = max / std
        # print(str(i)+": max Sample: "+str(max)+" "+str(maxIdx)+" mean "+str(mean)+" std "+str(std)+" max/std "+str(max/std))
        if (diff > 1.5):
            foundP300[i] = maxIdx
        else:
            foundP300[i] = 0

    return foundP300


def plotCycle(data, lowcut, highcut, cycle, color):
    plt.figure(cycle)
    plt.title(' P300 Cmd: %d Cycle (%d - %d Hz)' % (cycle, lowcut, highcut))
    plt.plot(data * 1000000, color=color)
    plt.ylabel('uV')
    plt.xlabel('Samples 250/s')
    axes = plt.gca()


def detectP300MultiChannels(data, data3, data5, cmdRowFocus, cmdRowNoFocus):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 4
    slotSize = 125  # 0.5s
    cycleCount = 9

    allDataFilterd1 = filterData(data, lowcut, highcut, fs, order)
    allDataFilterd3 = filterData(data3, lowcut, highcut, fs, order)
    allDataFilterd5 = filterData(data5, lowcut, highcut, fs, order)
    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300_Ch1 = []
    dataP300_Ch3 = []
    dataP300_Ch5 = []
    dataP300_Ch1NoFocus = []
    dataP300_Ch3NoFocus = []
    dataP300_Ch5NoFocus = []
    data300SubBaseline = []

    for i in range(cycleCount):
        ## SUBTRACT BASELINE MEAN
        dataP300_Ch1.append(allDataFilterd1[cmdRowFocus[i]:cmdRowFocus[i] + slotSize])
        dataP300_Ch3.append(allDataFilterd3[cmdRowFocus[i]:cmdRowFocus[i] + slotSize])
        dataP300_Ch5.append(allDataFilterd5[cmdRowFocus[i]:cmdRowFocus[i] + slotSize])
        dataP300_Ch1NoFocus.append(allDataFilterd1[cmdRowNoFocus[i]:cmdRowNoFocus[i] + slotSize])
        dataP300_Ch3NoFocus.append(allDataFilterd3[cmdRowNoFocus[i]:cmdRowNoFocus[i] + slotSize])
        dataP300_Ch5NoFocus.append(allDataFilterd5[cmdRowNoFocus[i]:cmdRowNoFocus[i] + slotSize])

    # SUBSTRACT BASELINE
    dataP300_Ch1 = substractBaselineMean(dataP300_Ch1, cycleCount)
    dataP300_Ch3 = substractBaselineMean(dataP300_Ch3, cycleCount)
    dataP300_Ch5 = substractBaselineMean(dataP300_Ch5, cycleCount)
    dataP300_Ch1NoFocus = substractBaselineMean(dataP300_Ch1NoFocus, cycleCount)
    dataP300_Ch3NoFocus = substractBaselineMean(dataP300_Ch3NoFocus, cycleCount)
    dataP300_Ch5NoFocus = substractBaselineMean(dataP300_Ch5NoFocus, cycleCount)

    # Plot cycle
    dataP300Cycle = np.array(dataP300_Ch1).flatten()
    print(dataP300_Ch1)
    plt.figure(1)
    for i in range(3, cycleCount):
        plotChannel(dataP300_Ch1[i] * 1000000, lowcut, highcut, "voldown", 1, i + 1, 'r')
    plt.figure(2)
    for i in range(3, cycleCount):
        plotChannel(dataP300_Ch1NoFocus[i] * 1000000, lowcut, highcut, "prev", 1, i + 1, 'b')
    plt.figure(3)
    for i in range(3, cycleCount):
        plotChannel(dataP300_Ch3[i] * 1000000, lowcut, highcut, "voldown", 3, i + 1, 'r')
    plt.figure(4)
    for i in range(3, cycleCount):
        plotChannel(dataP300_Ch3NoFocus[i] * 1000000, lowcut, highcut, "prev", 1, i + 1, 'b')

    plt.figure(5)
    for i in range(3, cycleCount):
        plotChannel(dataP300_Ch5[i] * 1000000, lowcut, highcut, "voldown", 5, i + 1, 'r')
    plt.figure(6)
    for i in range(3, cycleCount):
        plotChannel(dataP300_Ch5NoFocus[i] * 1000000, lowcut, highcut, "prev", 1, i + 1, 'b')

    plt.show()


def substractBaselineMean(dataP300, cycleCount):
    # SUBTRACT BASELINE MEAN ( equally ajust height )
    dataP300Baseline = []
    for i in range(cycleCount):
        mean = np.mean(dataP300[i])
        dataP300Baseline.append(dataP300[i] - mean)
    return dataP300Baseline


def substractBaselineMeanFromEpocheAndEpocheBefore(dataP300, cycleCount):
    # SUBTRACT BASELINE MEAN ( equally ajust height )
    dataP300Baseline = []
    dataP300Mean = []
    for i in range(cycleCount):
        dataP300Mean.append(dataP300[i - 1])
        dataP300Mean.append(dataP300[i])
        mean = np.mean(dataP300Mean)
        dataP300Baseline.append(dataP300[i] - mean)
    return dataP300Baseline


def substractBaselineFromEpocheBefore(dataP300, cycleCount):
    dataP300Baseline = []
    ## SUBTRACT BASELINE for each datapoint from period before
    dataP300Baseline = []
    for i in range(cycleCount):
        mean = np.mean(dataP300[i - 1])
        dataP300Baseline.append(dataP300[i] - mean)
    return dataP300Baseline


def getChannelData(data, channel):
    channelData = []
    for val in data:
        channelData.append(val["channelData"][channel])
    return channelData


def filterData(data, lowcut, highcut, fs, order):
    # filter data with butter bandpass
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


def plotChannel(data, lowcut, highcut, cmd, channel, subplotNr, color):
    nr = 320 + subplotNr - 3
    plt.subplot(nr)
    plt.title('Ch: %d Cycle: %d  (%s, %d - %d Hz)' % (channel, subplotNr, cmd, lowcut, highcut))
    plt.plot(data, color=color)
    plt.ylabel('uV')
    plt.xlabel('Samples 250/s')
    axes = plt.gca()
    # axes.set_ylim([-20, 20])


def plot(filteredData, cycle, title, cmd, color, row):
    # Plot original and filtered data
    nr = 320 + cmd
    plt.subplot(nr)
    plt.title(' P300 Cycle: %d Cmd: %s ' % (cycle, row))
    plt.plot(filteredData * 1000000, label=title, color=color)
    axes = plt.gca()
    # axes.set_ylim([-100, 100])
    plt.ylabel('microVolts')
    plt.xlabel('Samples 250/s')
    # plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    # plt.grid(True)


# start process
if __name__ == '__main__':
    main()

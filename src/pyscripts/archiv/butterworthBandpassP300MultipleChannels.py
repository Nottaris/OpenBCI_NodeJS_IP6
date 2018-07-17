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
    with open('../../test/data/p300_exp_3/data-2018-7-6-14-32-40.json') as f:
        dataJson = json.load(f)
    # Get channel data
    data1 = getChannelData(dataJson, 0)
    data2 = getChannelData(dataJson, 3)
    data3 = getChannelData(dataJson, 5)
    # commands data/data-2018-7-6-14-32-40.json
    # command order: next,voldown,playpause,prev,volup
    # 1 cycles focus onplaypause
    cycle = 1
    focus = 2
    focusCmd = "playpause"
    cmdRow = [5470, 5540, 5652, 5765, 5878, 5991]
    # timestamps: [1530880386457,1530880386734,1530880387184,1530880387633,1530880388083,1530880388533]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 2 cycles focus onplaypause
    cycle = 2
    focus = 2
    focusCmd = "playpause"
    cmdRow = [6103, 6216, 6328, 6441, 6554, 6666]
    # timestamps: [1530880388983,1530880389434,1530880389883,1530880390334,1530880390783,1530880391233]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 3 cycles focus onplaypause
    cycle = 3
    focus = 2
    focusCmd = "playpause"
    cmdRow = [6779, 6891, 7004, 7117, 7229, 7342]
    # timestamps: [1530880391683,1530880392134,1530880392584,1530880393033,1530880393482,1530880393934]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 4 cycles focus onplaypause
    cycle = 4
    focus = 2
    focusCmd = "playpause"
    cmdRow = [7454, 7567, 7680, 7792, 7905, 8017]
    # timestamps: [1530880394385,1530880394834,1530880395284,1530880395733,1530880396183,1530880396633]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 5 cycles focus onplaypause
    cycle = 5
    focus = 2
    focusCmd = "playpause"
    cmdRow = [8130, 8243, 8355, 8468, 8581, 8693]
    # timestamps: [1530880397082,1530880397533,1530880397982,1530880398434,1530880398883,1530880399334]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 6 cycles focus onplaypause
    cycle = 6
    focus = 2
    focusCmd = "playpause"
    cmdRow = [8806, 8918, 9031, 9144, 9256, 9369]
    # timestamps: [1530880399782,1530880400233,1530880400682,1530880401133,1530880401584,1530880402033]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 7 cycles focus onplaypause
    cycle = 7
    focus = 2
    focusCmd = "playpause"
    cmdRow = [9481, 9594, 9707, 9819, 9932, 10044]
    # timestamps: [1530880402483,1530880402932,1530880403385,1530880403834,1530880404283,1530880404734]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 8 cycles focus onplaypause
    cycle = 8
    focus = 2
    focusCmd = "playpause"
    cmdRow = [10157, 10270, 10382, 10495, 10608, 10720]
    # timestamps: [1530880405183,1530880405634,1530880406083,1530880406534,1530880406984,1530880407432]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 9 cycles focus onplaypause
    cycle = 9
    focus = 2
    focusCmd = "playpause"
    cmdRow = [10833, 10944, 11058, 11171, 11283, 11396]
    # timestamps: [1530880407884,1530880408333,1530880408783,1530880409234,1530880409684,1530880410133]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 10 cycles focus onplaypause
    cycle = 10
    focus = 2
    focusCmd = "playpause"
    cmdRow = [11508, 11621, 11734, 11846, 11959, 12071]
    # timestamps: [1530880410584,1530880411032,1530880411484,1530880411934,1530880412383,1530880412833]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)
    # 11 cycles focus onplaypause
    cycle = 11
    focus = 2
    focusCmd = "playpause"
    cmdRow = [12184, 12297, 12409, 12522, 12634, 12747]
    # timestamps: [1530880413284,1530880413732,1530880414183,1530880414633,1530880415083,1530880415534]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data1, data2, data3, cmdRow, cycle, focus, focusCmd)


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
    commands = ["next", "voldown", "playpause", "prev", "volup"]
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

    # diffMaxMin = getMaxMinDiff(dataP300, cmdCount)
    # idx = diffMaxMin.index(np.max(diffMaxMin))
    # print("Dataset 1: " + str(idx) + " cmd with biggest diff min/max")
    # diffMaxMin = getMaxMinDiff(dataP300_2, cmdCount)
    # idx2 = diffMaxMin.index(np.max(diffMaxMin))
    # print("Dataset 2: " + str(idx2) + " cmd with biggest diff min/max")

    plt.figure(1)
    dataP300Cycle = np.array(dataP300).flatten()
    plotCycle(dataP300Cycle, lowcut, highcut, cycle, 'b',"Oz")
    dataP300Cycle_2 = np.array(dataP300_2).flatten()
    plotCycle(dataP300Cycle_2, lowcut, highcut, cycle, 'b',"O1")
    plt.figure(2)
    dataP300Cycle_3 = np.array(dataP300_3).flatten()
    plotCycle(dataP300Cycle_3, lowcut, highcut, cycle, 'b',"O2")
    dataP300Cycle_all = np.array(dataP300all).flatten()
    plotCycle(dataP300Cycle_all, lowcut, highcut, cycle, 'r',"Avg")
    # Plot commands
    plt.figure(3)
    for i in range(cmdCount):
        if (i == focus):
            plotChannels(dataP300all[i], cycle, focusCmd, 'r', commands[i], "avg",i)
            plotChannels(dataP300[i], cycle, focusCmd, 'b', commands[i], "Oz",i)
            plotChannels(dataP300_2[i], cycle, focusCmd, 'b', commands[i], "O1",i )
            plotChannels(dataP300_3[i], cycle, focusCmd, 'b', commands[i], "O2",i)
        else:
            plotChannels(dataP300all[i], cycle, focusCmd, 'r', commands[i], "avg",i)
            plotChannels(dataP300[i], cycle, focusCmd, 'b', commands[i], "Oz",i)
            plotChannels(dataP300_2[i], cycle, focusCmd, 'b', commands[i], "O1",i )
            plotChannels(dataP300_3[i], cycle, focusCmd, 'b', commands[i], "O2",i)

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

def plotChannels(data, cycle, focusCmd, color, cmd, channel, nr):
    plt.figure(nr+1)
    # Plot original and filtered data
    plt.title(' Compare Channels Cycle: %d Cmd: %s ' % (cycle, cmd))
    plt.plot(data * 1000000, label=channel, color=color)
    axes = plt.gca()
    # axes.set_ylim([-100, 100])
    plt.ylabel('microVolts')
    plt.xlabel('Samples 250/s')
    plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    # plt.grid(True)


def plotCycle(data, lowcut, highcut, cycle, color, channel):
    plt.figure(cycle)
    plt.title('Compare Channels Cycle: %d (%d - %d Hz)' % (cycle, lowcut, highcut))
    plt.plot(data * 1000000, label=channel, color=color)
    plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
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

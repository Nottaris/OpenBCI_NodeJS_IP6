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

    # 4 cycles focus onplaypause
    cmdNext = [8130,8806,9481,10157,10833]
    cmdPlay = [8355,9031,9707,10382,11058]
    detectP300(data1, data2, data3, cmdNext, "next", 0)
    detectP300(data1, data2, data3, cmdPlay, "playpause", 1)

def detectP300(data1, data2, data3, cmdRow, focus, focusCmd):
    print("----- Avg  " + str(len(cmdRow)) + "Cycle focused command " + str(focusCmd) + " correct pos" + str(focus) + " -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 4
    slotSize = 125  # 0.5s
    cmdCount = 5
    allData = []
    cycle = 0
    commands = ["next", "voldown", "playpause", "prev", "volup"]

    # for i in range(len(data1)):
    #     allData.append(np.mean([data2[i], data3[i]]))

    ## FILTER DATA
    # allDataFilterd = data    // if no bandpass desired
    allDataFilterd1 = filterData(data1, lowcut, highcut, fs, order)
    allDataFilterd2 = filterData(data2, lowcut, highcut, fs, order)
    allDataFilterd3 = filterData(data3, lowcut, highcut, fs, order)

    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300 = [[],[],[],[],[]]
    for i in range(len(cmdRow)):
        dataP300[i].append(allDataFilterd1[cmdRow[i]:cmdRow[i] + slotSize])



    # print(len(dataP300all))
    # print(len(dataP300))
    ## SUBTRACT BASELINE MEAN ( equally ajust height )
    dataP300Baseline =[[],[],[],[],[]]
    for i in range(len(cmdRow)):
        mean = np.mean(dataP300[i][0])
        dataP300Baseline[i] = dataP300[i][0]-mean


    # Overwrite dataP300 array
    dataP300 = dataP300Baseline


    # Get Avg
    dataP300avg = np.average(dataP300, axis=0)
    dataP300Sum = dataP300[0]
    for i in range(1,len(cmdRow)):
        dataP300Sum = np.sum(np.array([dataP300Sum,dataP300[i]]), axis=0)

    plt.figure(1)
    for i in range(len(cmdRow)):
        plotCycle(dataP300[i], lowcut, highcut,  'b', ("Cycle "+str(i)),focus)

    plotCycle(dataP300avg, lowcut, highcut,  'r', "Avg",focus)

    plt.figure()
    for i in range(len(cmdRow)):
        plotCycleSum(dataP300[i], lowcut, highcut,  'b', ("Cycle "+str(i)),focus)

    plotCycleSum(dataP300Sum, lowcut, highcut,  'r', "Sum",focus)
    #
    # # plt.figure(4)
    # # for i in range(cmdCount):
    # #     if(i == focus):
    # #         plot(dataP300_2[i], cycle, focusCmd, i+1, 'g', cmdRow[i])
    # #     else:
    # #         plot(dataP300_2[i], cycle, ("cmd %s"%(i+1)), i+1, 'y', cmdRow[i])
    plt.show()


def plotCycle(data, lowcut, highcut, color, cycle, cmd):
    plt.title('Avg with 5 Cycle:  (%d - %d Hz) cmd %s' % (lowcut, highcut, cmd))
    plt.plot(data * 1000000, label=cycle, color=color)
    plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    plt.ylabel('uV')
    plt.xlabel('Samples 250/s')
    axes = plt.gca()

def plotCycleSum(data, lowcut, highcut, color, cycle, cmd):
    plt.title('Sum with 5 Cycle:  (%d - %d Hz) cmd %s' % (lowcut, highcut, cmd))
    plt.plot(data * 1000000, label=cycle, color=color)
    plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    plt.ylabel('uV')
    plt.xlabel('Samples 250/s')

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

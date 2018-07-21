from typing import List, Any

from scipy.signal import butter, lfilter
import json, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm

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
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410890_1_baseline.json') as f:
        baseline = json.load(f)
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410878_1_volts.json') as f:
        volts = json.load(f)
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410893_1_cmdIdx.json') as f:
        cmdIdx = json.load(f)

    # create a numpy array
    volts = np.array(volts)  # about 10 sec., enough for 3 cycles at least (4 sharp)
    baseline = np.array(baseline)
    # # cmd = detectP300(data, cmdIdx)

    ## active channels
    channels = [0, 1, 2, 3, 4, 5, 6, 7]  # 0-7 channels

    filterChannelData(volts, baseline, cmdIdx, channels)
    # extractFeature(dataChannel, dataBaseline, channels)


def filterChannelData(volts, baseline, cmdIdx, channels):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 12.0
    order = 4
    cmdCount = len(cmdIdx)
    slotSize = 120

    ## BP FILTER DATA
    channelDataBP = []
    for channel in range(len(channels)):
        #add baseline before filter BP
        dataWithBaseline = np.concatenate([baseline[:, channel], volts[:, channel]])
        dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
        #cut off baseline again
        channelDataBP.append(dataFilterd[len(baseline[:, channel]):])

        # Plot filterd data
        plt.figure(channel)
        plt.title("filterd data - Channel " + str(channel))
        plt.plot(channelDataBP[channel], color='r')
        plt.show()
        # Plot raw data
        plt.figure(channel+10)
        plt.title("Raw data - Channel " + str(channel))
        plt.plot(volts[:, channel], color='b')
        plt.show()

    ## BP FILTER BASELINE
    baselineDataBP = []
    for channel in range(len(channels)):
        dataFilterd = filterData(baseline[:, channel], lowcut, highcut, fs, order) #baseline is 1000 samples
        baselineDataBP.append(
            dataFilterd[int(len(baseline[:, channel]) / 4):int(3*(len(baseline[:, channel]) / 4))]
        )  # middle half (500 samples)

        # Plot filterd baseline
        plt.figure(channel+20)
        plt.title("filterd Baseline - Channel " + str(channel))
        plt.plot(baselineDataBP[channel], color='g')
        plt.show()


    ## SPLIT VOLTS DATA IN COMMAND EPOCHES
    ## collect volt for each cmd in dataP300[CMD][CHANNEL][VOLTS] of all cycles
    dataP300 = [[], [], [], [], []]
    cycles = 3
    print(cmdIdx)
    for cmd in range(cmdCount):
        for channel in range(len(channels)):
            for cycle in range(0, cycles):
                dataP300[cmd].append(
                    channelDataBP[channel][cmdIdx[cmd][cycle]:(cmdIdx[cmd][cycle] + slotSize)]
                )

    print("len(dataP300) aka 5 cmds: " + str(len(dataP300)))
    print("len(dataP300[0]) aka 3cycles*8channels = 24 : " + str(len(dataP300[0])))
    print("len(dataP300[0][1]) slotsize 120: " + str(len(dataP300[0][1])))

    ## SPLIT BASELINE IN EPOCHES
    blP300 = []
    cycles = 3
    print(cmdIdx)
    for channel in range(len(channels)):
        for cycle in range(0, cycles):
            blP300.append(
                baselineDataBP[channel][120*cycle:120*cycle + slotSize]
            )

    print("len(blP300) aka 3cycles*8channels = 24 : " + str(len(blP300)))
    print("len(blP300[0])  slotsize 120: " + str(len(blP300[0])))

    extractFeature(np.array(dataP300), np.array(blP300))


def extractFeature(dataP300, blP300):
    print("extract features: ")
    #baseline blP300 is non-target
    #dataP300 cmd playpause index=2 is target
    dataP300target = dataP300[2]
    trainData = np.concatenate((dataP300target, blP300))
    nx, ny = trainData.shape
    print(nx)
    print(ny)
    # create label y
    z = np.zeros(24)  # 0 = non-target for blP300
    o = np.ones(24)   # 1 = target for dataP300target
    y = np.concatenate((o, z))
    print(y)
    clf = svm.SVC()
    clf.fit(trainData, y)




def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

from typing import List, Any

from scipy.signal import butter, lfilter
import json, sys, numpy as np, matplotlib.pyplot as plt
from scipy import signal

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
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410893_1_cmdIdx_Training.json') as f:
        cmdIdx = json.load(f)

    # create a numpy array
    volts = np.array(volts)
    baseline = np.array(baseline)
    # # cmd = detectP300(data, cmdIdx)

    ## active channels
    channels = [0,1,2,3,4,5,6,7]  # 0-7 channels

    filterChannelData(volts, baseline, cmdIdx, channels)
    # extractFeature(dataChannel, dataBaseline, channels)





def filterChannelData(data, baseline, cmdIdx, channels):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 12.0
    order = 4
    cmdCount = len(cmdIdx)
    slotSize = 120

    # ## FILTER DATA
    # # Split channel Data
    channelDataBP = []
    for channel in range(len(channels)):
        dataWithBaseline = np.concatenate([baseline[:,channel], data[:,channel]])
        dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
        channelDataBP.append(dataFilterd[len(baseline[:,channel]):])
        # Plot filterd data
        plt.figure(channel)
        plt.title("filterd data - Channel " + str(channel))
        plt.plot(channelDataBP[channel], color='r')

        plt.figure(channel)
        plt.title("Raw data - Channel " + str(channel))
        plt.plot(data[:,channel], color='b')
    plt.show()

    # ## SPLIT VOLTS DATA IN COMMAND EPOCHES
    ##  collect volt for each cmd in dataP300[CMD][CHANNEL][VOLTS]
    dataP300 = [[], [], [], [], []]
    cycle = 0
    print(cmdIdx)
    for cmd in range(cmdCount):
        for channel in range(len(channels)):
            dataP300[cmd].append(channelDataBP[channel][cmdIdx[cmd][cycle]:(cmdIdx[cmd][cycle] + slotSize)])

    print(len(dataP300[0][1]))

def extractFeature(dataChannel, dataBaseline, channels):
    print("extract feature")

def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

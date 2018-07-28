from scipy.signal import butter, lfilter, decimate, resample
import json, os, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
import pickle



def filterDownsampleData(volts, baseline, commands, debug):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 16.0
    highcut = 24.0
    order = 4
    startSample = 1500
    endSample = 1750
    cmdCount = len(commands)
    downsampleFactor = 12   # reduce dimensions by this factor
    downsampleSize = int(len(volts)/downsampleFactor)   #resulting size of downsampled data depending on input size
    # ToDO: Set correct Channel Count
    channels = [1, 2]

    ## BP FILTER DATA
    channelDataBP = []
    baselineDataBP = []

    for cmd in range(cmdCount):
        channelData = []
        channelBaselineData = []
        for c in range(len(channels)):
            # add baseline before filter BP
            dataFilterd = filterData(volts[cmd][:, channels[c]], lowcut, highcut, fs, order)
            # cut off baseline again
            channelData.append(dataFilterd)

            if (debug):
                if(cmd == 2 or cmd == 3):
                    # plt.figure(channel + 1)
                    # plt.title("filterd Baseline Cmd " + str(commands[cmd]) + " - Channel " + str(channel))
                    # plt.plot(channelBaselineData[channel] * 1000000, color='g')
                    # axes = plt.gca()
                    # axes.set_ylim([-40, 40])
                    plt.figure(c + 2)
                    plt.plot(channelData[c] * 1000000, color='r')
                    plt.title("Data Cmd " + str(commands[cmd]) + " - Channel " + str(c))
                    # axes = plt.gca()
                    # axes.set_ylim([-40, 40])
                    plt.show()
        channelDataBP.append(channelData)
        baselineDataBP.append(channelBaselineData)


    ## EXTRACT EPOCHE BETWEEN 0.5 - 1.5 s (125 - 375) FOR EACH COMMAND
    ## dataMind[CMD][CHANNEL][VOLTS]
    dataMind = []
    for cmd in range(cmdCount):
        channelData = []
        for channel in range(len(channels)):
            channelData.append(channelDataBP[cmd][channel][startSample:endSample])
            squareData = np.square(channelData[channel]* 1000000)
            mean = np.mean(squareData)

            if (debug):
                if (cmd == 2 or cmd == 3):
                    print("cmd: "+str(cmd) + " channel " + str(channel) + " mean: " + str(mean))
                    plt.figure(channel)
                    plt.title("Train Epoche Cmd " + str(commands[cmd]) + " - Channel " + str(channel))
                    plt.plot(channelData[channel] * 1000000, color='b')
                    plt.plot(np.square(channelData[channel]* 1000000) , color='r')
                    axes = plt.gca()
                    axes.set_ylim([0, 100])
                    plt.show()
        dataMind.append(channelData)

        # ToDo: Imolement common spacial pattern
        ## SPACIAL PATTERM


    return dataMind, baselineDataBP




def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData

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

##
# detect mind commands
# (beta, unfinished)
#
# Source butter_bandpass http://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html
#
##

from scipy.signal import butter, lfilter, decimate, resample
import json, os, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
import pickle


def filterDownsampleData(volts, baseline, commands, debug):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 8.0
    highcut = 30.0
    order = 4
    startSample = 250   #analyse three 1 second slots in training phase
    sampleSize = 250
    cmdCount = len(commands)
    downsampleFactor = 12  # reduce dimensions by this factor
    downsampleSize = int(len(volts) / downsampleFactor)  # resulting size of downsampled data depending on input size
    channels = [0, 1, 2, 3, 4, 5, 6, 7]

    ## BP FILTER DATA
    ## volts[CMD][Samples][Channels]
    voltsBP = []
    baselineBP = []

    for cmd in range(cmdCount):
        voltsPerCmd = []
        baselinePerCmd = []
        for c in range(len(channels)):
            # print("volts[cmd][:, c] : "+str(len(volts[cmd][:, c])))
            dataBP = filterData(volts[cmd][:, c], lowcut, highcut, fs, order)
            voltsPerCmd.append(dataBP)
            dataBPbl = filterData(baseline[:, c], lowcut, highcut, fs, order)
            baselinePerCmd.append(dataBPbl)

            if (debug):
                if (cmd == 2 or cmd == 3):
                    # plt.figure(channel + 1)
                    # plt.title("filterd Baseline Cmd " + str(commands[cmd]) + " - Channel " + str(channel))
                    # plt.plot(channelBaselineData[channel] * 1000000, color='g')
                    # axes = plt.gca()
                    # axes.set_ylim([-40, 40])
                    plt.figure(c + 2)
                    plt.plot(voltsPerCmd[c] * 1000000, color='r')
                    plt.title("Data Cmd " + str(commands[cmd]) + " - Channel " + str(c))
                    # axes = plt.gca()
                    # axes.set_ylim([-40, 40])
                    plt.show()
        voltsBP.append(voltsPerCmd)
        baselineBP.append(baselinePerCmd)

    ## analyse 3 seconds  from 1-4 seconds in training phase
    ## dataMind[CMD][CHANNEL][sampleVOLTS]
    dataMind = []
    for cmd in range(cmdCount):
        channelData = []
        for channel in range(len(channels)):
            #take three seconds from each training phase
            channelData.append(voltsBP[cmd][channel][startSample:startSample+sampleSize])
            channelData.append(voltsBP[cmd][channel][startSample+sampleSize:startSample+2*sampleSize])
            channelData.append(voltsBP[cmd][channel][startSample+2*sampleSize:startSample+3*sampleSize])

            # squareData = np.square(channelData[channel] * 1000000)
            # mean = np.mean(squareData)

            # if (debug):
            #     if (cmd == 2 or cmd == 3):
            #      #   print("cmd: " + str(cmd) + " channel " + str(channel) + " mean: " + str(mean))
            #         plt.figure(channel)
            #         plt.title("Train Epoche Cmd " + str(commands[cmd]) + " - Channel " + str(channel))
            #         plt.plot(channelData[channel] * 1000000, color='b')
            #         plt.plot(np.square(channelData[channel] * 1000000), color='r')
            #         axes = plt.gca()
            #         axes.set_ylim([0, 100])
            #         plt.show()
        dataMind.append(channelData)

    ## ToDo: Implement common spacial pattern

    return dataMind, baselineBP


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

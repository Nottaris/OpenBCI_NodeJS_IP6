from scipy.signal import butter, lfilter, decimate, resample
import json, os, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
import pickle


substractBaseline = False

def filterDownsampleData(volts, baseline, commands, debug):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 8
    highcut = 30.0
    order = 5
    startSample = 125
    endSample = 375
    cmdCount = len(commands)
    downsampleFactor = 12   # reduce dimensions by this factor
    downsampleSize = int(len(volts)/downsampleFactor)   #resulting size of downsampled data depending on input size
    channels = 8    # always use all 8 channels

    ## BP FILTER DATA
    channelDataBP = []
    baselineDataBP = []

    for cmd in range(cmdCount):
        channelData = []
        channelBaselineData = []
        for channel in range(channels):
            # add baseline before filter BP
            dataWithBaseline = np.concatenate([baseline[:, channel], volts[cmd][:, channel]])
            dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
            # cut off baseline again
            channelData.append(dataFilterd[len(baseline[:, channel])-1:])
            channelBaselineData.append(dataFilterd[1000:len(baseline)])  # baseline is 9000 samples
            if (debug):
                plt.figure(channel + 1)
                plt.title("filterd Baseline Cmd " + str(commands[cmd]) + " - Channel " + str(channel))
                plt.plot(channelBaselineData[channel] * 1000000, color='g')
                plt.figure(channel + 2)
                plt.plot(channelData[channel] * 1000000, color='r')
                plt.title("Data Cmd " + str(commands[cmd]) + " - Channel " + str(channel))
                plt.show()
        channelDataBP.append(channelData)
        baselineDataBP.append(channelBaselineData)


    ## EXTRACT EPOCHE BETWEEN 0.5 - 1.5 s (125 - 375) FOR EACH COMMAND
    ## dataMind[CMD][CHANNEL][VOLTS]
    dataMind = []
    for cmd in range(cmdCount):
        channelData = []
        for channel in range(channels):
            channelData.append(channelDataBP[cmd][channel][startSample:endSample])
            if (debug):
                plt.figure(channel)
                plt.title("Train Epoche Cmd " + str(commands[cmd]) + " - Channel " + str(channel))
                plt.plot(channelData[channel] * 1000000, color='b')
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

from scipy.signal import butter, lfilter, decimate, resample
import json, os, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
import pickle


substractBaseline = False

def filterDownsampleData(volts, baseline, y, debug):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 8
    highcut = 30.0
    order = 5
    cmdCount = len(y)
    downsampleFactor = 12   # reduce dimensions by this factor
    downsampleSize = int(len(volts)/downsampleFactor)   #resulting size of downsampled data depending on input size
    channels = 8    # always use all 8 channels

    ## BP FILTER DATA
    channelDataBP = []
    baselineDataBP = []
    for channel in range(channels):
        # add baseline before filter BP
        dataWithBaseline = np.concatenate([baseline[:, channel], volts[:, channel]])
        dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
        # cut off baseline again
        channelDataBP.append(dataFilterd[len(baseline[:, channel])-1:])
        #get Baseline without first 1000 samples
        baselineDataBP.append(dataFilterd[1000:len(baseline)])
        if (debug):
            plt.figure(channel + 1)
            plt.title("filterd Baseline - Channel " + str(channel))
            plt.plot(baselineDataBP[channel] * 1000000, color='g')
            plt.figure(channel + 2)
            plt.plot(channelDataBP[channel] * 1000000, color='r')
            plt.title("Baseline Data - Channel " + str(channel))
            plt.show()

    #downsample
    dataDownSample = []
    for cmd in range(cmdCount):
        # Downsample: reduce dimensions from 80 samples to 20 samples
        dataDownSample.append(resample(channelDataBP[cmd], downsampleSize))

    baselineDownSample = resample(baselineDataBP, downsampleSize)

    if(debug):
        print("\n-- Command Data (Downsampled) ---")
        print("len(dataDownSample) aka 5 cmds: " + str(len(dataDownSample)))
        print("len(dataDownSample[0]) aka trainingSampleLength : " + str(len(dataDownSample[0])))


    return dataDownSample, baselineDownSample




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

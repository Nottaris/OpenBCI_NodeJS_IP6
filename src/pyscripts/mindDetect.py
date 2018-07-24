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

    # Get channel data


def detectMind(data1, data2, data3, cmdRow, cycle, focus, focusCmd):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 4
    slotSize = 125  # 0.5s

    allData = []
    for i in range(len(data1)):
        allData.append(np.mean([data2[i], data3[i]]))

    ## FILTER DATA
    # allDataFilterd = data    // if no bandpass desired
    allDataFilterd1 = filterData(data1, lowcut, highcut, fs, order)
    allDataFilterd2 = filterData(data2, lowcut, highcut, fs, order)
    allDataFilterd3 = filterData(data3, lowcut, highcut, fs, order)
    allDataFilterd = filterData(allData, lowcut, highcut, fs, order)


def getChannelData(data, channel):
    channelData = []
    for val in data:
        channelData.append(val["channelData"][channel])
    return channelData


def filterData(data, lowcut, highcut, fs, order):
    # filter data with butter bandpass
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

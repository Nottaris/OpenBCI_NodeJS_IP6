##
# P300 Functions to prepare data for SVM training: Bandpassfilter and Downsample Data to make features less complex
#
##
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, resample

substractBaseline = True

## filter and downsample command data and baseline
def filterDownsampleData(volts, baseline, cmdIdx, channels, debug):

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 12.0
    order = 6
    cmdCount = len(cmdIdx)
    slotSize = 100      #400 ms
    downsampleSize = 16
    cycles = len(cmdIdx[0])
    channels = len(channels)

    ## 1. BANDPASS FILTER DATA
    channelDataBP = []
    baselineDataBP = []
    for channel in range(channels):
        # add baseline before filter command data
        dataWithBaseline = np.concatenate([baseline[:, channel], volts[:, channel]])
        dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
        # cut off baseline again
        channelDataBP.append(dataFilterd[len(baseline[:, channel])-1:])
        baselineDataBP.append(dataFilterd[1000:len(baseline)])# baseline is 9000 samples
        if (debug):
            plt.figure(channel + 1)
            plt.plot(channelDataBP[channel] * 1000000, color='r')
            plt.title("Filterd Data - Channel " + str(channel))
            plt.show()

    ## 2. SPLIT VOLTS DATA IN COMMAND EPOCHES AND DOWNSAMPLE
    ## collect volt for each cmd in dataP300[CMD][CYCLE][CHANNEL][VOLTS] of all cycles
    dataDownSampleP300 =  []
    for cmd in range(cmdCount):
        cycleData = []
        for cycle in range(cycles):
            channelData = []
            for channel in range(channels):
                volts = channelDataBP[channel][cmdIdx[cmd][cycle]:(cmdIdx[cmd][cycle] + slotSize)]
                if (substractBaseline):
                   # Substract Baseline mean
                    mean = np.mean(volts)
                    volts = volts-mean

                # Downsample: reduce dimensions from 80 samples to 20 samples
                channelData.append(resample(volts, downsampleSize))

            ## save median from  all channels
            # median = np.median(channelData, axis=0)

            cycleData.append(channelData)

        if (debug):
            plt.show()
        dataDownSampleP300.append(cycleData)
    if(debug):
        print("\n-- Command Data (Downsampled) ---")
        print("len(dataDownSampleP300) aka 5 cmds: " + str(len(dataDownSampleP300)))
        print("len(dataDownSampleP300[0]) aka 3 cycles : " + str(len(dataDownSampleP300[0])))
        print("len(dataDownSampleP300[0][0]) aka 20 volts : " + str(len(dataDownSampleP300[0][0])))



    ## SPLIT BASELINE IN COMMAND EPOCHES AND DOWNSAMPLE
    start = 0
    downSampleBaseline = []
    while(start < len(baselineDataBP[0])-slotSize):
        channelData = []
        for channel in range(channels):
            volts = baselineDataBP[channel][start:start + slotSize]
            if (substractBaseline):
                ## SUBTRACT BASELINE MEAN
                mean = np.mean(volts)
                volts = volts-mean
            # Downsample: reduce dimensions from 80 samples to 20 samples
            channelData.append(resample(volts, downsampleSize))
        ## save median from  all channels
        # median = np.median(channelData, axis=0)
        downSampleBaseline.append(channelData)
        start += slotSize

    if(debug):
        print("\n-- Baseline Data (Downsampled) ---")
        print("len(downSampleBaseline[0]) : " + str(len(downSampleBaseline)))
        print("len(downSampleBaseline[0][0]) aka 20 volts : " + str(len(downSampleBaseline[0])))

    return dataDownSampleP300, downSampleBaseline

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

from scipy.signal import butter, lfilter, decimate, resample
import json, os, sys, numpy as np, matplotlib.pyplot as plt

substractBaseline = True

def filterDownsampleData(volts, baseline, cmdIdx, channels, debug, cmdTarget):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 12.0
    order = 6
    cmdCount = len(cmdIdx)
    slotSize = 150 #500 ms
    downsampleSize = 16
    cycles = len(cmdIdx[0])
    channels = len(channels)
    commands = ['playpause','next','prev','volup', 'voldown'];
    colors = ['b','g','r','c','m','y','k','w'];
    channelNames = ['O1','Oz','O2','P3','Pz','P4','Cz','Fz']
    ## BP FILTER DATA
    channelDataBP = []
    baselineDataBP = []
    for channel in range(channels):
        # add baseline before filter BP
        dataWithBaseline = np.concatenate([baseline[:, channel], volts[:, channel]])
        dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
        # cut off baseline again
        channelDataBP.append(dataFilterd[len(baseline[:, channel])-1:])
        baselineDataBP.append(dataFilterd[1000:len(baseline)])# baseline is 9000 samples
        # if (debug):
        #     plt.figure(channel + 1)
        #     plt.title("filterd Baseline - Channel " + str(channel))
        #     plt.plot(baselineDataBP[channel]*1000000, color='g')
        #     plt.figure(channel + 2)
        #     plt.plot(channelDataBP[channel] * 1000000, color='r')
        #     plt.title("Baseline Data - Channel " + str(channel))
        #     plt.show()

    ## SPLIT VOLTS DATA IN COMMAND EPOCHES AND DOWNSAMPLE
    ## collect volt for each cmd in dataP300[CMD][CYCLE][CHANNEL][VOLTS] of all cycles
    paddingSlot = 0 # remove first and last 30 samples from each slot to 30 - 90 (120ms - 360ms)
    dataDownSampleP300 =  []
    for cmd in range(cmdCount):
        cycleData = []
        for cycle in range(cycles):
            channelData = []
            for channel in range(channels):
                volts = channelDataBP[channel][cmdIdx[cmd][cycle] + paddingSlot:(cmdIdx[cmd][cycle] + slotSize - paddingSlot)]
                if (substractBaseline):
                   # Substract Baseline mean
                    mean = np.mean(volts)
                    volts = volts-mean

                # Downsample: reduce dimensions from 80 samples to 20 samples
                channelData.append(resample(volts, downsampleSize))


                if(cmd == cmdTarget):
                    fig1 = plt.figure(cycle + 10)
                    plt.plot(volts * 1000000,  label="Channel "+str(channelNames[channel-1]),  color=colors[channel])
                    plt.legend(loc='lower right')
                    axes = plt.gca()
                    axes.set_ylim([-30, 30])
                    fig1.add_subplot(1, 1, 1, facecolor='lightgray')

                    plt.title(str(commands[cmdTarget])+"Data - Channel 0 - Cycle " + str(cycle))

            ## save median from  all channels
            # median = np.median(channelData, axis=0)

            cycleData.append(channelData)
            # if (cmd == cmdTarget):
                # avg = np.average(cycleData[cycle], axis=0)
                # plt.figure(cycle + 20)
                # axes = plt.gca()
                # axes.set_ylim([-25, 25])
                # plt.plot(avg * 1000000, label="Avg Channels", color='b')
                # plt.title(str(commands[cmdTarget])+" AVG Data - All Channel - Cycle " + str(cycle))
                # plt.figure(cycle + 10)
                # # plt.plot(median * 1000000, label="Median Channels", color='g')
                # plt.legend(loc='lower right')
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

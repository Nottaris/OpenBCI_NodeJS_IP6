from typing import List, Any

from scipy.signal import butter, lfilter, decimate, resample
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


# global variable
clf = svm.SVC()


def main():
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410890_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410878_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410893_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f') # about 10 sec., enough for 3 cycles at least (4 sharp)
    baselineTraining = np.array(baselineTraining, dtype='f')

    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410890_1_baseline.json') as f:
        baselineTest= json.load(f)
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410878_1_volts.json') as f:
        voltsTest = json.load(f)
    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410893_1_cmdIdx.json') as f:
        cmdIdxTest = json.load(f)
    # create a numpy array
    voltsTest = np.array(voltsTest, dtype='f') # about 10 sec., enough for 3 cycles at least (4 sharp)
    baselineTest = np.array(baselineTest, dtype='f')

    ## active channels
    channels = [0, 1, 2, 3, 4, 5, 6, 7]  # 0-7 channels

    ## EXTRACT FEATURES FOR TRAINING DATA
    print("\n------ Traing Data ------")
    ## Training Target
    targetCmd = 0 # Playpause

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels)

    ##  2. Extract Features for Traingsdata
    [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)

    ##  3. Train Model with features


    ## EXTRACT FEATURES FOR TEST DATA
    print("\n------ Test Data ------")
    ## 1. Filter and Downsample Testdata

    [filterdTestdata, filterdTestBaseline] = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels)

    ##  2. Extract Features from Testdata
    [Xtest, ytest] = extractFeature(filterdTestdata, filterdTestBaseline, None)

   ##  3. Compare with Model



def filterDownsampleData(volts, baseline, cmdIdx, channels):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 12.0
    order = 4
    cmdCount = len(cmdIdx)
    slotSize = 120
    commands = ['playpause', 'next', 'prev', 'volup', 'voldown']
    cycles = len(cmdIdx[0])
    channels = len(channels)

    ## BP FILTER DATA
    channelDataBP = []
    for channel in range(channels):
        # add baseline before filter BP
        dataWithBaseline = np.concatenate([baseline[:, channel], volts[:, channel]])
        dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
        # cut off baseline again
        channelDataBP.append(dataFilterd[len(baseline[:, channel])-1:])

        # Plot filterd data
        # plt.figure(channel)
        # plt.title("filterd data - Channel " + str(channel))
        # plt.plot(channelDataBP[channel], color='r')
        # plt.show()
        # Plot raw data
        # plt.figure(channel + 10)
        # plt.title("Raw data - Channel " + str(channel))
        # plt.plot(volts[:, channel], color='b')
        # plt.show()

    # ## BP FILTER BASELINE
    baselineDataBP = []
    for channel in range(channels):
        dataFilterd = filterData(baseline[:, channel], lowcut, highcut, fs, order)  # baseline is 1000 samples
        baselineDataBP.append(dataFilterd)

        # Plot filterd baseline
        # plt.figure(channel + 20)
        # plt.title("filterd Baseline - Channel " + str(channel))
        # plt.plot(baselineDataBP[channel], color='g')
        # plt.show()

    ## SPLIT VOLTS DATA IN COMMAND EPOCHES
    ## collect volt for each cmd in dataP300[CMD][CYCLE][CHANNEL][VOLTS] of all cycles
    paddingSlot = 20 # remove first and last 20 samples from slots
    dataDownSampleP300 =  []
    for cmd in range(cmdCount):
        cycleData = []
        for cycle in range(cycles):
            channelData = []
            for channel in range(channels):
                volts = channelDataBP[channel][cmdIdx[cmd][cycle]+paddingSlot:(cmdIdx[cmd][cycle] + slotSize-paddingSlot)]
                # reduce dimensions from 80 samples to 20 samples
                channelData.append(resample(volts, 20))
                if(cmd == 0 and channel == 0 and cycle == 1):
                    plt.figure(channel + 20)
                    plt.title("filterd Data - Channel " + str(channel)+" cmd "+str(commands[cmd])+" cycle"+str(cycle))
                    plt.plot(channelData[channel], color='g')

            cycleData.append(channelData)
        dataDownSampleP300.append(cycleData)

    print("\n-- Command Data (Downsampled) ---")
    print("len(dataDownSampleP300) aka 5 cmds: " + str(len(dataDownSampleP300)))
    print("len(dataDownSampleP300[0]) aka 3 cycles : " + str(len(dataDownSampleP300[0])))
    print("len(dataDownSampleP300[0][0]) aka 8 channels : " + str(len(dataDownSampleP300[0][0])))
    print("len(dataDownSampleP300[0][0][0]) aka 20 volts : " + str(len(dataDownSampleP300[0][0][0])))

    ## SPLIT BASELINE IN COMMAND EPOCHES
    start = 0
    downSampleBaseline = []
    while(start < len(baselineDataBP[0])-80):
        channelData = []
        for channel in range(channels):
            volts = baselineDataBP[channel][start:start + 80]
            # reduce dimensions from 80 samples to 20 samples
            channelData.append(resample(volts, 20))
        downSampleBaseline.append(channelData)
        start += 80

    print("\n-- Baseline Data (Downsampled) ---")
    print("len(downSampleBaseline[0]) aka 1000 / 80 = 12 : " + str(len(downSampleBaseline)))
    print("len(downSampleBaseline[0][0]) aka 8 channels : " + str(len(downSampleBaseline[0])))
    print("len(downSampleBaseline[0][0][0]) aka 20 volts : " + str(len(downSampleBaseline[0][0])))

    plt.show()
    return dataDownSampleP300, downSampleBaseline


def extractFeature(dataDownSample, filterdBaseline, targetCmd):
    cmdCount = len(dataDownSample)
    cycles = len(dataDownSample[0])

    ## Reshape Data
    reshapedData =  [[],[],[],[],[]]
    for cmd in range(cmdCount):

        cmdData = np.array(dataDownSample[cmd])
        cycle, nx, ny = cmdData.shape
        reshapedData[cmd] = cmdData.reshape((cycle, nx * ny))
        # reshapedData[cmd].append(cycleData.reshape((nx * ny)))

    print("\n-- Reshaped Data ---")
    print("len(reshapedData) aka 5 cmds: " + str(len(reshapedData)))
    print("len(reshapedData[0]) aka 3 cycles : " + str(len(reshapedData[0])))
    print("len(reshapedData[0][0]) aka 8 channels and 20 samples : " + str(len(reshapedData[0][0])))

    ## Reshape Baseline
    baselineData = np.array(filterdBaseline)
    cycle, nx, ny = baselineData.shape
    reshapedBaselineData = baselineData.reshape((cycle, nx * ny))

    print("\n-- Reshaped Baseline ---")
    print("len(reshapedBaselineData) aka 1000 / 80 = 12 : " + str(len(reshapedBaselineData)))
    print("len(reshapedBaselineData[0]) aka 8 channels and 20 samples : " + str(len(reshapedBaselineData[0])))

    ## Create X and Y data for SVM training
    X = []
    y = []
    print(targetCmd)
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            X.append(reshapedData[cmd][cycle])
            if(cmd == targetCmd): #if cmd is traget command set y = 1
                y.append(1)
            else:
                y.append(0)

    print("\n-- X and Y Data ---")
    print("len(X) cycles x cmd = 3 * 5 = 15 : " + str(len(X)))
    print("y : " + str(y))


    for i in range(len(reshapedBaselineData)):
        X.append(reshapedBaselineData[i])
        y.append(0)

    print("\n-- X and Y Data with Baseline Data ---")
    print("len(X) data epoches + baseline epoches 15 + 12 = 27 : " + str(len(X)))
    print("y : " + str(y))
    return X, y

def trainData(dataP300, blP300):
    # create label y
    z = np.zeros(32)  # 0 = non-target for blP300
    o = np.ones(24)  # 1 = target for dataP300target
    y = np.concatenate((o, z))
    print(y)
    #clf = svm.SVC()    // global above main
    clf.fit(trainData, y)


def predict(sampleslot):
    # test predictions
    resultTarget = clf.predict(sampleslot)
    print(resultTarget)



def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

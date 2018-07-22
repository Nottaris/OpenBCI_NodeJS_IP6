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
    # with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410890_1_baseline.json') as f:
    #     baseline = json.load(f)
    # with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410878_1_volts.json') as f:
    #     volts = json.load(f)
    # with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080410893_1_cmdIdx.json') as f:
    #     cmdIdx = json.load(f)


    #    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080418380_2_baseline.json') as f:
    #        baseline = json.load(f)
    #    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080418368_2_volts.json') as f:
    #        volts = json.load(f)
    #    with open('../../../data/p300/ex5_2_cycles3_trainingdata/1532080418385_2_cmdIdx.json') as f:
    #        cmdIdx = json.load(f)
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
    print("------ Traing Data ------")
    ## Training Target
    targetCmd = 0 # Playpause

    ## 1. Filter and Downsample Traingsdata
    filterdTraindata = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels)

    ##  2. Extract Features for Traingsdata
    featuresTraining = extractFeature(filterdTraindata, targetCmd)

    ##  3. Train Model with features


    ## EXTRACT FEATURES FOR TEST DATA
    print("------ Test Data ------")
    ## 1. Filter and Downsample Testdata

    filterdTestdata = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels)

    ##  2. Extract Features from Testdata
    featuresTraining = extractFeature(filterdTestdata, None)

   ##  3. Compare with Model



def filterDownsampleData(volts, baseline, cmdIdx, channels):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 12.0
    order = 4
    cmdCount = len(cmdIdx)
    slotSize = 120
    baselineLength = len(baseline[0])
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
        baselineDataBP.append(
            dataFilterd[int(len(baseline[:, channel]) / 4):int(3 * (len(baseline[:, channel]) / 4))]
        )  # middle half (500 samples)

        # Plot filterd baseline
        # plt.figure(channel + 20)
        # plt.title("filterd Baseline - Channel " + str(channel))
        # plt.plot(baselineDataBP[channel], color='g')
        # plt.show()

    ## SPLIT VOLTS DATA IN COMMAND EPOCHES
    ## collect volt for each cmd in dataP300[CMD][CYCLE][CHANNEL][VOLTS] of all cycles
    paddingSlot = 20 # remove first and last 20 samples from slots
    dataP300 =  []
    for cmd in range(cmdCount):
        cycleData = []
        for cycle in range(cycles):
            channelData = []
            for channel in range(channels):
                channelData.append(channelDataBP[channel][cmdIdx[cmd][cycle]+paddingSlot:(cmdIdx[cmd][cycle] + slotSize-paddingSlot)])
                if(cmd == 0 and channel == 0 and cycle == 1):
                    plt.figure(channel + 20)
                    plt.title("filterd Data - Channel " + str(channel)+" cmd "+str(commands[cmd])+" cycle"+str(cycle))
                    plt.plot(channelData[channel], color='g')

            cycleData.append(channelData)
        dataP300.append(cycleData)

    print("-- Command Data ---")
    print("len(dataP300) aka 5 cmds: " + str(len(dataP300)))
    print("len(dataP300[0]) aka 3 cycles : " + str(len(dataP300[0])))
    print("len(dataP300[0][0]) aka 8 channels : " + str(len(dataP300[0][0])))
    print("len(dataP300[0][0][0]) aka 80 volts : " + str(len(dataP300[0][0][0])))

    ## Downsample
    # reduce dimensions from 80 samples to 20 samples
    dataDownSampleP300 = dataP300
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            for channel in range(channels):
                dataDownSampleP300[cmd][cycle][channel] = resample(dataP300[cmd][cycle][channel], 20)
                if (cmd == 0 and channel == 0 and cycle == 1):
                    plt.figure(channel + 30)
                    plt.title(
                        "filterd Downsampled Data - Channel " + str(channel) + " cmd " + str(commands[cmd]) + " cycle" + str(cycle))
                    plt.plot(dataDownSampleP300[cmd][cycle][channel], color='b')
    print("-- Downsampled Command Data ---")
    print("len(dataDownSampleP300) aka 5 cmds: " + str(len(dataDownSampleP300)))
    print("len(dataDownSampleP300[0]) aka 3 cycles : " + str(len(dataDownSampleP300[0])))
    print("len(dataDownSampleP300[0][0]) aka 8 channels : " + str(len(dataDownSampleP300[0][0])))
    print("len(dataDownSampleP300[0][0][0]) aka 80 volts : " + str(len(dataDownSampleP300[0][0][0])))

    plt.show()
    return dataDownSampleP300


def extractFeature(dataDownSample, targetCmd):
    cmdCount = len(dataDownSample)
    cycles = len(dataDownSample[0])

    # ## Split Data into target and non-target Data
    # target = []
    # nonTarget = []
    #
    # for cmd in range(len(dataDownSample)):
    #     if(cmd == targetCmd):
    #         target.append([dataDownSample[cmd]])
    #     else:
    #         nonTarget.append(dataDownSample[cmd])
    # print(len(target))
    # print(len(nonTarget))


    ## Reshape Data
    reshapedData =  [[],[],[],[],[]]
    for cmd in range(cmdCount):

        cmdData = np.array(dataDownSample[cmd])
        print(cmdData.shape)
        cycle, nx, ny = cmdData.shape
        reshapedData[cmd] = cmdData.reshape((cycle, nx * ny))
        # reshapedData[cmd].append(cycleData.reshape((nx * ny)))
        print(len(reshapedData[cmd]))

    print("-- Reshaped Data ---")
    print("len(reshapedData) aka 5 cmds: " + str(len(reshapedData)))
    print("len(reshapedData[0]) aka 3 cycles : " + str(len(reshapedData[0])))
    print("len(reshapedData[0][0]) aka 8 channels and 20 samples : " + str(len(reshapedData[0][0])))

    ## Create X and Y data for SVM training
    X = []
    y = []
    print(targetCmd)
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            X.append(reshapedData[cmd][cycle])
            if(cmd == targetCmd):
                y.append(1)
            else:
                y.append(0)

    print("-- X and Y Data ---")
    print("len(X) cycles x cmd = 3 * 5 : " + str(len(X)))
    print("y : " + str(y))
    # baseline blP300 is non-target
    # dataP300 cmd playpause index=2 is target
    # dataP300target = dataP300[2]
    # print(dataP300target.shape)
    # print(blP300.shape)
    # trainData = np.concatenate((dataP300target, blP300))
    # nx, ny = trainData.shape
    # print(nx)
    # print(ny)

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

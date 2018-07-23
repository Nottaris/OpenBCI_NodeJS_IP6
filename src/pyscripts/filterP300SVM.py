import pickle
from scipy.signal import butter, lfilter, decimate, resample
import json, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics

# enable/disable debug Mode
debug = False
substractBaseline = False

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
    # Load SVM Model
    with open('data/p300/model/svm_model.txt', 'rb') as e:
        clf = pickle.load(e)

     # get data as an array from read_in()
    datainput = json.loads(sys.stdin.read())
    cmdIdx = datainput['cmdIdx']
    volts = datainput['volts']
    baseline = datainput['baseline']

    # create a numpy array
    volts = np.array(volts, dtype='f')
    baseline = np.array(baseline, dtype='f')

    # active channels
    channels = [0,1,2,3,4,5,6,7]  # 0-7 channels

    if(debug):
        print("\n------ Filter and Downsample Data ------")
    ## 1. Filter and Downsample Traingsdata
    dataDownSampleP300 = filterDownsampleData(volts, baseline, cmdIdx, channels)

    if (debug):
       print("\n------ Create Features ------")
    ## 2. Extract Features
    X_test = extractFeature(dataDownSampleP300)

    ##  3. Compare Data with model
    if (debug):
        print("\n------ Model Accuracy ------")
    y_pred =  np.array(clf.predict(X_test)) #Predict the response for dataset
    # print("predicted y "+str(y_pred))

    ##  4. Get Command with most p300
    if(np.any(y_pred == 1)):
        cmdP300 = np.zeros(len(cmdIdx))
        cmdCount = len(cmdIdx)

        for y in range(len(y_pred)):
            if(y_pred[y] == 1):
                # increment cmd counter if classified as p300
                cmdP300[int(y/cmdCount)] += 1

        # print(cmdP300)
        # return cmd idx with most found p300 classifications
        print(np.argmax(cmdP300))
    else:
        print("nop")


def filterDownsampleData(volts, baseline, cmdIdx, channels):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 12.0
    order = 4
    cmdCount = len(cmdIdx)
    slotSize = 120
    downsampleSize = 16
    cycles = len(cmdIdx[0])
    channels = len(channels)

    ## BP FILTER DATA
    channelDataBP = []
    baselineDataBP = []
    for channel in range(channels):
        # add baseline before filter BP
        dataWithBaseline = np.concatenate([baseline[:, channel], volts[:, channel]])
        dataFilterd = filterData(dataWithBaseline, lowcut, highcut, fs, order)
        # cut off baseline again
        channelDataBP.append(dataFilterd[len(baseline[:, channel])-1:])

    ## SPLIT VOLTS DATA IN COMMAND EPOCHES AND DOWNSAMPLE
    ## collect volt for each cmd in dataP300[CMD][CYCLE][CHANNEL][VOLTS] of all cycles
    paddingSlot = 0 # remove first and last 30 samples from each slot to 30 - 90 (120ms - 360ms)
    dataDownSampleP300 =  []
    for cmd in range(cmdCount):
        cycleData = []
        for cycle in range(cycles):
            channelData = []
            for channel in range(channels):
                if (substractBaseline):
                #   # Substract Baseline mean
                    mean = np.mean(channelDataBP[channel][cmdIdx[cmd][cycle]+paddingSlot:(cmdIdx[cmd][cycle] + slotSize-paddingSlot)])
                    volts = channelDataBP[channel][cmdIdx[cmd][cycle]+paddingSlot:(cmdIdx[cmd][cycle] + slotSize-paddingSlot)]-mean
                else:
                    volts = channelDataBP[channel][cmdIdx[cmd][cycle] + paddingSlot:(cmdIdx[cmd][cycle] + slotSize - paddingSlot)]
                # Downsample: reduce dimensions from 80 samples to 20 samples
                channelData.append(resample(volts, downsampleSize))
            median = np.median(channelData, axis=0)
            cycleData.append(median)
        dataDownSampleP300.append(cycleData)
    if(debug):
        print("\n-- Data (Downsampled) ---")
        print("len(dataDownSampleP300) aka 5 cmds: " + str(len(dataDownSampleP300)))
        print("len(dataDownSampleP300[0]) aka 3 cycles : " + str(len(dataDownSampleP300[0])))
        print("len(dataDownSampleP300[0][0]) aka "+str(downsampleSize)+" volts : " + str(len(dataDownSampleP300[0][0])))

    return dataDownSampleP300

def extractFeature(dataDownSample):
    cmdCount = len(dataDownSample)
    cycles = len(dataDownSample[0])

    ## Create X to compare with  SVM model
    X = []
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            X.append(dataDownSample[cmd][cycle])
    if (debug):
        print("\n-- X Data ---")
        print("len(X) cycles x cmd = "+str(cycles)+" * "+(str(cmdCount))+" = "+str(cycles*cmdCount)+" : " + str(len(X)))

    X = preprocessing.scale(X)
    return X

def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData



# start process
if __name__ == '__main__':
    main()

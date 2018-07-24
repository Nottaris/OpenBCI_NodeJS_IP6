from typing import List, Any

from scipy.signal import butter, lfilter, decimate, resample
import json, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB


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

# enable/disable debug Mode
debug = False
substractBaseline = False

def main():
    with open('../../../data/p300/ex7_1_cycles5/training/1532349861282_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../../data/p300/ex7_1_cycles5/training/1532349861273_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../../data/p300/ex7_1_cycles5/training/1532349861307_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    with open('../../../data/p300/ex7_1_cycles5/test/1532350012450_1_baseline.json') as f:
        baselineTest= json.load(f)
    with open('../../../data/p300/ex7_1_cycles5/test/1532350012442_1_volts.json') as f:
        voltsTest = json.load(f)
    with open('../../../data/p300/ex7_1_cycles5/test/1532350012477_1_cmdIdx.json') as f:
        cmdIdxTest = json.load(f)

    # create a numpy array
    voltsTest = np.array(voltsTest, dtype='f')
    baselineTest = np.array(baselineTest, dtype='f')

    # active channels
    channels = [0,1,2,3,4,5,6,7]  # 0-7 channels

    print("\n------ Traing Data ------")

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels)

    ##  2. Extract Features for Traingsdata
    targetCmd = 0 # Training Target: Playpause
    [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)
    print("Features: "+str(len(X)))
    print("y: " + str(y))

    ##  3. Train Model with features

    # gamma: defines how far the influence of a single training example reaches, with low values meaning ‘far’ and high values meaning ‘close’.
    # C: trades off misclassification of training examples against simplicity of the decision surface.
    #    A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly by giving the model freedom to select more samples as support vectors.
    # Find optimal gamma and C parameters: http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
    # ToDo: Set correct SVM params
    #[C, gamma] = findTrainClassifier(X,y)
    #clf = svm.SVC(kernel='rbf', gamma=gamma, C=C)
    # clf = svm.SVC(kernel='linear',  C=10.0)

    #clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto', priors=None, n_components=2, store_covariance=False)  # lda

    #clf = KNeighborsClassifier(n_neighbors=5, weights='distance', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=-1)

    clf = GaussianNB()
    clf.fit(X, y)

    ##  Check if traingdata get 100% accuracy
    [accuracy, precision, recall] = modelAccuracy(y, clf.predict(X))
    print(clf.predict(X))
    print("Training Accuracy: " + str(accuracy))
    print("Training Precision: " + str(precision))
    print("Training Recall: " + str(recall))
    # if(accuracy ==1.0):
    #     print("Correct classification with traingdata")
    # else:
    #     print("Wrong classification with traingdata. check SVM algorithm")


    print("\n------ Test Data ------")
    ## 4. Filter and Downsample Testdata
    [filterdTestdata, filterdTestBaseline] = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels)

    ##  5. Extract Features from Testdata
    targetCmd = 0  # Playpause
    [X_test, y_test] = extractFeature(filterdTestdata, filterdTestBaseline, targetCmd)
    print("Features X_Test: "+str(len(X_test)))
    print("y_Test: " + str(y_test))

    ##  6. Check Model Accuracy
    print("\n------ Model Accuracy ------")
    y_pred =  clf.predict(X_test) #Predict the response for test dataset
    print("predicted y "+str(y_pred))

    [accuracy, precision, recall] = modelAccuracy(y_test, y_pred)
    print("Accuracy: "+str(accuracy))
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))


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
        baselineDataBP.append(dataFilterd[1000:len(baseline)])# baseline is 9000 samples
        plt.figure(channel + 1)
        plt.title("filterd Data - Channel " + str(channel))
        plt.plot(baselineDataBP[channel]*1000000, color='g')
        plt.figure(channel + 2)
        plt.plot(channelDataBP[channel] * 1000000, color='r')
        plt.title("Baseline Data - Channel " + str(channel))


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
                if(cmd == 0):
                    plt.figure(cycle + 1)
                    plt.plot(channelData[channel] * 1000000, color='r')
                    plt.title("Playpause Data - Channel 0 - Cycle " + str(cycle))
                    axes = plt.gca()
                    axes.set_ylim([-25, 25])

            median = np.median(channelData, axis=0)
            cycleData.append(median)
            if (cmd == 0):
                avg = np.average(cycleData[cycle], axis=0)
                plt.figure(cycle + 1)
                plt.plot(avg * 1000000, label="Avg Channels", color='b')
                plt.title("Playpause AVG Data - All Channel - Cycle " + str(cycle))
                plt.figure(cycle + 1)
                plt.plot(median * 1000000, label="Median Channels", color='g')
                plt.legend(loc='lower right')

        dataDownSampleP300.append(cycleData)
    if(debug):
        print("\n-- Command Data (Downsampled) ---")
        print("len(dataDownSampleP300) aka 5 cmds: " + str(len(dataDownSampleP300)))
        print("len(dataDownSampleP300[0]) aka 3 cycles : " + str(len(dataDownSampleP300[0])))
        print("len(dataDownSampleP300[0][0]) aka 20 volts : " + str(len(dataDownSampleP300[0][0])))

    if (debug):
        plt.show()

    ## SPLIT BASELINE IN COMMAND EPOCHES AND DOWNSAMPLE
    start = 0
    downSampleBaseline = []
    while(start < len(baselineDataBP[0])-80):
        channelData = []
        for channel in range(channels):
            if (substractBaseline):
                ## SUBTRACT BASELINE MEAN
                mean = np.mean(baselineDataBP[channel][start:start + 80])
                volts = baselineDataBP[channel][start:start + 80]-mean
            else:
                volts = baselineDataBP[channel][start:start + 80]
            # Downsample: reduce dimensions from 80 samples to 20 samples
            channelData.append(resample(volts, downsampleSize))
        median = np.median(channelData, axis=0)
        downSampleBaseline.append(median)
        start += 80

    if(debug):
        print("\n-- Baseline Data (Downsampled) ---")
        print("len(downSampleBaseline[0]) : " + str(len(downSampleBaseline)))
        print("len(downSampleBaseline[0][0]) aka 20 volts : " + str(len(downSampleBaseline[0])))

    return dataDownSampleP300, downSampleBaseline


def extractFeature(dataDownSample, filterdBaseline, targetCmd):
    cmdCount = len(dataDownSample)
    cycles = len(dataDownSample[0])

    ## Create X and Y data for SVM training
    X = []
    y = []
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            X.append(dataDownSample[cmd][cycle])
            if cmd == targetCmd: #if cmd is traget command set y = 1
                y.append(1)
            else:
                y.append(0)
    if (debug):
        print("\n-- X and Y Data ---")
        print("len(X) cycles x cmd = "+str(cycles)+" * "+(str(cmdCount))+" = "+str(cycles*cmdCount)+" : " + str(len(X)))
        print("y : " + str(y))

    for i in range(len(filterdBaseline)):
        X.append(filterdBaseline[i])
        y.append(0)
    if (debug):
        print("\n-- X and Y Data with Baseline Data ---")
        print("len(X) data epoches + baseline epoches : " + str(len(X)))

    ## Feature Standardization
    X = preprocessing.scale(X)

    return X, y


def modelAccuracy(y_test, y_pred):
    # Model Accuracy: how often is the classifier correct
    accuracy = metrics.accuracy_score(y_test, y_pred)

    # Model Precision: what percentage of positive tuples are labeled as such?
    precision = metrics.precision_score(y_test, y_pred)

    # Model Recall: what percentage of positive tuples are labelled as such?
    recall =  metrics.recall_score(y_test, y_pred)

    return[accuracy,precision,recall]

def findTrainClassifier(X,y):
    C_range = np.logspace(-2, 10, 13)
    gamma_range = np.logspace(-9, 3, 13)
    param_grid = dict(gamma=gamma_range, C=C_range)
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
    grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv)
    grid.fit(X, y)
    print("The best parameters are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))
    return grid.best_params_['C'], grid.best_params_['gamma']

def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

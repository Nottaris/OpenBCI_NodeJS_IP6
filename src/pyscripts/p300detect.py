##
# create Features form live data and compare them with trained SVM Model
##

import json
import numpy as np
import pickle
import sys

from p300Functions import filterDownsampleData
from sklearn import preprocessing

# enable/disable debug Mode
debug = False
avgChannel = False

def main():
    # Load SVM Model
    if(avgChannel):
        with open('data/p300/model/svm_model_avg.txt', 'rb') as e:
            clf = pickle.load(e)
    else:
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
    [dataDownSampleP300, dataBaseline] = filterDownsampleData(volts, baseline, cmdIdx, channels, debug, 0)

    if (debug):
       print("\n------ Create Features ------")

    ## 2. Extract Features
    X_test = extractXFeature(dataDownSampleP300)

    ##  3. Compare Data with model
    if (debug):
        print("\n------ Model Accuracy ------")

    y_pred =  np.array(clf.predict(X_test)) #Predict the response for dataset

    #  4. Get Command with most p300
    if(np.any(y_pred == 1)):
        cmdP300 = np.zeros(len(cmdIdx))
        cmdCount = len(cmdIdx)

        for y in range(len(y_pred)):
            if(y_pred[y] == 1):
                # increment cmd counter if classified as p300
                cmdP300[int(y/cmdCount)] += 1

        # return cmd idx with most found p300 classifications
        maxIdx = np.argmax(cmdP300)
        if(cmdP300[maxIdx]>1):
            print(np.argmax(cmdP300))
        else:
            print("nop")
    else:
        print("nop")

def extractXFeature(dataDownSample):
    if(avgChannel == False):
        cmdCount = len(dataDownSample)
        cycles = len(dataDownSample[0])

        ## Reshape Data
        reshapedData =  [[],[],[],[],[]]
        for cmd in range(cmdCount):
            cmdData = np.array(dataDownSample[cmd])
            cycle, nx, ny = cmdData.shape
            reshapedData[cmd] = cmdData.reshape((cycle, nx * ny))
            # reshapedData[cmd].append(cycleData.reshape((nx * ny)))
        if (debug):
            print("\n-- Reshaped Data ---")
            print("len(reshapedData) aka 5 cmds: " + str(len(reshapedData)))
            print("len(reshapedData[0]) aka 3 cycles : " + str(len(reshapedData[0])))
            print("len(reshapedData[0][0]) aka 8 channels and 20 samples : " + str(len(reshapedData[0][0])))
    else:
        cmdCount = len(dataDownSample)
        cycles = len(dataDownSample[0])

        ## Reshape Data
        reshapedData = [[], [], [], [], []]
        for cmd in range(cmdCount):
            for cycle in range(cycles):
                median = np.median(dataDownSample[cmd][cycle], axis=0)
                reshapedData[cmd].append(median)

        if (debug):
            print("\n-- Reshaped Data ---")
            print("len(reshapedData) aka 5 cmds: " + str(len(reshapedData)))
            print("len(reshapedData[0]) aka 3 cycles : " + str(len(reshapedData[0])))
            print("len(reshapedData[0][0]) aka 8 channels and 20 samples : " + str(len(reshapedData[0][0])))

    ## Create X data for SVM training
    X = []

    for cmd in range(cmdCount):
        for cycle in range(cycles):
            X.append(reshapedData[cmd][cycle])

    if (debug):
        print("\n-- X and Y Data ---")
        print("len(X) cycles x cmd = "+str(cycles)+" * "+(str(cmdCount))+" = "+str(cycles*cmdCount)+" : " + str(len(X)))

    ## Feature Standardization
    X = preprocessing.scale(X)

    return X

# start process
if __name__ == '__main__':
    main()

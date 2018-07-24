import pickle
from scipy.signal import butter, lfilter, decimate, resample
import json, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
from p300Functions import filterDownsampleData

# enable/disable debug Mode
debug = False

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
    [dataDownSampleP300, dataBaseline] = filterDownsampleData(volts, baseline, cmdIdx, channels, debug)

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


# start process
if __name__ == '__main__':
    main()

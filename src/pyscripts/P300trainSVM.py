##
# Train SVM Model with given Command samples and baseline data and compare it with testdata
##

import codecs
import json
import pickle

import numpy as np
from p300Functions import filterDownsampleData
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit

debug = False            # enable/disable debug Mode
useSavedFeatures = False # use local stored features
avgChannel = False       # avg all channel in Feature

def main():
    channels = [0,1,2,3,4,5,6,7]  # set active channels 0-7 channels

    print("\n------ Traing Data ------")

    if (useSavedFeatures):

        ## 1. Load saved Features
        # load target features
        file_path = '../../data/p300/model/X_target.json'
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        targetData = json.loads(obj_text)
        print("Target Features: " + str(len(targetData)))

        # load non-target features
        file_path = '../../data/p300/model/X_nontarget.json'
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        b_new = json.loads(obj_text)
        baseline = np.array(b_new)
        print("Non Target Features: " + str(len(baseline)))

        ##  2. Extract Features for Traingsdata
        [X,y] = extractFeatureWithoutCycles(targetData, baseline)
        print("Total Features: " + str(len(X)))
        print(y)

    else:
        # Load stored command stamples and baseline data
        with open('../../data/p300/ex4_5_cycles5/training/1532349861282_1_baseline.json') as f:
            baselineTraining = json.load(f)
        with open('../../data/p300/ex4_5_cycles5/training/1532349861273_1_volts.json') as f:
            voltsTraining = json.load(f)
        with open('../../data/p300/ex4_5_cycles5/training/1532349861307_1_cmdIdx.json') as f:
            cmdIdxTraining = json.load(f)

        # create a numpy array
        voltsTraining = np.array(voltsTraining, dtype='f')
        baselineTraining = np.array(baselineTraining, dtype='f')

        ## 1. Filter and Downsample Traingsdata
        [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug)

        ##  2. Extract Features for Traingsdata
        targetCmd = 0  # Training Target: Playpause
        [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)


    ##  3. Train Model with features

    # ToDo: Set correct SVM params
    # gamma: defines how far the influence of a single training example reaches, with low values meaning ‘far’ and high values meaning ‘close’.
    # C: trades off misclassification of training examples against simplicity of the decision surface.  A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly by giving the model freedom to select more samples as support vectors.
    # [C, gamma] = findTrainClassifier(X,y)
    # clf = svm.SVC(kernel='rbf', gamma=gamma, C=C)

    clf = svm.SVC(kernel='linear', C = 1.0)

    clf.fit(X,y)

    ##  Check if traingdata get 100% accuracy
    [accuracy,_,_] = modelAccuracy(y,  clf.predict(X))
    if(accuracy ==1.0):
        print("Correct classification with traingdata")
    else:
        print("Wrong classification with traingdata. check SVM algorithm")

    print("\n------ Test Data ------")
    with open('../../data/p300/ex4_5_cycles5/test/1532350012450_1_baseline.json') as f:
        baselineTest= json.load(f)
    with open('../../data/p300/ex4_5_cycles5/test/1532350012442_1_volts.json') as f:
        voltsTest = json.load(f)
    with open('../../data/p300/ex4_5_cycles5/test/1532350012477_1_cmdIdx.json') as f:
        cmdIdxTest = json.load(f)

    targetCmd = 0  # Training Target: Playpause

    # create a numpy array
    voltsTest = np.array(voltsTest, dtype='f')
    baselineTest = np.array(baselineTest, dtype='f')

    ## 4. Filter and Downsample Testdata
    [filterdTestdata, filterdTestBaseline] = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels, debug)

    ##  5. Extract Features from Testdata
    targetCmd = 0  # Playpause
    [X_test, y_test] = extractFeature(filterdTestdata, filterdTestBaseline, targetCmd)
    print("Anz. Features X_Test: "+str(len(X_test)))
    print("y_Test: " + str(y_test))


    ##  6. Check Model Accuracy
    print("\n------ Model Accuracy ------")
    y_pred =  clf.predict(X_test) #Predict the response for test dataset
    print("predicted y "+str(y_pred))

    [accuracy, precision, recall] = modelAccuracy(y_test, y_pred)
    print("Accuracy: "+str(accuracy))
    print("Precision: " + str(precision))
    print("Recall: " + str(recall))

    ## 7. save model
    if(avgChannel):
        with open('../../data/p300/model/svm_model_avg.txt', 'wb') as outfile:
           pickle.dump(clf, outfile)
        print("saved model: svm_model_avg.txt")
    else:
        with open('../../data/p300/model/svm_model.txt', 'wb') as outfile:
           pickle.dump(clf, outfile)
        print("saved model: svm_model.txt")

def extractFeature(dataDownSample, filterdBaseline, targetCmd):
    reshapedBaselineData = []
    if(avgChannel == False):
        cmdCount = len(dataDownSample)
        cycles = len(dataDownSample[0])

        ## Reshape Data
        reshapedData =  [[],[],[],[],[]]
        for cmd in range(cmdCount):
            cmdData = np.array(dataDownSample[cmd])
            cycle, nx, ny = cmdData.shape
            reshapedData[cmd] = cmdData.reshape((cycle, nx * ny))

        if (debug):
            print("\n-- Reshaped Data ---")
            print("len(reshapedData) aka 5 cmds: " + str(len(reshapedData)))
            print("len(reshapedData[0]) aka 3 cycles : " + str(len(reshapedData[0])))
            print("len(reshapedData[0][0]) aka 8 channels and 20 samples : " + str(len(reshapedData[0][0])))

        ## Reshape Baseline
        baselineData = np.array(filterdBaseline)
        cycle, nx, ny = baselineData.shape
        reshapedBaselineData = baselineData.reshape((cycle, nx * ny))

        if (debug):
            print("\n-- Reshaped Baseline ---")
            print("len(reshapedBaselineData): " + str(len(reshapedBaselineData)))
            print("len(reshapedBaselineData[0]) aka 8 channels and 20 samples : " + str(len(reshapedBaselineData[0])))
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

        ## Reshape Baseline
        for i in range(len(filterdBaseline)):
            median = np.median(filterdBaseline[i], axis=0)
            reshapedBaselineData.append(median)

        if (debug):
            print("\n-- Reshaped Baseline ---")
            print("len(reshapedBaselineData): " + str(len(reshapedBaselineData)))
            print("len(reshapedBaselineData[0]) aka 8 channels and 20 samples : " + str(len(reshapedBaselineData[0])))

    ## Create X and Y data for SVM training
    X = []
    y = []
    for cmd in range(cmdCount):
        for cycle in range(cycles):
            X.append(reshapedData[cmd][cycle])
            if cmd == targetCmd: #if cmd is traget command set y = 1
                y.append(1)
            else:
                y.append(0)
    if (debug):
        print("\n-- X and Y Data ---")
        print("len(X) cycles x cmd = "+str(cycles)+" * "+(str(cmdCount))+" = "+str(cycles*cmdCount)+" : " + str(len(X)))
        print("y : " + str(y))

    for i in range(len(reshapedBaselineData)):
        X.append(reshapedBaselineData[i])
        y.append(0)
    if (debug):
        print("\n-- X and Y Data with Baseline Data ---")
        print("len(X) data epoches + baseline epoches : " + str(len(X)))

    ## Feature Standardization
    X = preprocessing.scale(X)

    return X, y


def extractFeatureWithoutCycles(filterdData, filterdBaseline):
    reshapedTargetData = []
    reshapedBaselineData = []

    if(avgChannel == False):
        ## Reshape Data
        targetData = np.array(filterdData)
        cycle, nx, ny = targetData.shape
        reshapedTargetData = targetData.reshape((cycle, nx * ny))

        if (debug):
            print("\n-- Reshaped Data ---")
            print("len(reshapedData) aka 16 Features cmds: " + str(len(reshapedTargetData)))
            print("len(reshapedData[0][0]) aka 8 channels and 16 samples : " + str(len(reshapedTargetData[0])))

        ## Reshape Baseline
        baselineData = np.array(filterdBaseline)
        cycle, nx, ny = baselineData.shape
        reshapedBaselineData = baselineData.reshape((cycle, nx * ny))

        if (debug):
            print("\n-- Reshaped Baseline ---")
            print("len(reshapedBaselineData): " + str(len(reshapedBaselineData)))
            print("len(reshapedBaselineData[0]) aka 8 channels and 20 samples : " + str(len(reshapedBaselineData[0])))
    else:
        # Avg all Channel Data for each slot
        for i in range(len(filterdData)):
            median = np.median(filterdData[i], axis=0)
            reshapedTargetData.append(median)


        for i in range(len(filterdBaseline)):
            median = np.median(filterdBaseline[i], axis=0)
            reshapedBaselineData.append(median)

    ## Create X and Y data for SVM training
    X = []
    y = []
    for i in range(len(reshapedTargetData)):
            X.append(reshapedTargetData[i])
            y.append(1)

    for i in range(len(reshapedBaselineData)):
        X.append(reshapedBaselineData[i])
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

# Find optimal gamma and C parameters Source: http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
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

# start process
if __name__ == '__main__':
    main()

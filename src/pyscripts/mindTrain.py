import json
import os
import sys
import time
import pickle
import numpy as np
from mindFunctions import filterDownsampleData
from scipy.signal import butter, lfilter
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit


# enable/disable debug Mode
debug = False

# the 5 commands from player
commands = ['volup', 'playpause','next','prev','voldown']
cmdCount = len(commands)  # nr of commands



def main():
    # read training data from files
    # filepath-example = 'your project path'/data/mind/training-playpause.json'
    traindata = []

    for cmd in range (cmdCount):
        filepath = '../../data/mind/training-'+commands[cmd]+'.json'
        # read file of trainingCmd
        with open(filepath) as f:
            data = json.load(f)
        traindata.append(np.array(data, dtype='f'))


    # read in baseline from file
    # TODO: generate baseline in training phase
    baseline = []
    blfilepath = '../../data/mind/training-baseline.json'
    blpath = blfilepath.replace('"', '')
    # read file of baseline
    with open(blpath) as blf:
        bl = json.load(blf)
    baseline = np.array(bl, dtype='f')


    # TODO: generate testdata from live session (current ones are fake copies)
    ## read in test data
    with open('../../data/mind/test-baseline.json') as f:
        baselineTest = json.load(f)
    with open('../../data/mind/test-volts.json') as f:
        voltsTest = json.load(f)

    # create a numpy array
    voltsTest = np.array(voltsTest, dtype='f')
    baselineTest = np.array(baselineTest, dtype='f')

    if debug: print("\n------ Traing Data ------")
    ## 1. Filter and Downsample Traingsdata
    # bp filter data
    [filterdTraindata,baselineDataBP] = filterDownsampleData(traindata, baseline, commands, debug)

    ##  2. Extract Features for Trainingdata (only commands)
    [X, y] = extractFeature(filterdTraindata)
    print("Anz. Features: " + str(len(X)))
    print("y: " + str(y))
    #
    # ##  3. Train Model with features
    #
    # # gamma: defines how far the influence of a single training example reaches, with low values meaning ‘far’ and high values meaning ‘close’.
    # # C: trades off misclassification of training examples against simplicity of the decision surface.
    # #    A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly by giving the model freedom to select more samples as support vectors.
    # # Find optimal gamma and C parameters: http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
    # # TODO: Set correct SVM params
    # [C, gamma] = findTrainClassifier(X, y)
    # clf = svm.SVC(kernel='rbf', gamma=gamma, C=C)
    # clf.fit(X, y)
    #
    # ## save model
    # with open('../../data/mind/model/svm_model-mind.txt', 'wb') as outfile:
    #     pickle.dump(clf, outfile)
    #
    #
    # ##  Check if trainingdata get 100% accuracy
    # if debug:
    #     [accuracy, _, _] = modelAccuracy(y, clf.predict(X))
    #     if (accuracy == 1.0):
    #         print("Correct classification with traingdata")
    #     else:
    #         print("Wrong classification with traingdata. check SVM algorithm")
    #
    #     print("\n------ Test Data ------")
    #     ## 4. Filter and Downsample Testdata
    #     [filterdTestdata] = filterDownsampleData(voltsTest, yindicies, debug)
    #
    #     ##  5. Extract Features from Testdata
    #     targetCmd = 1  # Playpause===1
    #     [X_test, y_test] = extractFeature(filterdTestdata, targetCmd)
    #     print("Anz. Features X_Test: " + str(len(X_test)))
    #     print("y_Test: " + str(y_test))
    #
    #     ##  6. Check Model Accuracy
    #     print("\n------ Model Accuracy ------")
    #     y_pred = clf.predict(X_test)  # Predict the response for test dataset
    #     if debug: print("predicted y " + str(y_pred))
    #
    #     [accuracy, precision, recall] = modelAccuracy(y_test, y_pred)
    #     print("Accuracy: " + str(accuracy))
    #     print("Precision: " + str(precision))
    #     print("Recall: " + str(recall))
    #
    # # send success back to node
    # # TODO: uncomment / implement success boolean return and
    # # print('true')


def extractFeature(dataFilterd):
    ## Create X and Y data for SVM training
    X = []
    y = []

    # TODO: Extract Features

    # ## Reshape Data
    # reshapedData = []
    # dataFilterdNp = np.array(dataFilterd)
    # trainCmd, nx, ny = dataFilterdNp.shape
    # reshapedData = dataFilterdNp.reshape((trainCmd, nx * ny))
    #
    # # if (debug):
    # print("\n-- Reshaped Data ---")
    # print("len(reshapedData) aka 5 cmds: " + str(len(reshapedData)))
    # print("len(reshapedData[0]) channels*samples aka  8*250  : " + str(len(reshapedData[0])))

    # print(len(dataFilterd))
    # for cmd in range (cmdCount):
    #     X.append(dataFilterd[cmd])
    #     y.append(cmd)
    # if debug:
    #     print("\n-- X and Y Data ---")
    #     print("y : " + str(y))
    # print(X)

    # TODO: Feature Standardization
    ## Feature Standardization
    # X = preprocessing.scale(X)

    return X, y


def extractFeatureTest(dataDownSample, cmd):
    ## Create X and Y data for SVM test
    X = []
    y = []
    print(len(X))
    X.append(dataDownSample)
    y.append(cmd)
    if debug:
        print("\n-- X and Y Data ---")
        print("y : " + str(y))

    ## Feature Standardization
    X = preprocessing.scale(X)

    return X, y


def modelAccuracy(y_test, y_pred):
    # Model Accuracy: how often is the classifier correct
    accuracy = metrics.accuracy_score(y_test, y_pred)

    # Model Precision: what percentage of positive tuples are labeled as such?
    precision = metrics.precision_score(y_test, y_pred)

    # Model Recall: what percentage of positive tuples are labelled as such?
    recall = metrics.recall_score(y_test, y_pred)

    return [accuracy, precision, recall]


def findTrainClassifier(X, y):
    C_range = np.logspace(-2, 10, 13)
    gamma_range = np.logspace(-9, 3, 13)
    param_grid = dict(gamma=gamma_range, C=C_range)
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
    grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv)
    grid.fit(X, y)
    if debug:
        print("The best parameters are %s with a score of %0.2f" % (grid.best_params_, grid.best_score_))
    return grid.best_params_['C'], grid.best_params_['gamma']


# start process
if __name__ == '__main__':
    main()

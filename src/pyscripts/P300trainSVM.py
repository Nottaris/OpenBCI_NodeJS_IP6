from scipy.signal import butter, lfilter, decimate, resample
import json, os, sys, numpy as np, matplotlib.pyplot as plt
from sklearn import svm, preprocessing, metrics
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import GridSearchCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import pickle
from p300Functions import filterDownsampleData
import codecs, json
# enable/disable debug Mode

debug = True
useSavedFeatures = True
avgChannel = False

def main():
    # active channels
    channels = [0,1,2,3,4,5,6,7]  # 0-7 channels

    print("\n------ Traing Data ------")
    with open('../../data/p300/ex6_1_cylces5/training/1532341316088_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../data/p300/ex6_1_cylces5/training/1532341316076_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../data/p300/ex6_1_cylces5/training/1532341316116_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    targetCmd = 0 # Training Target: Playpause

    if (useSavedFeatures == False):
        ## 1. Filter and Downsample Traingsdata

        [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug, targetCmd)

        ##  2. Extract Features for Traingsdata
        [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)

    else:
        file_path = '../../data/p300/model/X_target.json'
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        targetData = json.loads(obj_text)
        print("Target Features: " + str(len(targetData)))

        # for i in range(len(targetData)):
        #     for channel in range(len(targetData[0])):
        #         plt.figure(i + 31)
        #         plt.title("Feature " + str(i) + " - Channel " + str(channel))
        #         plt.plot(targetData[i][channel], color='g')
        # if(debug):
        #     plt.show()

        file_path = '../../data/p300/model/X_nontarget.json'
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        b_new = json.loads(obj_text)
        baseline = np.array(b_new)
        print("Non Target Features: " + str(len(baseline)))

        [X,y] = extractFeatureWithoutCycles(targetData, baseline)
        print("Total Features: " + str(len(X)))
        print(y)

    ##  3. Train Model with features

    # gamma: defines how far the influence of a single training example reaches, with low values meaning ‘far’ and high values meaning ‘close’.
    # C: trades off misclassification of training examples against simplicity of the decision surface.
    #    A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly by giving the model freedom to select more samples as support vectors.
    # Find optimal gamma and C parameters: http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
    # ToDo: Set correct SVM params
    # [C, gamma] = findTrainClassifier(X,y)
    # clf = svm.SVC(kernel='rbf', gamma=gamma, C=C)
    clf = svm.SVC(kernel='linear')
    # clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto', priors=None, n_components=2, store_covariance=False)  # lda

    clf.fit(X,y)

    ##  Check if traingdata get 100% accuracy
    [accuracy,_,_] = modelAccuracy(y,  clf.predict(X))
    if(accuracy ==1.0):
        print("Correct classification with traingdata")
    else:
        print("Wrong classification with traingdata. check SVM algorithm")

    # ## save model
    # with open('../../data/p300/model/svm_model.txt', 'wb') as outfile:
    #     pickle.dump(clf, outfile)

    # save features
    # outfile = '../../data/p300/model/X_training.txt'
    # json.dump(X[0:20].tolist(), codecs.open(outfile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
    #               indent=4)  ### this saves the array in .json format
    # outfile = '../../data/p300/model/X_training_Baseline.txt'
    # json.dump(X[20:len(X)].tolist(), codecs.open(outfile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
    #               indent=4)  ### this saves the array in .json format

    print("\n------ Test Data ------")
    with open('../../data/p300/ex7_1_cycles5/test/1532350012450_1_baseline.json') as f:
        baselineTest= json.load(f)
    with open('../../data/p300/ex7_1_cycles5/test/1532350012442_1_volts.json') as f:
        voltsTest = json.load(f)
    with open('../../data/p300/ex7_1_cycles5/test/1532350012477_1_cmdIdx.json') as f:
        cmdIdxTest = json.load(f)

    # create a numpy array
    voltsTest = np.array(voltsTest, dtype='f')
    baselineTest = np.array(baselineTest, dtype='f')
    ## 4. Filter and Downsample Testdata
    [filterdTestdata, filterdTestBaseline] = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels, debug, targetCmd)

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

    print("\n------ Test Data 2 ------")

    with open('../../data/p300/ex8_cycles5/1532426604595_1_baseline.json') as f:
        baselineTest= json.load(f)
    with open('../../data/p300/ex8_cycles5/1532426604585_1_volts.json') as f:
        voltsTest = json.load(f)
    with open('../../data/p300/ex8_cycles5/1532426604613_1_cmdIdx.json') as f:
        cmdIdxTest = json.load(f)

    # create a numpy array
    voltsTest = np.array(voltsTest, dtype='f')
    baselineTest = np.array(baselineTest, dtype='f')
    ## 4. Filter and Downsample Testdata
    [filterdTestdata, filterdTestBaseline] = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels, debug, targetCmd)

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



def extractFeature(dataDownSample, filterdBaseline, targetCmd):
    reshapedTargetData = []
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
            # reshapedData[cmd].append(cycleData.reshape((nx * ny)))
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

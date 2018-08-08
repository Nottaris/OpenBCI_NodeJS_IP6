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
useSavedFeatures = False

def main():
    # active channels
    channels = [0,1,2,3,4,5,6,7]  # 0-7 channels

    print("\n------ Traing Data ------")
    with open('../../data/p300/ex10_cycles5/1-play/1533644747884_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/1-play/1533644747872_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/1-play/1533644747913_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    targetCmd = 0 # Training Target: Playpause

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug, targetCmd)

    ##  2. Extract Features for Traingsdata
    [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)

    print("\n------ Traing Data Next ------")
    with open('../../data/p300/ex10_cycles5/2-next/1533644916870_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/2-next/1533644916859_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/2-next/1533644916890_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    targetCmd = 1 # Training Target: Next

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug, targetCmd)

    ##  2. Extract Features for Traingsdata
    [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)

    print("\n------ Traing Data VolDown ------")
    with open('../../data/p300/ex10_cycles5/3-prev/1533645116967_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/3-prev/1533645116953_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/3-prev/1533645116988_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    targetCmd = 2 # Training Target: Prev

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug, targetCmd)

    ##  2. Extract Features for Traingsdata
    [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)

    print("\n------ Traing Data ------")
    with open('../../data/p300/ex10_cycles5/4-volup/1533644839857_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/4-volup/1533644839848_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/4-volup/1533644839882_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    targetCmd = 3 # Training Target: VolUp

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug, targetCmd)

    ##  2. Extract Features for Traingsdata
    [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)


    print("\n------ Traing Data ------")
    with open('../../data/p300/ex10_cycles5/5-voldown/1533644995773_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/5-voldown/1533644995766_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../data/p300/ex10_cycles5/5-voldown/1533644995801_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    targetCmd = 4 # Training Target: Next

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug, targetCmd)

    print("\n------ Traing Data ------")
    with open('../../data/p300/ex8_cycles5/1532426604595_1_baseline.json') as f:
        baselineTraining = json.load(f)
    with open('../../data/p300/ex8_cycles5/1532426604585_1_volts.json') as f:
        voltsTraining = json.load(f)
    with open('../../data/p300/ex8_cycles5/1532426604613_1_cmdIdx.json') as f:
        cmdIdxTraining = json.load(f)

    # create a numpy array
    voltsTraining = np.array(voltsTraining, dtype='f')
    baselineTraining = np.array(baselineTraining, dtype='f')

    targetCmd = 0 # Training Target: Next

    ## 1. Filter and Downsample Traingsdata
    [filterdTraindata, filterdBaseline] = filterDownsampleData(voltsTraining, baselineTraining, cmdIdxTraining, channels, debug, targetCmd)

    ##  2. Extract Features for Traingsdata
    [X, y] = extractFeature(filterdTraindata,filterdBaseline, targetCmd)
    if (useSavedFeatures):
        X = []
        y = []
        file_path = '../../data/p300/model/X_training.txt'
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        b_new = json.loads(obj_text)
        X = np.array(b_new)
        print(len(X))
        for i in range(len(X)):
            y.append(1)

        file_path = '../../data/p300/model/X_training_Baseline.txt'
        obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
        b_new = json.loads(obj_text)
        baseline = np.array(b_new)
        X = np.concatenate((X, baseline), axis=0)
        print(len(X))
        for i in range(len(baseline)):
            y.append(0)

    print("Anz. Features: " + str(len(X)))
    print("y: " + str(y))

    ##  3. Train Model with features

    # gamma: defines how far the influence of a single training example reaches, with low values meaning ‘far’ and high values meaning ‘close’.
    # C: trades off misclassification of training examples against simplicity of the decision surface.
    #    A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly by giving the model freedom to select more samples as support vectors.
    # Find optimal gamma and C parameters: http://scikit-learn.org/stable/auto_examples/svm/plot_rbf_parameters.html
    # ToDo: Set correct SVM params
    # [C, gamma] = findTrainClassifier(X,y)
    # clf = svm.SVC(kernel='rbf', gamma=gamma, C=C)
    clf = svm.SVC(kernel='linear',  C=1.0)
    # clf = LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto', priors=None, n_components=2, store_covariance=False)  # lda

    clf.fit(X,y)

    ##  Check if traingdata get 100% accuracy
    [accuracy,_,_] = modelAccuracy(y,  clf.predict(X))
    if(accuracy ==1.0):
        print("Correct classification with traingdata")
    else:
        print("Wrong classification with traingdata. check SVM algorithm")

    ## save model
    # with open('../../data/p300/model/svm_model.txt', 'wb') as outfile:
    #     pickle.dump(clf, outfile)

    ## save features
    # outfile = '../../data/p300/model/X_training.txt'
    # json.dump(X[0:20].tolist(), codecs.open(outfile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
    #               indent=4)  ### this saves the array in .json format
    # outfile = '../../data/p300/model/X_training_Baseline.txt'
    # json.dump(X[20:len(X)].tolist(), codecs.open(outfile, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True,
    #               indent=4)  ### this saves the array in .json format

    # print("\n------ Test Data ------")
    # with open('../../data/p300/ex7_1_cycles5/test/1532350012450_1_baseline.json') as f:
    #     baselineTest= json.load(f)
    # with open('../../data/p300/ex7_1_cycles5/test/1532350012442_1_volts.json') as f:
    #     voltsTest = json.load(f)
    # with open('../../data/p300/ex7_1_cycles5/test/1532350012477_1_cmdIdx.json') as f:
    #     cmdIdxTest = json.load(f)
    #
    # # create a numpy array
    # voltsTest = np.array(voltsTest, dtype='f')
    # baselineTest = np.array(baselineTest, dtype='f')
    # ## 4. Filter and Downsample Testdata
    # [filterdTestdata, filterdTestBaseline] = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels, debug)
    #
    # ##  5. Extract Features from Testdata
    # targetCmd = 0  # Playpause
    # [X_test, y_test] = extractFeature(filterdTestdata, filterdTestBaseline, targetCmd)
    # print("Anz. Features X_Test: "+str(len(X_test)))
    # print("y_Test: " + str(y_test))
    #
    #
    # ##  6. Check Model Accuracy
    # print("\n------ Model Accuracy ------")
    # y_pred =  clf.predict(X_test) #Predict the response for test dataset
    # print("predicted y "+str(y_pred))
    #
    # [accuracy, precision, recall] = modelAccuracy(y_test, y_pred)
    # print("Accuracy: "+str(accuracy))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))
    #
    # print("\n------ Test Data 2 ------")
    #
    # with open('../../data/p300/ex8_cycles5/1532426604595_1_baseline.json') as f:
    #     baselineTest= json.load(f)
    # with open('../../data/p300/ex8_cycles5/1532426604585_1_volts.json') as f:
    #     voltsTest = json.load(f)
    # with open('../../data/p300/ex8_cycles5/1532426604613_1_cmdIdx.json') as f:
    #     cmdIdxTest = json.load(f)
    #
    # # create a numpy array
    # voltsTest = np.array(voltsTest, dtype='f')
    # baselineTest = np.array(baselineTest, dtype='f')
    # ## 4. Filter and Downsample Testdata
    # [filterdTestdata, filterdTestBaseline] = filterDownsampleData(voltsTest, baselineTest, cmdIdxTest, channels, debug)
    #
    # ##  5. Extract Features from Testdata
    # targetCmd = 0  # Playpause
    # [X_test, y_test] = extractFeature(filterdTestdata, filterdTestBaseline, targetCmd)
    # print("Anz. Features X_Test: "+str(len(X_test)))
    # print("y_Test: " + str(y_test))
    #
    #
    # ##  6. Check Model Accuracy
    # print("\n------ Model Accuracy ------")
    # y_pred =  clf.predict(X_test) #Predict the response for test dataset
    # print("predicted y "+str(y_pred))
    #
    # [accuracy, precision, recall] = modelAccuracy(y_test, y_pred)
    # print("Accuracy: "+str(accuracy))
    # print("Precision: " + str(precision))
    # print("Recall: " + str(recall))



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

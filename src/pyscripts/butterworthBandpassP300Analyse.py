from scipy import sparse
from scipy._lib.six import xrange
from scipy.signal import butter, lfilter
from scipy.sparse.linalg import spsolve
import json, sys, numpy as np, matplotlib.pyplot as plt


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


def main():
    channel = 0  # channel 0-7

    # load json
    with open('../../test/data/p300_ina_1/data-2018-6-29-11-32-11.json') as f:
         dataJson = json.load(f)

    # Get channel data
    data = getChannelData(dataJson, channel)
    # commands data/data-2018-6-29-11-32-11.json
    # command order: next,voldown,play,prev,pause,volup
    # 1 cycles focus onvoldown
    cycle = 1
    focus = 1
    focusCmd = "voldown"
    cmdRow = [4329, 4449, 4570, 4690, 4810, 4930]
    # timestamps: [1530264752620,1530264753068,1530264753519,1530264753968,1530264754418,1530264754868]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 2 cycles focus onvoldown
    cycle = 2
    focus = 1
    focusCmd = "voldown"
    cmdRow = [5051, 5171, 5290, 5403, 5411, 5532]
    # timestamps: [1530264755325,1530264755771,1530264756218,1530264756668,1530264757119,1530264757568]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 3 cycles focus onvoldown
    cycle = 3
    focus = 1
    focusCmd = "voldown"
    cmdRow = [5652, 5772, 5892, 6127, 6133, 6253]
    # timestamps: [1530264758020,1530264758468,1530264758917,1530264759560,1530264759818,1530264760269]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 4 cycles focus onvoldown
    cycle = 4
    focus = 1
    focusCmd = "voldown"
    cmdRow = [6373, 6494, 6614, 6734, 6854, 6975]
    # timestamps: [1530264760719,1530264761169,1530264761620,1530264762068,1530264762518,1530264762968]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 5 cycles focus onvoldown
    cycle = 5
    focus = 1
    focusCmd = "voldown"
    cmdRow = [7092, 7095, 7215, 7335, 7456, 7576]
    # timestamps: [1530264763420,1530264763869,1530264764318,1530264764769,1530264765219,1530264765670]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 6 cycles focus onvoldown
    cycle = 6
    focus = 1
    focusCmd = "voldown"
    cmdRow = [7696, 7816, 7936, 8057, 8177, 8297]
    # timestamps: [1530264766118,1530264766569,1530264767018,1530264767470,1530264767919,1530264768369]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 7 cycles focus onvoldown
    cycle = 7
    focus = 1
    focusCmd = "voldown"
    cmdRow = [8417, 8538, 8658, 8778, 8893, 8898]
    # timestamps: [1530264768819,1530264769269,1530264769718,1530264770169,1530264770619,1530264771069]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 8 cycles focus onvoldown
    cycle = 8
    focus = 1
    focusCmd = "voldown"
    cmdRow = [9019, 9139, 9259, 9379, 9500, 9620]
    # timestamps: [1530264771551,1530264771969,1530264772419,1530264772869,1530264773318,1530264773768]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 9 cycles focus onvoldown
    cycle = 9
    focus = 1
    focusCmd = "voldown"
    cmdRow = [9740, 9860, 9981, 10101, 10221, 10341]
    # timestamps: [1530264774219,1530264774670,1530264775120,1530264775568,1530264776018,1530264776469]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 10 cycles focus onvoldown
    cycle = 10
    focus = 1
    focusCmd = "voldown"
    cmdRow = [10462, 10582, 10695, 10702, 10943, 10943]
    # timestamps: [1530264776919,1530264777368,1530264777819,1530264778268,1530264778830,1530264779168]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 11 cycles focus onvoldown
    cycle = 11
    focus = 1
    focusCmd = "voldown"
    cmdRow = [11063, 11183, 11303, 11424, 11544, 11664]
    # timestamps: [1530264779620,1530264780068,1530264780519,1530264780969,1530264781418,1530264781868]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 12 cycles focus onvoldown
    cycle = 12
    focus = 1
    focusCmd = "voldown"
    cmdRow = [11784, 11904, 12025, 12145, 12265, 12384]
    # timestamps: [1530264782319,1530264782769,1530264783219,1530264783757,1530264784120,1530264784569]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 13 cycles focus onvoldown
    cycle = 13
    focus = 1
    focusCmd = "voldown"
    cmdRow = [12385, 12506, 12626, 12746, 12866, 12987]
    # timestamps: [1530264785018,1530264785469,1530264785918,1530264786383,1530264786819,1530264787270]
    # commands: ["next","voldown","play","prev","pause","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 14 cycles focus onvoldown
    cycle = 14
    focus = 1
    focusCmd = "voldown"
    cmdRow = [13107, 13227, 13347, 13468, 13588, 13588]
    # timestamps: [1530264787719,1530264788168,1530264788676,1530264789070,1530264789518,1530264789968]
    # commands: ["next","voldown","play","prev","pause","volup"]

def detectP300(data,cmdRow,cycle,focus,focusCmd):
    print("----- Cycle "+str(cycle)+" focused command "+str(focusCmd)+" correct pos"+str(focus)+" -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 2
    slotSize = 125 #0.5s

    ## FILTER DATA
    #allDataFilterd = data    // if no bandpass desired
    allDataFilterd = filterData(data, lowcut, highcut, fs, order)

    ## NORMALIZE DATA
    # allDataFilterd = allDataFilterd-np.mean(allDataFilterd)
    # allDataFilterd = allDataFilterd/np.std(allDataFilterd, ddof=1)

    ## BASELINE CORRECTION   // https://stackoverflow.com/a/29185844
    def baseline_als(y, lam=10 ^ 5, p=0.01, niter=10):
        L = len(y)
        D = sparse.csc_matrix(np.diff(np.eye(L), 2))
        w = np.ones(L)
        for i in xrange(niter):
            W = sparse.spdiags(w, 0, L, L)
            Z = W + lam * D.dot(D.transpose())
            z = spsolve(Z, w * y)
            w = p * (y > z) + (1 - p) * (y < z)
        return z

    # allDataFilterd = baseline_als(allDataFilterd)

    ## Decibel Conversion - Reference = 1mV = 1e-3
    # allDataFilterd = list(map(lambda x: (10 * np.log10(abs(x * 1000) / 1e-3)), allDataFilterd))

    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300 = []
    data300SubBaseline = []
    for i in range(6):
        ## SUBTRACT BASELINE MEAN
         dataP300.append(allDataFilterd[cmdRow[i]:cmdRow[i]+slotSize])
         # filteredData = filterData(data[start-125*4:end], lowcut, highcut, fs, order)
         # dataP300.append(filteredData[125*4:])
         #dataP300.append(allDataFilterd[start:end])



    ## SUBTRACT BASELINE MEAN ( equally ajust height )
    dataP300Baseline = []
    for i in range(6):
         mean = np.mean(dataP300[i])
         dataP300Baseline.append(dataP300[i]-mean)
    #Overwrite dataP300 array
    dataP300 = dataP300Baseline

    ## SUBTRACT BASELINE for each datapoint from period before
    for i in range(6):
        dataP300[i] = dataP300[i] - dataP300[i - 1]

    ## Decibel Conversion - Reference = 1mV = 1e-3   for each epoch
    #for i in range(6):
    #    dataP300[i] = list(map(lambda x: (10 * np.log10(abs(x * 1000) / 1e-3)), dataP300[i]))

    # ONLY ANALYSE DATA BETWEEN 250ms(62) and 450ms(120) AFTER CMD
    #for i in range(6):
    #    dataP300[i] = dataP300[i][62:120]

    ## CALCULATE AMPLITUDE # ONLY ANALYSE DATA BETWEEN 200ms(50) and 400ms(100) AFTER CMD
    diff = []
    for i in range(6):
        diff.append(np.max(dataP300[i][80:110]) - np.min(dataP300[i][80:110]))
    #get max index
    idx = diff.index(np.max(diff))

    max = np.max(dataP300[idx])
    mean = np.mean(dataP300[idx])
    if (True):
         if (idx+1 == focus):
            print(str(idx+1) + " CORRECT P300 detection")
         else:
            print(str(idx+1) + " wrong P300 detection. Correct would be cmd " + str(focus))

    stringDiff = ''.join(str(diff))
    print("diff values: "+stringDiff)
    print("mean: " + str(np.mean(diff)))
    print("Max: "+str(np.max(diff)))
    idx = diff.index(np.max(diff))  # get index to match cmd 0-5
    if(idx == focus):
         print(str(idx)+" CORRECT P300 detection")
    else:
         print(str(idx)+" wrong P300 detection. Correct would be cmd "+str(focus))

    ## PLOT DATA

    # Plot cycle
    dataP300Cycle = np.array(dataP300).flatten()
    plotCycle(dataP300Cycle,lowcut,highcut,cycle)
    plt.figure(1)

    # Plot commands
    for i in range(6):
        if(i == focus):
            plot(dataP300[i], cycle, focusCmd, i+1, 'r', cmdRow[i])
            print("Max: " + str(np.max(dataP300[i][60:80]* 1000000)))
            print("mean: " + str(np.mean(dataP300[i])*1000000))
            #plot(dataP300Baseline[i], lowcut, highcut, cycle, focusCmd, 1, 'b')
        else:
            plot(dataP300[i], cycle, ("cmd %s"%(i+1)), i+1, 'b', cmdRow[i])

    plt.show()


def getChannelData(data, channel):
    channelData = []
    for val in data:
        channelData.append(val["channelData"][channel])
    return channelData


def filterData(data, lowcut, highcut, fs, order):
    # filter data with butter bandpass
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData

def plot(filteredData, cycle,title,cmd,color,row):
    # Plot original and filtered data
    nr = 320+cmd
    plt.subplot(nr)
    plt.title(' P300 Cmd: %d Cycle %d (row: %d)' % (cmd, cycle, row))
    plt.plot(filteredData*1000000, label=title, color=color)
    axes = plt.gca()
    axes.set_ylim([-35, 35])
    # plt.ylabel('volts')
    # plt.xlabel('Samples 250/s')
    # plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    # plt.grid(True)

def plotCycle(data, lowcut, highcut, cycle):
    plt.figure(cycle)
    plt.title(' P300 Cmd: %d Cycle (%d - %d Hz)' % (cycle, lowcut, highcut))
    plt.plot(data*1000000, 'b')
#start process
if __name__ == '__main__':
    main()

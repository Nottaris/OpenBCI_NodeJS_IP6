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
    with open('../../test/data/p300_job_06-07-18/data-2018-7-6-14-32-40.json') as f:
        dataJson = json.load(f)

    # Get channel data
    data = getChannelData(dataJson, channel)

    # commands data/data-2018-7-6-14-32-40.json
    # command order: next,voldown,playpause,prev,volup
    # 1 cycles focus onplaypause
    cycle = 1
    focus = 99
    focusCmd = "playpause"
    cmdRow = [5470, 5540, 5652, 5765, 5878]
    # timestamps: [1530880386457,1530880386734,1530880387184,1530880387633,1530880388083,1530880388533]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 2 cycles focus onplaypause
    cycle = 2
    focus = 99
    focusCmd = "playpause"
    cmdRow = [5991, 6103, 6216, 6328, 6441]
    # timestamps: [1530880388983,1530880389434,1530880389883,1530880390334,1530880390783,1530880391233]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 3 cycles focus onplaypause
    cycle = 3
    focus = 99
    focusCmd = "playpause"
    cmdRow = [6554, 6666, 6779, 6891, 7004]
    # timestamps: [1530880391683,1530880392134,1530880392584,1530880393033,1530880393482,1530880393934]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 4 cycles focus onplaypause
    cycle = 4
    focus = 2
    focusCmd = "playpause"
    cmdRow = [7117, 7229, 7342, 7454, 7567]
    # timestamps: [1530880394385,1530880394834,1530880395284,1530880395733,1530880396183,1530880396633]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 5 cycles focus onplaypause
    cycle = 5
    focus = 2
    focusCmd = "playpause"
    cmdRow = [7680, 7792, 7905, 8017, 8130]
    # timestamps: [1530880397082,1530880397533,1530880397982,1530880398434,1530880398883,1530880399334]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 6 cycles focus onplaypause
    cycle = 6
    focus = 2
    focusCmd = "playpause"
    cmdRow = [8243, 8355, 8468, 8581, 8693]
    # timestamps: [1530880399782,1530880400233,1530880400682,1530880401133,1530880401584,1530880402033]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 7 cycles focus onplaypause
    cycle = 7
    focus = 2
    focusCmd = "playpause"
    cmdRow = [8806, 8918, 9031, 9144, 9256]
    # timestamps: [1530880402483,1530880402932,1530880403385,1530880403834,1530880404283,1530880404734]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 8 cycles focus onplaypause
    cycle = 8
    focus = 2
    focusCmd = "playpause"
    cmdRow = [9369, 9481, 9594, 9707, 9819]
    # timestamps: [1530880405183,1530880405634,1530880406083,1530880406534,1530880406984,1530880407432]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 9 cycles focus onplaypause
    cycle = 9
    focus = 2
    focusCmd = "playpause"
    cmdRow = [9932, 10044, 10157, 10270, 10382]
    # timestamps: [1530880407884,1530880408333,1530880408783,1530880409234,1530880409684,1530880410133]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 10 cycles focus onplaypause
    cycle = 10
    focus = 2
    focusCmd = "playpause"
    cmdRow = [10495, 10608, 10720, 10833, 10944]
    # timestamps: [1530880410584,1530880411032,1530880411484,1530880411934,1530880412383,1530880412833]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 11 cycles focus onplaypause
    cycle = 11
    focus = 2
    focusCmd = "playpause"
    cmdRow = [11058, 11171, 11283, 11396, 11508]
    # timestamps: [1530880413284,1530880413732,1530880414183,1530880414633,1530880415083,1530880415534]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)


def detectP300(data,cmdRow,cycle,focus,focusCmd):
    print("----- Cycle "+str(cycle)+" focused command "+str(focusCmd)+" correct pos"+str(focus)+" -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 4
    slotSize = 125 #0.5s
    cmdCount = 5

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
    for i in range(cmdCount):
        ## SUBTRACT BASELINE MEAN
         dataP300.append(allDataFilterd[cmdRow[i]:cmdRow[i]+slotSize])
         # filteredData = filterData(data[start-125*4:end], lowcut, highcut, fs, order)
         # dataP300.append(filteredData[125*4:])
         #dataP300.append(allDataFilterd[start:end])



    ## SUBTRACT BASELINE MEAN ( equally ajust height )
    dataP300Baseline = []
    for i in range(cmdCount):
         mean = np.mean(dataP300[i])
         dataP300Baseline.append(dataP300[i]-mean)
    #Overwrite dataP300 array
    dataP300 = dataP300Baseline

    ## SUBTRACT BASELINE for each datapoint from period before
    for i in range(cmdCount):
        dataP300[i] = dataP300[i] - dataP300[i - 1]

    ## Decibel Conversion - Reference = 1mV = 1e-3   for each epoch
    #for i in range(6):
    #    dataP300[i] = list(map(lambda x: (10 * np.log10(abs(x * 1000) / 1e-3)), dataP300[i]))

    # ONLY ANALYSE DATA BETWEEN 250ms(62) and 450ms(120) AFTER CMD
    #for i in range(6):
    #    dataP300[i] = dataP300[i][62:120]

    ## CALCULATE AMPLITUDE # ONLY ANALYSE DATA BETWEEN 200ms(50) and 400ms(100) AFTER CMD
    diff = []
    for i in range(cmdCount):
        diff.append(np.max(dataP300[i][50:100]) - np.min(dataP300[i][50:100]))
        max = np.max(dataP300[i][50:100])
        mean = np.mean(dataP300[i][50:100])
        std = np.mean(dataP300[i][50:100])
        print("max: "+str(max)+" mean "+str(mean)+" std "+str(std))
    #get max index
    idx = diff.index(np.max(diff))

    max = np.max(dataP300[idx])
    mean = np.mean(dataP300[idx])
    if (True):
         if (idx == focus):
            print(str(idx) + " CORRECT P300 detection")
         else:
            print(str(idx) + " wrong P300 detection. Correct would be cmd " + str(focus))

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
    for i in range(cmdCount):
        if(i == focus):
            plot(dataP300[i], cycle, focusCmd, i+1, 'r', cmdRow[i])
            print("Max: " + str(np.max(dataP300[i][60:80])))
            print("mean: " + str(np.mean(dataP300[i])))
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
    plt.plot(filteredData, label=title, color=color)
    axes = plt.gca()
    # axes.set_ylim([-100, 100])
    # plt.ylabel('volts')
    # plt.xlabel('Samples 250/s')
    # plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    # plt.grid(True)

def plotCycle(data, lowcut, highcut, cycle):
    plt.figure(cycle)
    plt.title(' P300 Cmd: %d Cycle (%d - %d Hz)' % (cycle, lowcut, highcut))
    plt.plot(data, 'b')
    axes = plt.gca()

def plotCmd(data, lowcut, highcut, cmd):
    plt.figure(0)
    plt.title(' P300 Cmd: %d Cycle (%d - %d Hz)' % (cmd, lowcut, highcut))
    plt.plot(data, 'b')
    axes = plt.gca()

#start process
if __name__ == '__main__':
    main()

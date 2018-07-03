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
    with open('../../test/data/p300_ina_1/data-2018-6-29-14-06-10.json') as f:
         dataJson = json.load(f)

    # Get channel data
    data = getChannelData(dataJson, channel)
    next = [3953, 4628, 5304, 5979]
    detectP300Cycles(data, next, "next",1)
    voldown = [4065, 4741, 5410, 6092]
    detectP300Cycles(data, voldown, "voldown",2)
    play = [4178, 4853, 5529, 6204]
    prev = [4290, 4966, 5641, 6317]
    pause = [4403, 5078, 5754, 6430]
    volup = [4516, 5191, 5867, 6542]

    plt.show()


    # commands data/data-2018-6-29-14-06-10.json
    # command order: next,voldown,play,prev,pause,volup
    # # 1 cycles focus onvoldown
    # cycle = 1
    # focus = 1
    # focusCmd = "voldown"
    # cmdRow = [2607, 2714, 2827, 2939, 3052, 3165]
    # # timestamps: [1530273985005,1530273985439,1530273985887,1530273986337,1530273986789,1530273987239]
    # # commands: ["next","voldown","play","prev","pause","volup"]
    # detectP300(data, cmdRow, cycle, focus, focusCmd)
    # # 2 cycles focus onvoldown
    # cycle = 2
    # focus = 1
    # focusCmd = "voldown"
    # cmdRow = [3277, 3390, 3502, 3607, 3726, 3840]
    # # timestamps: [1530273987687,1530273988136,1530273988587,1530273989039,1530273989488,1530273989938]
    # # commands: ["next","voldown","play","prev","pause","volup"]
    # detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 3 cycles focus onvoldown
    # cycle = 3
    # focus = 1
    # focusCmd = "voldown"
    # cmdRow = [3953, 4065, 4178, 4290, 4403, 4516]
    # # timestamps: [1530273990387,1530273990837,1530273991288,1530273991737,1530273992187,1530273992638]
    # # commands: ["next","voldown","play","prev","pause","volup"]
    # detectP300(data, cmdRow, cycle, focus, focusCmd)
    # # 4 cycles focus onvoldown
    # cycle = 4
    # focus = 1
    # focusCmd = "voldown"
    # cmdRow = [4628, 4741, 4853, 4966, 5078, 5191]
    # # timestamps: [1530273993086,1530273993538,1530273993989,1530273994436,1530273994886,1530273995337]
    # # commands: ["next","voldown","play","prev","pause","volup"]
    # detectP300(data, cmdRow, cycle, focus, focusCmd)
    # # 5 cycles focus onvoldown
    # cycle = 5
    # focus = 1
    # focusCmd = "voldown"
    # cmdRow = [5304, 5410, 5529, 5641, 5754, 5867]
    # # timestamps: [1530273995787,1530273996237,1530273996687,1530273997139,1530273997587,1530273998037]
    # # commands: ["next","voldown","play","prev","pause","volup"]
    # detectP300(data, cmdRow, cycle, focus, focusCmd)
    # # 6 cycles focus onvoldown
    # cycle = 6
    # focus = 1
    # focusCmd = "voldown"
    # cmdRow = [5979, 6092, 6204, 6317, 6430, 6542]
    # # timestamps: [1530273998487,1530273998937,1530273999387,1530273999837,1530274000287,1530274000737]
    # # commands: ["next","voldown","play","prev","pause","volup"]
    # detectP300(data, cmdRow, cycle, focus, focusCmd)
    # # # 7 cycles focus onvoldown
    # # cycle = 7
    # # focus = 1
    # # focusCmd = "voldown"
    # # cmdRow = [6655, 6767, 6880, 6992, 7094, 7214]
    # # # timestamps: [1530274001188,1530274001637,1530274002087,1530274002537,1530274002987,1530274003437]
    # # # commands: ["next","voldown","play","prev","pause","volup"]
    # # detectP300(data, cmdRow, cycle, focus, focusCmd)


def detectP300Cycles(data,cmdRow,cmd,nr):
    print("-----  command "+str(cmd)+"  -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 2
    slotSize = 125 #0.5s

    ## FILTER DATA
    allDataFilterd = filterData(data, lowcut, highcut, fs, order)
    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300 = []
    data300SubBaseline = []
    for i in range(4):
        ## SUBTRACT BASELINE MEAN
         dataP300.append(allDataFilterd[cmdRow[i]:cmdRow[i]+slotSize])

    mean = np.mean(np.array(dataP300).flatten())
    data300SubBasline = dataP300 - mean
    print(dataP300[1])
    print(data300SubBasline[1])
    plt.figure(1)
    for i in range(4):
        plot(dataP300[1], 0, 1, nr, 'r', cmdRow[2])
        plot(data300SubBasline[1], 0, 1, nr, 'b', cmdRow[2])

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
    for i in range(6):
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

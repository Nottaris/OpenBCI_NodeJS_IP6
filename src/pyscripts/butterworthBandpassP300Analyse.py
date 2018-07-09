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
    channel = 1  # channel 0-7

    # load json
    with open('../../test/data/p300_exp_2/exp2_C_Matrix/data-2018-7-9-13-47-10.json') as f:
        dataJson = json.load(f)

    # Get channel data
    data = getChannelData(dataJson, channel)

    # commands data/data-2018-7-9-13-47-10.json
    # command order: next,voldown,playpause,prev,volup
    # 1 cycles focus onplaypause
    cycle = 1
    focus = 2
    focusCmd = "playpause"
    cmdRow = [6074, 6222, 6372, 6522, 6672]
    # timestamps: [1531136858336,1531136858928,1531136859528,1531136860127,1531136860727]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 2 cycles focus onplaypause
    cycle = 2
    focus = 2
    focusCmd = "playpause"
    cmdRow = [6822, 6972, 7122, 7272, 7422]
    # timestamps: [1531136861327,1531136861928,1531136862529,1531136863128,1531136863728]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 3 cycles focus onplaypause
    cycle = 3
    focus = 2
    focusCmd = "playpause"
    cmdRow = [7572, 7722, 7873, 8023, 8173]
    # timestamps: [1531136864328,1531136864928,1531136865528,1531136866129,1531136866727]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 4 cycles focus onplaypause
    cycle = 4
    focus = 2
    focusCmd = "playpause"
    cmdRow = [8323, 8473, 8623, 8774, 8924]
    # timestamps: [1531136867328,1531136867927,1531136868528,1531136869129,1531136869729]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 5 cycles focus onplaypause
    cycle = 5
    focus = 2
    focusCmd = "playpause"
    cmdRow = [9074, 9224, 9374, 9525, 9675]
    # timestamps: [1531136870327,1531136870928,1531136871528,1531136872128,1531136872727]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 6 cycles focus onplaypause
    cycle = 6
    focus = 2
    focusCmd = "playpause"
    cmdRow = [9825, 9975, 10125, 10276, 10426]
    # timestamps: [1531136873328,1531136873928,1531136874528,1531136875127,1531136875729]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 7 cycles focus onplaypause
    cycle = 7
    focus = 2
    focusCmd = "playpause"
    cmdRow = [10578, 10726, 10876, 11026, 11177]
    # timestamps: [1531136876330,1531136876928,1531136877527,1531136878128,1531136878728]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 8 cycles focus onplaypause
    cycle = 8
    focus = 2
    focusCmd = "playpause"
    cmdRow = [11327, 11477, 11627, 11777, 11928]
    # timestamps: [1531136879328,1531136879928,1531136880528,1531136881127,1531136881727]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 9 cycles focus onplaypause
    cycle = 9
    focus = 2
    focusCmd = "playpause"
    cmdRow = [12078, 12228, 12378, 12528, 12678]
    # timestamps: [1531136882327,1531136882929,1531136883527,1531136884127,1531136884728]
    # commands: ["next","voldown","playpause","prev","volup"]
    detectP300(data, cmdRow, cycle, focus, focusCmd)
    # 10 cycles focus onplaypause
    cycle = 10
    focus = 2
    focusCmd = "playpause"
    cmdRow = [12829, 12979, 13129, 13279, 13429]
    # timestamps: [1531136885328,1531136885928,1531136886527,1531136887128,1531136887728]
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
    # for i in range(cmdCount):
    #     dataP300[i] = dataP300[i] - dataP300[i - 1]

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
    # plotCycle(dataP300Cycle,lowcut,highcut,cycle)
    plt.figure(1)

    # Plot commands
    commands = ["next","voldown","play","prev","volup"]
    for i in range(cmdCount):
        if(i == focus):
            plot(dataP300[i], cycle, focusCmd, i+1, 'r', commands[i])
            print("Max: " + str(np.max(dataP300[i][60:80])))
            print("mean: " + str(np.mean(dataP300[i])))
            #plot(dataP300Baseline[i], lowcut, highcut, cycle, focusCmd, 1, 'b')
        else:
            plot(dataP300[i], cycle, ("cmd %s"%(i+1)), i+1, 'b', commands[i])

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
    plt.title(' P300 Cycle: %d Cmd: %s ' % (cycle, row))
    plt.plot(filteredData*1000000, label=title, color=color)
    axes = plt.gca()
    axes.set_ylim([-35, 35])
    plt.ylabel('microVolts')
    plt.xlabel('Samples 250/s')
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

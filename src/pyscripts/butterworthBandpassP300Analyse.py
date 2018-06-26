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
    channel = 0 #channel 0-7

    # load json
    with open('../../test/data/p300_job_4/data-2018-6-26-12-39-22.json') as f:
         dataJson = json.load(f)

   # Get channel data
    data = getChannelData(dataJson, channel)

    # 6 - 12 cycles focus on play
    start = 5653
    cycle = 6
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 6134
    cycle = 7
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 6494
    cycle = 8
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 6855
    cycle = 9
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7216
    cycle = 10
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7577
    cycle = 11
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7937
    cycle = 12
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7577
    cycle = 13
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7937
    cycle = 14
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7577
    cycle = 15
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7937
    cycle = 16
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7577
    cycle = 17
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7937
    cycle = 18
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)

    # load json
    with open('../../test/data/p300_job_4/data-2018-6-26-12-40-45.json') as f:
        dataJson = json.load(f)

    # Get channel data
    data = getChannelData(dataJson, channel)

    # 6 - 12 cycles focus on play
    start = 4449
    cycle = 3
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 5171
    cycle = 4
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 5772
    cycle = 5
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 6494
    cycle = 6
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7215
    cycle = 7
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)
    start = 7816
    cycle = 8
    focus = 3
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)

def detectP300(data,start,cycle,focus,focusCmd):
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
    def baseline_als(y, lam=10^5, p=0.01, niter=10):
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
    end = start+slotSize
    dataP300 = []
    data300SubBaseline = []
    for i in range(6):
        # baseline = data[start-125:start]
        # epoche = data[start:end]
        # data300SubBaseline.append( np.subtract(epoche, baseline))
        # filteredData = filterData(data[start-125*4:end], lowcut, highcut, fs, order)
        # dataP300.append(filteredData[125*4:])
        dataP300.append(allDataFilterd[start:end])
        start = end
        end = start + slotSize

    ## SUBTRACT BASELINE MEAN ( equally ajust height )
    #dataP300Baseline = []
    #for i in range(6):
    #      mean = np.mean(dataP300[i])
    #      print("baseline mean: "+str(mean))
    #      dataP300Baseline.append(dataP300[i]-mean)

    ## SUBTRACT BASELINE for each datapoint from period before
    #for i in range(6):
    #    dataP300[i]=dataP300[i] - dataP300[i-1]

    ## Decibel Conversion - Reference = 1mV = 1e-3   for each epoch
    #for i in range(6):
    #    dataP300[i] = list(map(lambda x: (10 * np.log10(abs(x * 1000) / 1e-3)), dataP300[i]))

    # ONLY ANALYSE DATA BETWEEN 250ms(62) and 450ms(120) AFTER CMD
    # for i in range(6):
    #   dataP300[i] = dataP300[i][62:120]

    ## CALCULATE AMPLITUDE
    diff = []
    for i in range(6):
         diff.append(np.max(dataP300[i]) - np.min(dataP300[i]))

    stringDiff = ''.join(str(diff))
    print("diff values: "+stringDiff)
    print("mean: " + str(np.mean(diff)))
    print("Max: "+str(np.max(diff)))
    idx = diff.index(np.max(diff)) + 1  # get index and add 1 to match cmd 1-6
    if(idx == focus):
         print(str(idx)+" CORRECT P300 detection")
    else:
         print(str(idx)+" wrong P300 detection. Correct would be cmd "+str(focus))

    ## PLOT DATA

    #plt.figure(0)
    #plot(allDataFilterd[slotSize*4:],lowcut,highcut,order,"totalDataFilterd",1,'b')
    plt.figure(1)
    axes = plt.gca()
    axes.set_ylim([0, 100])

    for i in range(6):
        if(i == focus-1):
            plot(dataP300[i], lowcut, highcut, cycle, focusCmd, 1, 'r')
            print("Max: " + str(np.max(dataP300[i][60:80]* 1000000)))
            print("mean: " + str(np.mean(dataP300[i])*1000000))
            #plot(dataP300Baseline[i], lowcut, highcut, cycle, focusCmd, 1, 'b')
       # else:
       #     plot(dataP300[i], lowcut, highcut, cycle, ("cmd %s"%(i+1)), 1, 'b')

    plt.show()

def getChannelData(data, channel):
    channelData=[]
    for val in data:
        channelData.append(val["channelData"][channel])
    return channelData

def filterData(data,lowcut,highcut,fs,order):
    #filter data with butter bandpass
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData

def plot(filteredData, lowcut, highcut, cycle,title,cmd,color):
    # Plot original and filtered data
    nr = 310+cmd
    plt.subplot(nr)
    plt.title(' Compare P300 - Cycle %d (%d - %d Hz)' % (cycle, lowcut, highcut))
    plt.plot(filteredData, label=title, color=color)
    plt.ylabel('volts')
    plt.xlabel('Samples 250/s')
    plt.legend(loc='best', bbox_to_anchor=(1, 0.5))
    plt.grid(True)


#start process
if __name__ == '__main__':
    main()
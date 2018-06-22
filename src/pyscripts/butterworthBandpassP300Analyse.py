from scipy.signal import butter, lfilter
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
    channel = 4 #channel 0-7

    # load json
    with open('../../test/data/p300_ex3/data-2018-6-22-14-27-04.json') as f:
         dataJson = json.load(f)

   # Get channel data
    data = getChannelData(dataJson, channel)

    # First 5 cycles focus on play
    start = 251
    cycle = 1
    focus = 5
    focusCmd = "play"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 1006
    cycle = 2
    focus = 6
    focusCmd = "play"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 1762
    cycle = 3
    focus = 6
    focusCmd = "play"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 2518
    cycle = 4
    focus = 6
    focusCmd = "play"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 3274
    cycle = 5
    focus = 6
    focusCmd = "play"
    detectP300(data, start, cycle, focus, focusCmd)

    # Next 5 cycles focus on voldown
    start = 4030
    cycle = 6
    focus = 5
    focusCmd = "voldown"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 4786
    cycle = 7
    focus = 3
    focusCmd = "voldown"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 5542
    cycle = 8
    focus = 3
    focusCmd = "voldown"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 6298
    cycle = 9
    focus = 3
    focusCmd = "voldown"
    detectP300(data,start,cycle,focus,focusCmd)
    start = 7054
    cycle = 10
    focus = 2
    focusCmd = "voldown"
    detectP300(data, start, cycle, focus, focusCmd)

def detectP300(data,start,cycle,focus,focusCmd):
    print("----- Cycle "+str(cycle)+" focused command "+str(focusCmd)+" correct pos"+str(focus)+" -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1.0
    highcut = 15.0
    order = 2
    slotSize = 125 #0.5s

    ## FILTER DATA
    allDataFilterd = filterData(data, lowcut, highcut, fs, order)

    ## NORMALIZE DATA
    # allDataFilterd = allDataFilterd-np.mean(allDataFilterd)
    # allDataFilterd = allDataFilterd/np.std(allDataFilterd, ddof=1)

    ## SPLIT DATA IN COMMAND EPOCHES
    end = start+slotSize
    dataP300 = []
    for i in range(6):
        dataP300.append(allDataFilterd[start:end])
        start = end
        end = start + slotSize

    ## ONLY ANALYSE DATA BETWEEN 250ms(62) and 450ms(120) AFTER CMD
    # for i in range(6):
    #     dataP300[i] = dataP300[i][62:120]

    ## CALCULATE AMPLITUDE
    diff = []
    for i in range(6):
        diff.append(np.max(dataP300[i]) - np.min(dataP300[i]))

    stringDiff = ''.join(str(diff))
    print("diff values: "+stringDiff)
    print("mean: " + str(np.mean(diff)))
    print("Max: "+str(np.max(diff)))
    idx = diff.index(np.max(diff))
    if(idx == focus):
        print(str(idx+1)+" CORRECT P300 detection")
    else:
        print(str(idx+1)+" wrong P300 detection. Correct would be cmd "+str(focus))

    ## PLOT DATA

    #plt.figure(0)
    # plot(allDataFilterd[slotSize*2:],lowcut,highcut,order,"totalDataFilterd",1,'b')
    plt.figure(1)

    for i in range(6):
        if(i == focus-1):
            plot(dataP300[i], lowcut, highcut, cycle, focusCmd, 1, 'r')
        else:
            plot(dataP300[i], lowcut, highcut, cycle, ("cmd %s"%(i+1)), 1, 'b')

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
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)


#start process
if __name__ == '__main__':
    main()
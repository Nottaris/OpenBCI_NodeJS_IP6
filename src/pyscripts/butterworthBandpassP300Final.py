from scipy.signal import butter, lfilter
import json, numpy as np

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


def detectP300(data, start, cycle, focus, focusCmd):
    #print("----- Cycle " + str(cycle) + " focused command " + str(focusCmd) + " correct pos" + str(focus) + " -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 2
    slotSize = 125  # 0.5s

    ## FILTER DATA
    allDataFilterd = filterData(data, lowcut, highcut, fs, order)

    ## SPLIT DATA IN COMMAND EPOCHES
    end = start + slotSize
    dataP300 = []
    for i in range(6):
        dataP300.append(allDataFilterd[start:end])
        start = end
        end = start + slotSize


    # ONLY ANALYSE DATA BETWEEN 280ms(70) and 440ms(110) AFTER CMD
    for i in range(6):
        dataP300[i] = dataP300[i][70:110]

    ## SUBTRACT BASELINE for each datapoint from period before
    for i in range(6):
        dataP300[i] = dataP300[i] - dataP300[i - 1]

    ## CALCULATE AMPLITUDE
    diff = []
    for i in range(6):
        diff.append(np.max(dataP300[i]) - np.min(dataP300[i]))
    #get index of max diff
    idx = diff.index(np.max(diff))

    max = np.max(dataP300[idx])
    mean = np.mean(dataP300[idx])
    if (True):
         if (idx+1 == focus):
            print(str(idx+1) + " is CORRECT")
         else:
            print(str(idx+1) + " is wrong. Correct would be cmd " + str(focus))

    #print("diff values: " + ''.join(str(diff)))
    #print("diff values Mean: " + str(np.mean(diff)))
    #print("diff values Max: " + str(np.max(diff)))


    #for i in range(6):
    #   if (i == focus - 1):
    #print("Max: " + str(np.max(dataP300[idx])*100000))
    #print("mean: " + str(np.mean(dataP300[idx])*100000))
    #print("max-mean: " + str(np.max(dataP300[idx])*100000 - np.mean(dataP300[idx])*100000))
    #print("max/mean: "+ str(np.max(dataP300[idx])/np.mean(dataP300[idx])))



def getChannelData(data, channel):
    channelData = []
    for val in data:
        channelData.append(val["channelData"][channel])
    return channelData


def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

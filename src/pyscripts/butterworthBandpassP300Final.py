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
    # 0 = OZ


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


def detectP300(data, cmdRow, cycle, focus, focusCmd):
    print("----- Cycle " + str(cycle) + " focused command " + str(focusCmd) + " correct pos" + str(focus) + " -----")

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 2
    slotSize = 125  #500ms
    cmdCount = 5

    ## FILTER DATA
    allDataFilterd = filterData(data, lowcut, highcut, fs, order)

    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300 = []
    for i in range(cmdCount):
        dataP300.append(allDataFilterd[cmdRow[i]:cmdRow[i] + slotSize])

    # ONLY ANALYSE DATA BETWEEN 320ms(70) and 450ms(112) AFTER CMD
    dataP300Slots = []
    dataBaseline = []
    for i in range(cmdCount):
        dataBaseline.append(dataP300[i][10:50])
        dataP300Slots.append(dataP300[i][80:120])

    ## SUBTRACT BASELINE for each datapoint from period before
    for i in range(cmdCount):
        dataP300Slots[i] = dataP300Slots[i] - dataBaseline[i]

    ## CALCULATE AMPLITUDE
    diff = []
    for i in range(cmdCount):
        diff.append(np.max(dataP300Slots[i]) - np.min(dataP300Slots[i]))
    #get index of max diff
    idx = diff.index(np.max(diff))

    max = np.max(dataP300Slots[idx])
    mean = np.mean(dataP300Slots[idx])
    if (True):
         if (idx == focus):
            print(str(idx) + " is CORRECT")
         else:
            print(str(idx) + " is wrong. Correct would be cmd " + str(focus))

    #print("diff values: " + ''.join(str(diff)))
    #print("diff values Mean: " + str(np.mean(diff)))
    #print("diff values Max: " + str(np.max(diff)))


    #for i in range(cmdCount):
    #   if (i == focus - 1):
    #print("Max: " + str(np.max(dataP300Slots[idx])*100000))
    #print("mean: " + str(np.mean(dataP300Slots[idx])*100000))
    #print("max-mean: " + str(np.max(dataP300Slots[idx])*100000 - np.mean(dataP300Slots[idx])*100000))
    print("max/mean: "+ str(np.max(dataP300Slots[idx])/np.mean(dataP300Slots[idx])))



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

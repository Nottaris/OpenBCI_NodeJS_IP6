from typing import List, Any

from scipy.signal import butter, lfilter
import json, sys, numpy as np


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
    # get data as an array from read_in()
    datainput = sys.stdin.read()

    # create array
    input = json.loads(datainput)

    # divide volts from commands
    volts = input[:-5]  # everything except last 5 items should be volts
    commands = input[-5:]  # last 5 items of array should be commands

    # create a numpy array
    data = np.array(volts)

    # detect P300
    cmd = detectP300(data, commands)

    # send docommand back to node
    print(cmd)


def detectP300(data, commands):
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 0.1
    highcut = 15.0
    order = 2
    slotSize = 112
    cmdCount = 5
    threshold = 1.5

    ## FILTER DATA
    allDataFilterd = filterData(data, lowcut, highcut, fs, order)

    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300 = []
    for i in range(cmdCount):
        dataP300.append(allDataFilterd[i * slotSize:(i * slotSize) + slotSize])

    # ONLY ANALYSE DATA BETWEEN 320ms(70) and 450ms(112) AFTER CMD
    dataP300Slots = []
    for i in range(cmdCount):
        dataP300Slots.append(dataP300[i][70:112])

    ## CALCULATE AMPLITUDE
    diff = []
    for i in range(cmdCount):
        diff.append(np.max(dataP300Slots[i]) - np.min(dataP300Slots[i]))
    # get index of max diff
    idx = diff.index(np.max(diff))

    max = np.max(dataP300Slots[idx])
    mean = np.mean(dataP300Slots[idx])

    if (max > mean * threshold):
        return commands[idx]
    else:
        return "nop"


def filterData(data, lowcut, highcut, fs, order):
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData


# start process
if __name__ == '__main__':
    main()

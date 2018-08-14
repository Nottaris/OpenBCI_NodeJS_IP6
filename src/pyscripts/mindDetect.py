##
# detect mind commands
# (beta, unfinished as eeg data did not show motor imagery)
#
##

import numpy as np
from mindFunctions import filterDownsampleData
from scipy.signal import butter, lfilter
import json, sys, numpy as np, matplotlib.pyplot as plt


def main():

    # # get data as an array from read_in()
    # datainput = json.loads(sys.stdin.read())
    # volts = datainput['volts']
    # baseline = datainput['baseline']
    #
    # # create a numpy array
    # volts = np.array(volts, dtype='f')
    # baseline = np.array(baseline, dtype='f')
    #
    # # active channels
    # channels = [0, 1, 2, 3, 4, 5, 6, 7]  # 0-7 channels
    #
    # # filter and downsample data
    # voltsF = filterDownsampleData(volts)
    # baselineF = filterDownsampleData(baseline)
    #
    # TODO: implement detection based on ml
    # detectMind(voltsF, baselineF)
    # no command found is "nop"
    print("nop")


# start process
if __name__ == '__main__':
    main()

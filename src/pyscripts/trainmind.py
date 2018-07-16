from scipy import sparse
from scipy._lib.six import xrange
from scipy.signal import butter, lfilter
from scipy.sparse.linalg import spsolve
from scipy.stats import norm
from tempfile import TemporaryFile
import time, json, sys, numpy as np, matplotlib.pyplot as plt
from pprint import pprint
import os


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


def filterData(data, lowcut, highcut, fs, order):
    doubledata = np.concatenate([data, data])
    doubledataFilterd = butter_bandpass_filter(doubledata, lowcut, highcut, fs, order)
    dataBP0 = doubledataFilterd[int(len(doubledataFilterd)/2):]

    return dataBP0


def main():
    # get trainingCmd as from read_in()
    input = sys.stdin.read()
    trainingCmd = str(input.strip())
    # filepath = '/Users/mjair/Documents/GitHub/OpenBCI_NodeJS_IP6/data/mind/training-playpause.json'
    cwd = os.getcwd()
    filepath = ''.join([cwd, '/data/mind/training-', trainingCmd, '.json'])
    path = filepath.replace('"', '')
    # read file of trainingCmd
    with open(path) as f:
        data = json.load(f)

    traindata = np.array(data)
    # process data
    trainmind(traindata)

    # send success back to node
    # TODO: uncomment / implement success boolean return
    # print('true')


def trainmind(traindata):
    ch1 = traindata[:, 0]
    ch2 = traindata[:, 1]
    ch3 = traindata[:, 2]
    ch4 = traindata[:, 3]
    ch5 = traindata[:, 4]
    ch6 = traindata[:, 5]
    ch7 = traindata[:, 6]
    ch8 = traindata[:, 7]

    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 8
    highcut = 30.0
    order = 5

    ## FILTER DATA
    ch1f = filterData(ch1, lowcut, highcut, fs, order)
    ch2f = filterData(ch2, lowcut, highcut, fs, order)
    ch3f = filterData(ch3, lowcut, highcut, fs, order)
    ch4f = filterData(ch4, lowcut, highcut, fs, order)
    ch5f = filterData(ch5, lowcut, highcut, fs, order)
    ch6f = filterData(ch6, lowcut, highcut, fs, order)
    ch7f = filterData(ch7, lowcut, highcut, fs, order)
    ch8f = filterData(ch8, lowcut, highcut, fs, order)

    ## save to file for dev
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open("data/mind/"+timestr+'_dataCh1.json', 'w') as outfile:
        json.dump(ch1f.tolist(), outfile)
    with open("data/mind/"+timestr+'_dataCh2.json', 'w') as outfile:
        json.dump(ch2f.tolist(), outfile)
    with open("data/mind/"+timestr+'_dataCh3.json', 'w') as outfile:
        json.dump(ch3f.tolist(), outfile)

# start process
if __name__ == '__main__':
    main()

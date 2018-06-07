from scipy.signal import butter, lfilter
import sys, json, numpy as np


# Source http://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html
#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    for line in sys.stdin:
        print(line[:-1])
    # Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def mainTEST():
    # get our data as an array from read_in()
    lines = read_in()

    # create a numpy array
    data = np.array(lines)


    print(data[0])
    print(data[1])
    print(data[2])
    print(data[3])
    print(data[4])
    print(data[5])
    print(data[6])
    print(data[7])
    print(data[8])

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 5.0
    highcut = 50.0

    y = butter_bandpass_filter(data, lowcut, highcut, fs, order=6)
    print(y[0])
    print(y[1])
    print(y[2])
    print(y[3])
    print(y[4])
    print(y[5])
    print(y[6])
    print(y[7])
    print(y[8])

    #run(np_lines)

    #use numpys sum method to find sum of all elements in the array
    lines_sum = np.sum(data)

    #return the sum to the output stream
    print(lines_sum)


def main():
    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1.0
    highcut = 20.0

    # get our data as an array from read_in()
    lines = []
    for line in sys.stdin:
        lines.append(float(line))

    # create a numpy array
    data = np.array(lines)

    # filter data
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order=6)

    # send filterd data back to node
    for f in filterdData:
        print(f)


#start process
if __name__ == '__main__':
    main()
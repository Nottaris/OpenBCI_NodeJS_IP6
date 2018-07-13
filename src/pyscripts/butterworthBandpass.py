from scipy.signal import butter, lfilter
import json, sys, numpy as np, matplotlib.pyplot as plt


# Source butter_bandpass http://scipy-cookbook.readthedocs.io/items/ButterworthBandpass.html

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


def main():
    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1.0
    highcut = 4.0

    # get our data as an array from read_in()
    datainput = sys.stdin.read()
    data = np.array(json.loads(datainput))
    print(data[:, 0])

    # filter data
    for i in range(0, 8):
        filterdData = butter_bandpass_filter(data[:, i], lowcut, highcut, fs, order=6)
        plot(data[:, i], filterdData, lowcut, highcut, i)

    # show plots
    plt.show()

    # send filterd data back to node
    for f in filterdData:
        print(f)


def plot(data, filteredData, lowcut, highcut, channel):
    # Plot original and filtered data
    plt.figure(channel)
    plt.subplot(211)
    plt.title('Channel %s - No Filter' % (channel + 1))
    plt.plot(data, label="Original Data")
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.legend(loc='upper right')
    plt.grid(True)

    plt.subplot(212)
    plt.title('Channel %s - Bandpass Filter %d - %d Hz' % (channel + 1, lowcut, highcut))
    plt.plot(filteredData, label="Filterd Data", color='r')
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.grid(True)
    plt.legend(loc='upper right')


# start process
if __name__ == '__main__':
    main()

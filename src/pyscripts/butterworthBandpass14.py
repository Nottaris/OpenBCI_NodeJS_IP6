from scipy.signal import butter, lfilter
import sys, numpy as np, matplotlib.pyplot as plt


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
    lines = []
    for line in sys.stdin:
        lines.append(float(line))

    # create a numpy array
    data = np.array(lines)

    # filter data
    filteredData = butter_bandpass_filter(data, lowcut, highcut, fs, order=6)

    # send filtered data back to node
    for f in filteredData:
        print(f)

    # plot if needed
    #plot(data, filteredData, lowcut, highcut)

def plot(data, filteredData, lowcut, highcut):
    # Plot original and filtered data
    plt.figure(1)
    plt.subplot(211)
    plt.title('Eye Blink - No Filter')
    plt.plot(data, label="Original Data")
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.legend(loc='upper right')
    plt.grid(True)

    plt.subplot(212)
    plt.title('Eye Blink - Bandpass Filter %d - %d Hz' % (lowcut, highcut))
    plt.plot(filteredData, label="Filterd Data", color='r')
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.grid(True)
    plt.legend(loc='upper right')
    axes = plt.gca()
    axes.set_ylim([-4000, 4000])

    plt.show()


#start process
if __name__ == '__main__':
    main()

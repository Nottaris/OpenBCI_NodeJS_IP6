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
    # Define sample rate and desired cutoff frequencies (in Hz).
    fs = 250.0
    lowcut = 1
    highcut = 16.0
    order = 2
    slotSize = 125  # 0.5s

    # get our data as an array from read_in() and creat np array
    datainput = sys.stdin.read()
    data = np.array(json.loads(datainput))

    # filter and plot data
    filterData(data[:, 0], lowcut, highcut, fs, order, slotSize)


def filterData(data, lowcut, highcut, fs, order, slotSize):
    # filter data with butter bandpass
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)

    avgData = [filterdData[0]]
    subBaseline = []
    tempData = []
    count = 0

    # Calculate mean value for slots
    for sample in filterdData:
        if (count < slotSize):
            tempData.append(sample)
            count += 1
        else:
            # Add avg value from slot to last value
            avg = avgData[-1] + np.mean(tempData)
            for i in range(slotSize):
                avgData.append(avg)
            count = 0
            tempData = []
        # subtract baseline from data
        subBaseline.append(sample - np.mean(filterdData))

    plot(filterdData, avgData, subBaseline, lowcut, highcut, 0, order)
    plt.show()
    print("done")
    # # filter data
    # for i in range(0, 8):
    #     filterdData = butter_bandpass_filter(data[:,i], lowcut, highcut, fs, order=6)
    #     plot(data[:, i], filterdData, lowcut, highcut, i)
    #
    # # show plots
    # plt.show()
    #
    # # send filterd data back to node
    # for f in filterdData:
    #     print(f)


def plot(filteredData, avgData, subBaslineData, lowcut, highcut, channel, order):
    # Plot original and filtered data
    plt.figure(channel)
    plt.subplot(311)
    plt.title('Channel %s - Bandpass Filter %d - %d Hz order %d' % (channel + 1, lowcut, highcut, order))
    plt.plot(filteredData, label="Filterd Data", color='r')
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.legend(loc='upper right')
    plt.grid(True)

    plt.subplot(312)
    plt.title('Avg Data - Bandpass Filter %d - %d Hz' % (lowcut, highcut))
    plt.plot(avgData, label="Avg Data", color='r')
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.grid(True)
    plt.legend(loc='upper right')

    plt.subplot(313)
    plt.title('subBaslineData Data - Bandpass Filter %d - %d Hz' % (lowcut, highcut))
    plt.plot(subBaslineData, label="subBaslineData Data", color='r')
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.grid(True)
    plt.legend(loc='upper right')


# start process
if __name__ == '__main__':
    main()

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
    highcut = 30.0

    # get our data as an array from read_in()
    lines = []
    for line in sys.stdin:
        lines.append(float(line))

    # create a numpy array
    data = np.array(lines)

    # filter data
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order=6)

    # send filterd data back to node
    # for f in filterdData:
    #     print(f)

    # Plot original and filtered data
    # plt.figure(1)
    # plt.subplot(211)
    # plt.title('Eye Blink FP1 - No Filter')
    # plt.plot(data[2500:4500]*1000000, label="Raw Data")
    # plt.ylabel('microVolts')
    # plt.xlabel('Samples')
    # plt.legend(loc='upper right')
    # plt.grid(True)
    #
    # plt.figure(2)
    # plt.subplot(212)
    # plt.title('Eye Blink FP1 - Bandpass Filter %d - %d Hz' % (lowcut, highcut))
    # plt.plot(filterdData[2500:4500]*1000000, label="Filterd Data", color='r')
    # plt.ylabel('microVolts')
    # plt.xlabel('Samples 250/s')
    # plt.grid(True)
    # plt.legend(loc='upper right')
    # axes = plt.gca()
    # axes.set_ylim([-4000, 4000])

    # Plot original and filtered data
    dataFilterd =data[1800:3300]
    baseline = data[1800:2800]
    std = np.std(baseline, dtype=np.float64)
    median = np.median(baseline)
    std = np.full((1, len(dataFilterd)), (median+std))
    median = np.full((1, len(dataFilterd)), median)
    stdArr =  std.flatten()
    print(stdArr)
    medianArr =  median.flatten()
    print(medianArr)
    plt.figure(3)
    plt.title('Blink FP1')
    plt.plot(dataFilterd, label="Raw Data", color='r')
    plt.plot(medianArr, label="Baseline 5s", color='g')
    plt.plot(medianArr, label="Median Baseline", color='b')
    plt.legend(loc='lower right')
    plt.ylabel('Volts')
    plt.xlabel('Samples 250/s')
    plt.grid(True)
    axes = plt.gca()
    # axes.set_ylim([0.078, 0.09])
    plt.show()
    print("Blink")


# start process
if __name__ == '__main__':
    main()

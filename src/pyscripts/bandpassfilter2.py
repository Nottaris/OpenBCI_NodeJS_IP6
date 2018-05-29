import numpy as np
import sys

## bandpass filter algo by https://plot.ly/python/fft-filters/#bandpass-filter

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return lines[0]


def bandpass(data):
    fL = 0.1
    fH = 0.3
    b = 0.08
    N = int(np.ceil((4 / b)))
    if not N % 2:
        N += 1  # Make sure that N is odd.
    n = np.arange(N)

    # low-pass filter
    hlpf = np.sinc(2 * fH * (n - (N - 1) / 2.))
    hlpf *= np.blackman(N)
    hlpf = hlpf / np.sum(hlpf)

    # high-pass filter
    hhpf = np.sinc(2 * fL * (n - (N - 1) / 2.))
    hhpf *= np.blackman(N)
    hhpf = hhpf / np.sum(hhpf)
    hhpf = -hhpf
    hhpf[(N - 1) / 2] += 1

    h = np.convolve(hlpf, hhpf)
    s = list(data[0])
    new_signal = np.convolve(s, h)
    return new_signal


def main():
    #get our data as an array from read_in()
    line = read_in()
    datastrings = line.split(",")
    data = map(float, datastrings)

    newdata = bandpass(data)

    #print
    #print("data: "+data.tostring()[0,10])
    #print("newdata: "+newdata.tostring()[0,10])

    sys.stdout(newdata.tostring())


#start process
if __name__ == '__main__':
    main()
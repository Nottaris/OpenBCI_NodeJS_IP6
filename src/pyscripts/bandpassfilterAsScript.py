import plotly as py
import plotly.graph_objs as go

import numpy as np
import pandas as pd
import scipy

from scipy import signal

data = pd.read_csv('/Users/mjair/Documents/GitHub/OpenBCI_NodeJS_IP6/data/data.txt')

df = data[0:10]

table = py.figure_factory.create_table.create_table(df)
py.plot(table, filename='wind-data-sample')

trace1 = go.Scatter(
    x=range(len(list(data[1]))),
    y=list(data[1]),
    mode='lines',
    name='Wind Data'
)

layout = go.Layout(
    showlegend=True
)

trace_data = [trace1]
fig = go.Figure(data=trace_data, layout=layout)
py.iplot(fig, filename='wind-raw-data-plot')


fL = 0.1
fH = 0.3
b = 0.08
N = int(np.ceil((4 / b)))
if not N % 2: N += 1  # Make sure that N is odd.
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
s = list(data[1])
new_signal = np.convolve(s, h)


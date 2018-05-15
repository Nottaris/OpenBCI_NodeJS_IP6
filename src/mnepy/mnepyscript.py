import mne
import numpy as np

# Generate some random data
data = np.random.randn(8, 1000)

# Initialize an info structure
info = mne.create_info(
    ch_names=['EEG1', 'EEG2', 'EEG3', 'EEG4', 'EEG5', 'EEG6', 'EEG7', 'EEG8'],
    ch_types=['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg'],
    sfreq=250
)

custom_raw = mne.io.RawArray(data, info)
print(custom_raw)

custom_raw.plot(block=True, lowpass=40)





# Generate some random data: 10 epochs, 8 channels, 2 seconds per epoch
sfreq = 100
data = np.random.randn(10, 8, sfreq * 2)

# Initialize an info structure
info = mne.create_info(
    ch_names=['EEG1', 'EEG2', 'EEG3', 'EEG4', 'EEG5', 'EEG6', 'EEG7', 'EEG8'],
    ch_types=['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg'],
    sfreq=sfreq
)

# Create an event matrix: 10 events with alternating event codes
events = np.array([
    [0, 0, 1],
    [1, 0, 2],
    [2, 0, 1],
    [3, 0, 2],
    [4, 0, 1],
    [5, 0, 2],
    [6, 0, 1],
    [7, 0, 2],
    [8, 0, 1],
    [9, 0, 2],
])

event_id = dict(smiling=1, frowning=2)

# Trials were cut from -0.1 to 1.0 seconds
tmin = -0.1

custom_epochs = mne.EpochsArray(data, info, events, tmin, event_id)

print(custom_epochs)

# We can treat the epochs object as we would any other
_ = custom_epochs['smiling'].average().plot(time_unit='s')


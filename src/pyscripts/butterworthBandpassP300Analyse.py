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
    lowcut = 1.0
    highcut = 30.0
    order = 2
    slotSize = 171 #0.5s

    # get our data as an array from read_in() and creat np array
    # datainput = sys.stdin.read()
    # data = np.array(json.loads(datainput))


    # Cycle 1
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD5_next.json') as f:
    #     dataJson = json.load(f)
    # baseline = getChannelData(dataJson, 0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD6_play.json') as f:
    #     dataJson = json.load(f)
    # baseline = np.concatenate([baseline,getChannelData(dataJson, 0)])
    # Volup
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD_volup.json') as f:
    #     dataJson = json.load(f)
    # dataCmd1=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD2_voldown.json') as f:
    #     dataJson = json.load(f)
    # dataCmd2=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD3_pause.json') as f:
    #     dataJson = json.load(f)
    # dataCmd3=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD4_prev.json') as f:
    #     dataJson = json.load(f)
    # dataCmd4=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD5_next.json') as f:
    #     dataJson = json.load(f)
    # dataCmd5=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD6_play.json') as f:
    #     dataJson = json.load(f)
    # dataCmd6=getChannelData(dataJson,0)

    # Cycle 2
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD5_next.json') as f:
    #     dataJson = json.load(f)
    # baseline = getChannelData(dataJson, 0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C1_CMD6_play.json') as f:
    #     dataJson = json.load(f)
    # baseline = np.concatenate([baseline,getChannelData(dataJson, 0)])
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD_volup.json') as f:
    #     dataJson = json.load(f)
    # dataCmd1=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD2_pause.json') as f:
    #     dataJson = json.load(f)
    # dataCmd2=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD3_voldown.json') as f:
    #     dataJson = json.load(f)
    # dataCmd3=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD4_prev.json') as f:
    #     dataJson = json.load(f)
    # dataCmd4=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD5_play.json') as f:
    #     dataJson = json.load(f)
    # dataCmd5=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD6_next.json') as f:
    #     dataJson = json.load(f)
    # dataCmd6=getChannelData(dataJson,0)

    # Cycle 3
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD5_play.json') as f:
    #     dataJson = json.load(f)
    # baseline = getChannelData(dataJson, 0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C2_CMD6_next.json') as f:
    #     dataJson = json.load(f)
    # baseline = np.concatenate([baseline,getChannelData(dataJson, 0)])
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD1_prev.json') as f:
    #     dataJson = json.load(f)
    # dataCmd1=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD2_voldown.json') as f:
    #     dataJson = json.load(f)
    # dataCmd2=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD3_pause.json') as f:
    #     dataJson = json.load(f)
    # dataCmd3=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD4_next.json') as f:
    #     dataJson = json.load(f)
    # dataCmd4=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD5_play.json') as f:
    #     dataJson = json.load(f)
    # dataCmd5=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD6_volup.json') as f:
    #     dataJson = json.load(f)
    # dataCmd6=getChannelData(dataJson,0)

    # Cycle 4
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD5_play.json') as f:
    #     dataJson = json.load(f)
    # baseline = getChannelData(dataJson, 0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C3_CMD6_volup.json') as f:
    #     dataJson = json.load(f)
    # baseline = np.concatenate([baseline,getChannelData(dataJson, 0)])
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C4_CMD1_volup.json') as f:
    #     dataJson = json.load(f)
    # dataCmd1=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C4_CMD2_pause.json') as f:
    #     dataJson = json.load(f)
    # dataCmd2=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C4_CMD3_next.json') as f:
    #     dataJson = json.load(f)
    # dataCmd3=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C4_CMD4_voldown.json') as f:
    #     dataJson = json.load(f)
    # dataCmd4=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C4_CMD5_play.json') as f:
    #     dataJson = json.load(f)
    # dataCmd5=getChannelData(dataJson,0)
    # with open('ex2/data-2018-6-21-17-51-07_Ex2_Run2_C4_CMD6_prev.json') as f:
    #     dataJson = json.load(f)
    # dataCmd6=getChannelData(dataJson,0)

    # Cycle 5
    with open('ex3/data-2018-6-22-11-47-41_cycle1_cmdvolup.json') as f:
        dataJson = json.load(f)
    baseline = getChannelData(dataJson, 0)
    with open('ex3/data-2018-6-22-11-47-41_cycle2_cmdnext.json') as f:
        dataJson = json.load(f)
    baseline = np.concatenate([baseline,getChannelData(dataJson, 0)])
    with open('ex3/data-2018-6-22-11-47-41_cycle2_cmdnext.json') as f:
        dataJson = json.load(f)
    dataCmd1=getChannelData(dataJson,0)
    with open('ex3/data-2018-6-22-11-47-41_cycle2_cmdpause.json') as f:
        dataJson = json.load(f)
    dataCmd2=getChannelData(dataJson,0)
    with open('ex3/data-2018-6-22-11-47-41_cycle2_cmdplay.json') as f:
        dataJson = json.load(f)
    dataCmd3=getChannelData(dataJson,0)
    with open('ex3/data-2018-6-22-11-47-41_cycle2_cmdprev.json') as f:
        dataJson = json.load(f)
    dataCmd4=getChannelData(dataJson,0)
    with open('ex3/data-2018-6-22-11-47-41_cycle2_cmdvoldown.json') as f:
        dataJson = json.load(f)
    dataCmd5=getChannelData(dataJson,0)
    with open('ex/data-2018-6-22-11-47-41_cycle2_cmdvolup.json') as f:
        dataJson = json.load(f)
    dataCmd6=getChannelData(dataJson,0)

    totalData=[]
    slotSize
    print(len(baseline))
    totalData = np.concatenate([totalData, baseline])
    totalData = np.concatenate([totalData, dataCmd1])
    totalData = np.concatenate([totalData, dataCmd2])
    totalData = np.concatenate([totalData, dataCmd3])
    totalData = np.concatenate([totalData, dataCmd4])
    totalData = np.concatenate([totalData, dataCmd5])
    totalData = np.concatenate([totalData, dataCmd6])
    print(len(totalData))
    totalDataFilterd = filterData(totalData,lowcut,highcut,fs,order)

    ## REMOVE BASELINE
    filterDataWithoutBaseline= totalDataFilterd[slotSize*2:]

    ## SPLIT DATA IN COMMAND EPOCHES
    dataP300_cmd1 = filterDataWithoutBaseline[:slotSize]
    dataP300_cmd2 = filterDataWithoutBaseline[slotSize:slotSize*2]
    dataP300_cmd3 = filterDataWithoutBaseline[slotSize*2:slotSize*3]
    dataP300_cmd4 = filterDataWithoutBaseline[slotSize*3:slotSize*4]
    dataP300_cmd5 = filterDataWithoutBaseline[slotSize*4:slotSize*5]
    dataP300_cmd6 = filterDataWithoutBaseline[slotSize*5:slotSize*6]

    ## GET RELEVANT DATA BETWEEN 250-450ms FOR EACH COMMAND
    # start = 62; # After 250ms
    # end = start+50; # After 450ms
    # dataP300_cmd1 = dataP300_cmd1[start:end]
    # dataP300_cmd2 = dataP300_cmd2[start:end]
    # dataP300_cmd3 = dataP300_cmd3[start:end]
    # dataP300_cmd4 = dataP300_cmd4[start:end]
    # dataP300_cmd5 = dataP300_cmd5[start:end]
    # dataP300_cmd6 = dataP300_cmd6[start:end]

    ## CALCULATE AMPLITUDE
    diff = []
    diff.append(np.max(dataP300_cmd1) - np.min(dataP300_cmd1))
    diff.append(np.max(dataP300_cmd2) - np.min(dataP300_cmd2))
    diff.append(np.max(dataP300_cmd3) - np.min(dataP300_cmd3))
    diff.append(np.max(dataP300_cmd4) - np.min(dataP300_cmd4))
    diff.append(np.max(dataP300_cmd5) - np.min(dataP300_cmd5))
    diff.append(np.max(dataP300_cmd6) - np.min(dataP300_cmd6))
    cmd = 1
    for val in diff:
        print(str(cmd)+" "+str(val))
        cmd += 1

    print("Found mean: " + str(np.mean(diff)))
    print("Found Max: "+str(np.max(diff)))

    ## PLOT DATA
    plt.figure(0)
    plot(totalDataFilterd[slotSize*2:],lowcut,highcut,order,"totalDataFilterd",1,'b')
    plt.figure(1)
    plot(dataP300_cmd1,lowcut,highcut,order,"volup",1,'b')
    plot(dataP300_cmd2,lowcut,highcut,order,"pause",1,'g')
    plot(dataP300_cmd3,lowcut,highcut,order,"down",1,'r')
    # plt.figure(2)
    plot(dataP300_cmd4,lowcut,highcut,order,"prev",1,'y')
    plot(dataP300_cmd5,lowcut,highcut,order,"play",1,'k')
    plot(dataP300_cmd6,lowcut,highcut,order,"next",1,'w')
    plt.show()

def getChannelData(data, channel):
    channelData=[]
    for val in data:
        channelData.append(val["channelData"][channel])
    return channelData

def filterData(data,lowcut,highcut,fs,order):
    #filter data with butter bandpass
    filterdData = butter_bandpass_filter(data, lowcut, highcut, fs, order)
    return filterdData

def plot(filteredData, lowcut, highcut, order,title,cmd,color):
    # Plot original and filtered data
    nr = 310+cmd
    plt.subplot(nr)
    plt.title(' Compare Commands P300 - (%d - %d Hz)' % (lowcut, highcut))
    plt.plot(filteredData, label=title, color=color)
    plt.ylabel('microVolts')
    plt.xlabel('Samples')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)


#start process
if __name__ == '__main__':
    main()
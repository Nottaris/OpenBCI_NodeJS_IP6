# OpenBCI Music Player
In this project, opportunities to control a web-based music player with an OpenBCI were evaluated. Different approaches – based on blinking, P300 and motor imagery, using common data processing as well as machine learning algorithms to analyse the EEG data are described. In the absence of laboratory conditions and by using available hardware, the concept of controlling the player by blinking was successfully implemented. Conceptually described and partially implemented are the concepts of P300 as well as training and detecting mental commands with motor imagery. 

### Documentation
[IP6-IIT15-bciMusicInterface-IW-MJ.pdf](/docs/IP6-IIT15-bciMusicInterface-IW-MJ.pdf) (German BSc Thesis)  
jsDoc can be found here: /docs/jsdoc/index.html


### Installation
1. Clone the source code:
``` git clone https://github.com/Nottaris/OpenBCI_NodeJS_IP6.git ```   
2. Install required node packages:  
``` npm install ``` 
3. Install python 3.6

## How to use it
To use this demo you need to start the musicplayer, connect the OpenBCI board and additonaly start the EEG Control that you would like to use.

### 1. Start Musicplayer
Run ``` npm run player ```  to start the react music player. 
With the dropdown in the title of the musicplayer you can switch between the player for Blink, P300 and Mind Control

### 2. Connect with OpenBCI Cyton Board
In every control folder is a app.js file prepared, where the board can be configured. 
```javascript
const boardSettings = {
    verbose: true,                                             //  Print out useful debugging events
    debug: false,                                              //  Print out a raw dump of bytes sent and received
    simulate: false,                                           // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, true, true, true, true, true, true, true],    // power down unused channel 1 - 8
    port: "COM3",                                              // COM Port OpenBCI dongle
    control: "blink"                                           // Control type
}
```

### 3. Start EEG Controls
Three different approaches where developed to control the music player with the OpenBCI Heasdset

* Blink control: ``` npm run blink ``` 

* P300 control - beta ``` npm run p300 ```

* Mind control - beta ``` npm run mind ``` 


#### Helpers
* Save Data ``` npm run save ``` - save eeg samples in json file
* Plot Data ``` npm run plot ``` - show plot http://localhost:8888/
* Stream Data ``` npm run stream ``` - stream eeg data to plot
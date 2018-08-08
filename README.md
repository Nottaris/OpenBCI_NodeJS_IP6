# OpenBCI NodeJS IP6
In this project 3 different approches were developed to control a web music player with a Brain Computer Interface. 

## Installation
1. Clone the source code:
``` git clone https://github.com/Nottaris/OpenBCI_NodeJS_IP6.git ```   
2. Install required node packages:  
``` npm install ``` 
3. Install python 3.6

# How to use it
To use this demo you need to start the musicplayer and additonaly start the EEG Control that you would like to use.

## 1. Start Musicplayer
Run ``` npm run player ```  to start the react music player. 
With the Dropdown in the title of the musicplayer you can switch between the player for Blink, P300 and Mind Control

## 2. Connect with OpenBCI Cyton Board
In every control folder is a app.js file prepared, where the board can be configured. 
```javascript
const boardSettings = {
    verbose: true,                                              //  Print out useful debugging events
    debug: false,                                               //  Print out a raw dump of bytes sent and received
    simulate: false,                                            // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, true, true, true, true, true, true, true],    // power down unused channel 1 - 8
    port: "COM3",                                              // COM Port OpenBCI dongle
    control: "blink"                                            // Control type
}
```

## 3. Start EEG Controls
3 different approaches where developed to control the music player with the OpenBCI Heasdset

#### Blink control
``` npm run blink ``` 

#### P300 control - beta
``` npm run p300 ```

#### Mind control - beta
``` npm run mind ``` 


### Helpers
#### Save Data
``` npm run save ``` 
#### Plot Data
``` npm run plot ``` 

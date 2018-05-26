/**
 * extract p300 from eeg signal
 *
 */

module.exports = {
    getP300: function (sample) {
        digestSamples(sample);
    },
    getSettings,
    setSettings,
    reset
}

const commands = [
    "play",
    "pause",
    "next",
    "prev",
    "volup",
    "voldown",
    "play"
];

var currentCommand = "play";

const detectP300 = require('./detectP300');

const defaultSettings  = {
    channel: 5,                 // number of channel ( from 1 to 8 ) 5 === yellow Cz (middle top head)
    sampleRate: 250,            // 250Hz
    slots: 150,                  // data points per slot ( 600ms === 150 )
    threshold: 1.2,              // deviation factor
    debug: true                  // show console.log
}

let volts = [];
let count = 0;
let settings = defaultSettings;

function digestSamples(sample) {


    if (count < settings.slots) {
        volts.push(Number((sample.channelData[settings.channel-1] * 1000000).toFixed(20))); //microVolts
        count++;
    } else if (count >= settings.slots) {

        detectP300.getVEP(volts, currentCommand);
        setNextCommand();
        volts = [];
        count = 0;
    }
}


function setNextCommand() {
    let idx = commands.indexOf(currentCommand);
    currentCommand = commands[idx + 1];
}


function getSettings(){
    return settings;
}

function setSettings(newSettings) {
    settings =  newSettings ;
}

function reset(){
     settings = defaultSettings;
     count = 0;
     volts = [];
}

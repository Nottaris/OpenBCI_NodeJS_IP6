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
    "prev",
    "play",
    "next",
    "voldown",
    "pause",
    "volup",
    "prev"
];

var currentCommand = "play";

const detectP300 = require('./detectP300');
const server = require('./server');

const defaultSettings  = {
    channel: 5,                 // number of channel ( from 1 to 8 ) 5 === yellow Cz (middle top head) for p300
    sampleRate: 250,            // 250Hz
    slots: 150,                  // data points per slot ( 600ms === 150 )
    threshold: 2,              // deviation factor
    debug: true                  // show console.log
}

let volts = [];
let count = 0;
let settings = defaultSettings;

function digestSamples(sample) {

    // fetch 600ms of samples from channel 5
    if (count < settings.slots) {
        volts.push(Number((sample.channelData[settings.channel-1] * 1000000).toFixed(20))); //microVolts
        count++;
    } else if (count >= settings.slots) {
        //send past 600ms and past command to evaluate
        detectP300.getVEP(volts, currentCommand);

        //send next command to flash on player
        setNextCommand();
        server.sendCmd(currentCommand);

        // reset
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

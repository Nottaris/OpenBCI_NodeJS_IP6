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

const defaultSettings  = {
    channel: 5,                 // number of channel ( from 1 to 8 ) 5 === yellow Cz (middle top head) for p300
    sampleRate: 250,            // 250Hz
    slots: 150,                  // data points per slot ( 600ms === 150 )
    threshold: 1.2,              // deviation factor
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
        //send to evaluate
        detectP300.getVEP(volts, currentCommand);
        setNextCommand();
        sendCmd(currentCommand);
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

//******** send command to player via socket.io ************

const http = require('http');
let io;
let app;

(function start(){
    // create socket server on port 3001
    app = http.createServer(function(req, res) {});
    io = require('socket.io').listen(app);
    app.listen(3001, function(){
        console.log('listening on *:3001');
    });
})();

function sendCmd(command) {
    //emmit command event for each
    io.emit('command', { command: command });
    process.stdout.write("sending commands...\r");
}
//**********************************************************

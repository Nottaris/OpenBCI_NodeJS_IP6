/**
 * extract MindCmd from eeg signal
 *
 */

module.exports = {
    getMind: function (sample) {
        digestSamples(sample);
    },
    reset
}

const server = require('../socket/server');
const detectMind = require('./detectMind');

const defaultSettings = {
    sampleRate: 250,        // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    debug: true             // show console.log
}

let volts = [];
let count = 0;
let settings = defaultSettings;

server.startSocketServer();

function getCmdTimefromPlayer(data) {
    //console.log("from player: " + data.command + " " + data.time);
};

server.subscribeToCmds(getCmdTimefromPlayer);


function digestSamples(sample) {
    // fetch samples for slottime from all channels
    if (count < settings.slots) {
        //save channel data
        volts.push({
            channelData: sample.channelData
        });
        count++;
    } else if (count >= settings.slots) {
        //send data to evaluate
        detectMind.detectMind(volts);
        // reset
        volts = [];
        count = 0;
    }
}


function reset() {
    settings = defaultSettings;
    count = 0;
    volts = [];
}

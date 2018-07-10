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
const fs = require('fs');

const defaultSettings = {
    sampleRate: 250,        // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    debug: true,             // show console.log
    trainingSampleSize: 250      // 1 minute = 1000ms = 250 samples
}

let volts = [];
let count = 0;
let settings = defaultSettings;
let trainingCmd = "none";
let trainingOn = false;

server.startSocketServer();

function getTrainingCmd(data) {
    console.log("mind got training cmd from player: " + data.command);
    //reset
    volts = [];
    count = 0;
    trainingCmd = data.command;
    trainingOn = true;
};

server.subscribeToTrainingCmds(getTrainingCmd);


function digestSamples(sample) {
    //if trainingOn collect samples for trainingtime and save to file
    if (trainingOn) {
        // training mode:
        // fetch samples for slottime from all channels
        if (count < settings.trainingSampleSize) {
            //save channel data
            volts.push({
                channelData: sample.channelData
            });
            count++;
        } else {
            // reset
            trainingOn = false;
            //save to file
            let record = JSON.stringify(volts);
            fs.writeFile("data/mind/training-" + trainingCmd + ".json", record, ()=>console.log("training file for "+trainingCmd+" written"));
        }
    } else {
        // live detection mode:
        // fetch samples for slottime from all channels
        if (count < settings.slots) {
            //save channel data
            volts.push({
                channelData: sample.channelData
            });
            count++;
        } else {
            //send data to evaluate
            detectMind.detectMind(volts);
            // reset
            volts = [];
            count = 0;
        }
    }
}

//used by testing
function reset() {
    settings = defaultSettings;
    count = 0;
    volts = [];
}

/**
 * use mind to control musicplayer
 *
 */

module.exports = {
    getMind: function (sample) {
        digestSamples(sample);
    },
    getSettings,
    setSettings,
    reset
}

const server = require('../socket/server');
const detectMind = require('./detectMind');
const trainMind = require('./trainMind');
const fs = require('fs');

const defaultSettings = {
    sampleRate: 250,        // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    debug: true,             // show console.log
    //TODO: set correct trainingSampleSize 15000 ; 1500 samples = 6sec. is for dev
    trainingSampleSize: 1500      // 1 minute = 60 sec. = 60000ms = 15000 samples
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
            fs.writeFile("data/mind/training-" + trainingCmd + ".json", record, processTrainingsData(trainingCmd) );
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


//init processing of trainings data in callback of file write
function processTrainingsData(trainingCmd) {
    console.log("training file for "+trainingCmd+" written");
    trainMind.trainMind(trainingCmd);
}

//used by testing

function getSettings() {
    return settings;
}

function setSettings(newSettings) {
    settings = newSettings;
}

function reset() {
    settings = defaultSettings;
    count = 0;
    volts = [];
}

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
    debug: true             // show console.log
}

let volts = [];
let trainvolts = [];
let count = 0;
let settings = defaultSettings;
let trainingCmd = "none";
let slotsize = 1000;

server.startSocketServer();

function getTrainingCmd(data) {
    console.log("mind got training cmd from player: " + data.command.command);
    //reset
    trainingCmd = data.command.command;
    slotsize = data.command.slots;

    saveTrainingData();
};

server.subscribeToTrainingCmds(getTrainingCmd);


function digestSamples(sample) {
    // live detection mode:
    // fetch samples for slottime from all channels
    if (count < settings.slots) {
        //save channel data
        volts.push({
            channelData: sample.channelData
        });
        trainvolts.push({
            channelData: sample.channelData
        });
        count++;
         process.stdout.write("trainvolts.length: "+trainvolts.length+"\r");
    } else {
        //send data to evaluate
        detectMind.detectMind(volts);
        // reset
        volts = [];
        count = 0;
    }
    // downsize trainvolts
    if (trainvolts.length > 2000000) {
        trainvolts = trainvolts.slice(2000000 * 0.5);
    }
}

//on trainingCmd save samples for past trainingtime to file
function saveTrainingData() {
    // get latest samples for slottime from all channels
    console.log("trainvolts: "+trainvolts.length);
    sendvolts = trainvolts.slice(-slotsize);
    console.log("sendvolts: "+sendvolts.length);
    //save to file
    let values = sendvolts.map(v => v.channelData);
    let record = JSON.stringify(values);
    fs.writeFile("data/mind/training-" + trainingCmd + ".json", record, processTrainingsData(trainingCmd));
}


//init processing of trainings data in callback of file write
function processTrainingsData(trainingCmd) {
    console.log("training file for " + trainingCmd + " written");
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

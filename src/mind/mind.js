/**
 * mind control
 * fetch eeg data, init training of ml
 *
 */

module.exports = {
    getMind: function (sample) {
        digestSamples(sample);
    },
    getSettings,
    setSettings,
    reset
};

const server = require("../socket/server");
const detectMind = require("./detectMind");
const trainMind = require("./trainMind");
const fs = require("fs");


const defaultSettings = {
    sampleRate: 250,        // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    trainvoltsMaxLength: 2000000,
    slotsize: 1000,
    debug: true             // show console.log
};

let volts = [];
let trainvolts = [];
let count = 0;
let settings = defaultSettings;
let trainingCmd = "none";
let baseline = false;

server.startSocketServer();
server.subscribeToTrainingCmds(getTrainingCmd);


/**
 * receive training commands with slotsize, or training init from GUI
 *
 */
function getTrainingCmd(data) {
    console.log("mind got training cmd from player: " + data.command.command);
    //get cmd and slotsize
    trainingCmd = data.command.command;
    settings.slotsize = data.command.slots;
    //if init Training command is comming start training of ml
    if (trainingCmd === "init") {
        initTraining();
    } else {   //if a cmd is comming save volts in file
        saveTrainingData();
    }
}

/**
 * process data from openbci board
 *
 */
function digestSamples(sample) {
    // fetch samples for slottime from all channels
    if (count < settings.slots) {
        //save channel data for live detecion
        volts.push({
            channelData: sample.channelData
        });
        //save channel data for training
        trainvolts.push({
            channelData: sample.channelData
        });
        count += 1;
    } else {
        //send data to evaluate
        detectMind.detectMind(volts);
        // reset
        volts = [];
        count = 0;
    }
    // downsize trainvolts
    if (trainvolts.length > settings.trainvoltsMaxLength) {
        trainvolts = trainvolts.slice(settings.trainvoltsMaxLength * 0.5);
    }
}


/**
 * on trainingCmd save samples for past trainingtime to file
 *
 */
function saveTrainingData() {
    // get latest samples for slottime from all channels
    console.log("trainvolts: " + trainvolts.length);
    let sendvolts = trainvolts.slice(-settings.slotsize);
    console.log("sendvolts: " + sendvolts.length);

    //save to file
    let values = sendvolts.map((v) => v.channelData);
    let record = JSON.stringify(values);
    fs.writeFile("data/mind/training-" + trainingCmd + ".json", record, reportTrainingsData(trainingCmd));
    // Save baseline
    if (!baseline) {
        if (trainvolts.length > 3 * settings.slotsize) {
            let baselinevolts = trainvolts.slice(-3 * settings.slotsize, -settings.slotsize);
            console.log("baseline: " + baselinevolts.length);
            //save to file
            let baselineValues = baselinevolts.map((v) => v.channelData);
            let baselineRecord = JSON.stringify(baselineValues);
            fs.writeFile("data/mind/training-baseline.json", baselineRecord, reportTrainingsData("baseline"));
            baseline = true;
        }
    }

}


/**
 * report file write in callback of file write
 *
 */
function reportTrainingsData(trainingCmd) {
    console.log("training file for " + trainingCmd + " written");
}


/**
 * init processing of trainings data
 *
 */
function initTraining() {
    console.log("training started");
    trainMind.trainMind();
}

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

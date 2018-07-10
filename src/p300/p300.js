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


const server = require('../socket/server');
const detectP300 = require('./detectP300v4');

const defaultSettings = {
    channel: 1,             // number of channel ( from 1 to 8 ) 1 === OZ for p300
    sampleRate: 250,        // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    threshold: 1.8,         // deviation factor
    //ToDO: Set correct baselineLength
    baselineLength: 50,    // baseline 3s = 750 samples
    voltsMaxLength: 10000,  //max length of volts array
    commands: ['playpause','next','prev','volup', 'voldown'],
    debug: true             // show console.log
}

let volts = [];
let timestamps = [];
let count = 0;
let cycles = 3; //nr of cycles that will be analysed
let settings = defaultSettings;
var currentCommand; //cmd player is showing
var currentTime; //time player showed cmd
var counter = 0;
var startIdx = 0;
var endIdx = 0;

// timpestamp of each cmd
var cmdTimestamps = {
    playpause: [],
    next: [],
    prev: [],
    volup: [],
    voldown: []
};


server.startSocketServer();

function getCmdTimefromPlayer(data) {
    currentCommand = data.command;
    currentTime = data.time;


    if (settings.baselineLength < volts.length && typeof currentCommand !== 'undefined') {
        //console.log("from player: " + data.command + " " + data.time+" "+volts.length+" "+getIdxForTimestamp(timestamps, currentTime));
        if (!enoughDataForP300(cmdTimestamps, settings.commands, cycles)) {
            //Add current timestamp to cmd array
            cmdTimestamps[currentCommand].push(currentTime);

        } else {
            var compareCmd = [];
            var firstTimestamps = [];

            //save first timestampe as startidx
            settings.commands.forEach(function (cmd) {
                firstTimestamps.push(cmdTimestamps[cmd][0]);
            });

            //get first timestamp
            startTime = firstTimestamps.sort()[0];
            startIdx = getIdxForTimestamp(timestamps, startTime.toString().slice(0, -1));
            console.log("Search for P300 startIdx: " + startIdx + " " + currentTime);

            //save timestamps that will be analysed for p300 and remove them from cmdTimestamps Object
            settings.commands.forEach(function (cmd, i) {
                compareCmd[i] = cmdTimestamps[cmd].splice(0, cycles);
            });

            //get volts between startIdx and the end of volts array
            voltsForCycles = volts.slice(startIdx - 1);

            //get timestamp from startIdx until the end of timestamp array (buffer 10 samples)
            timestampesForCycles = timestamps.slice(startIdx - 1);

            //Analayse data for P300
            detectP300.getVEP(voltsForCycles, timestampesForCycles, compareCmd);

            // downsize volts and timestamp array
            if (volts.length > settings.voltsMaxLength) {
                volts = volts.slice(settings.voltsMaxLength * 0.75);
                timestamps = timestamps.slice(settings.voltsMaxLength * 0.75);
            }

            //Add current timestamp to cmdTimestamp array
            cmdTimestamps[currentCommand].push(currentTime);

            //reset
            startTime = 0;
            firstTimestamps = [];
        }
    } else {
        process.stdout.write("waiting for baseline...\r");
    }

};

server.subscribeToCmds(getCmdTimefromPlayer);

// process data from openbci board
function digestSamples(sample) {
    //save timestamp foreach sample
    timestamps.push(sample.timestamp.toString().slice(0, -1));
    //save volts for each sampple
    volts.push(Number(sample.channelData[settings.channel - 1]));
}



// find timestamp idx in timestamp array
function getIdxForTimestamp(timestamps, currentTime) {
    return timestamps.findIndex(timestamp => timestamp === currentTime);
}

// check if for each cycles data are in every command
function enoughDataForP300(cmdTimestamps, commands, compareCycles) {
    return commands.filter(cmd => cmdTimestamps[cmd].length >= compareCycles).length === commands.length;
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

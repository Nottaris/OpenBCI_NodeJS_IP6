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
};


const server = require('../socket/server');
const detectP300 = require('./detectP300v4');

const defaultSettings = {
    channel: 1,             // number of channel ( from 1 to 8 ) 1 === OZ for p300
    sampleRate: 250,        // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    threshold: 1.8,         // deviation factor
    //ToDo: Set correct baselineLength
    baselineLength: 10,    // baseline 3s = 750 samples
    voltsMaxLength: 20000,  //max length of volts array
    cycles: 2,              //nr of cycles that will be analysed
    commands: ['playpause','next','prev','volup', 'voldown'],
    debug: true             // show console.log
};

let volts = [];
let timestamps = [];
let count = 0;

let settings = defaultSettings;
let currentCommand; //cmd player is showing
let currentTime; //time player showed cmd
let counter = 0;
let startIdx = 0;
let once = true;
// timpestamp of each cmd
let cmdTimestamps = {
    playpause: [],
    next: [],
    prev: [],
    volup: [],
    voldown: []
};


server.startSocketServer();

function getCmdTimefromPlayer(data) {
    currentCommand = data.command;
    currentTime = data.time.toString().slice(0, -1);
    //ToDo: Remove once, only for testing
    if (once && settings.baselineLength < volts.length && typeof currentCommand !== 'undefined') {

        if (!enoughDataForP300(cmdTimestamps, settings.commands, settings.cycles)) {
            //Add current timestamp to cmd array
            cmdTimestamps[currentCommand].push(currentTime);
        } else {

            let voltsForCycles = volts.slice(0); //clone
            let timestampesForCycles = timestamps.slice(0);//clone

            let compareCmd = []; //timestamps that will be analysed for p300 and removed them from cmdTimestamps Object
            let firstTimestampe = []; //timestamps of first cycle

            settings.commands.forEach(function (cmd, i) {
                firstTimestampe.push(cmdTimestamps[cmd][0]);
                compareCmd[i] = cmdTimestamps[cmd].splice(0, settings.cycles);
            });

            //get smallest timestamp and use it as startIdx
            let startTimestamp = firstTimestampe.sort()[0];
            startIdx = getIdxForTimestamp(timestampesForCycles, startTimestamp);

            if(startIdx>0) {
                //get volts between startIdx and the end of volts array
                voltsForCycles = voltsForCycles.slice(startIdx);
                //get timestamp from startIdx until the end of timestamp array (buffer 10 samples)
                timestampesForCycles = timestampesForCycles.slice(startIdx);

                console.log("startIdx "+startIdx+" "+startTimestamp+" timestamp for cycle: "+timestampesForCycles[0]+" votls.length "+volts.length);

                //Analayse data for P300
                detectP300.getVEP(voltsForCycles, timestampesForCycles, compareCmd);
                once = false


            } else {
                console.log("!!! No index for startIdx timestamp was found " + startTimestamp+": timestampArray:"+timestampesForCycles[0]);
            }


            //reset
            counter = 0;
            voltsForCycles = [];
            timestampesForCycles = [];

            //Add current timestamp to cmd array
            cmdTimestamps[currentCommand].push(currentTime);
        }
         counter += 1;
    } else {
        process.stdout.write("waiting for baseline...\r");
    }

}

server.subscribeToCmds(getCmdTimefromPlayer);

// process data from openbci board
function digestSamples(sample) {
    //save timestamp foreach sample
    timestamps.push(sample.timestamp.toString().slice(0, -1));
    //save volts for each sampple
    volts.push(Number(sample.channelData[settings.channel - 1]));

    // downsize volts and timestamp array
    if (volts.length > settings.voltsMaxLength) {
        volts = volts.slice(settings.voltsMaxLength * 0.6);
        timestamps = timestamps.slice(settings.voltsMaxLength * 0.6);
    }
}


// find timestamp idx in timestamp array
function getIdxForTimestamp(timestamps, currentTime) {
    return timestamps.findIndex(timestamp => timestamp === currentTime);
}
// // find timestamp idx in timestamp array
// function getIdxForTimestamp(times, time) {
//     let timesReverse = times;
//     timesReverse.reverse();
//     return timesReverse.length - timesReverse.findIndex(findIndexForTimestamp(time)) - 1;
// }

//find timestamp in sample that is equal to time from command
function findIndexForTimestamp(time) {
    return function (element) {
        return time === element.time;
    }
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

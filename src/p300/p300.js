/**
 * use p300 to control musicplayer
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


const server = require("../socket/server");
const detectP300 = require("./detectP300");

const defaultSettings = {
    sampleRate: 250,        // 250Hz
    baselineLength: 5000,    // baseline 3s = 750 samples
    voltsMaxLength: 100000,  //max length of volts array
    cycles: 5,              //nr of cycles that will be analysed together
    commands: ["playpause","next","prev","volup", "voldown"],
    debug: true             // show console.log
};

let settings = defaultSettings;
let volts = [];
let timestamps = [];
let currentCommand; //cmd player is showing
let currentTime; //time player showed cmd
let counter = 0;
let cycle = 0;
let startIdx = 0;

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

    //save cmd and timestamp from socket event
    currentCommand = data.command;
    currentTime = data.time.toString().slice(0, -1);

    if (settings.baselineLength < volts.length && typeof currentCommand !== "undefined") {
        //print cycle
        if(settings.debug) {
            if (counter % settings.cycles === 0) {
                cycle += 1;
                console.log("cycle " + cycle + " " + cmdTimestamps["playpause"]);
            }
        }

        if (!enoughDataForP300(cmdTimestamps, settings.commands, settings.cycles)) {
            //Add current timestamp to cmd array
            cmdTimestamps[currentCommand].push(currentTime);
        } else {

            let voltsForCycles = volts.slice(0); //clone
            let timestampesForCycles = timestamps.slice(0);//clone
            let baselineForCycles = [];
            let compareCmd = [];
            let firstTimestampe = []; //timestamps of first cycle

            settings.commands.forEach(function (cmd, i) {
                firstTimestampe.push(cmdTimestamps[cmd][0]);
                //compareCmd will be analysed for p300 and removed them from cmdTimestamps Object
                compareCmd[i] = cmdTimestamps[cmd].splice(0, settings.cycles);
            });

            //get smallest timestamp and use it as startIdx
            let startTimestamp = firstTimestampe.sort()[0];
            startIdx = getIdxForTimestamp(timestampesForCycles, startTimestamp);

            if (startIdx > 0) {

                baselineForCycles = voltsForCycles.slice(startIdx-settings.baselineLength,startIdx);

                //get volts between startIdx and the end of volts array
                voltsForCycles = voltsForCycles.slice(startIdx);
                
                //save timestamp from startIdx until the end of timestamp array
                timestampesForCycles = timestampesForCycles.slice(startIdx);
                 if(settings.debug) {
                     console.log("detect P300 startIdx " + startIdx + " " + startTimestamp + " voltsForCycles.length " + voltsForCycles.length + " voltes.length " + volts.length + " cycle " + cycle);
                 }
                //Analayse data for P300
                detectP300.detectP300(voltsForCycles, baselineForCycles, timestampesForCycles, compareCmd, server);

            } else {
                console.log("!!! No index for startIdx timestamp was found " + startTimestamp + ": timestampArray:" + timestampesForCycles[0]);
            }

            //reset
            counter = 0;

            //Add current timestamp to cmd array
            cmdTimestamps[currentCommand].push(currentTime);
        }
         counter += 1;
    }

}

server.subscribeToP300Cmds(getCmdTimefromPlayer);

// process data from openbci board
function digestSamples(sample) {

    if(volts.length<settings.baselineLength) {
        process.stdout.write("wait for baseline...\r");
    } else if(volts.length === settings.baselineLength) {
        process.stdout.write("START PLAYER         \n");
    }

    //save timestamp foreach sample
    timestamps.push(sample.timestamp.toString().slice(0, -1));

    //save volts for each sampple
    volts.push(sample.channelData);

    // downsize volts and timestamp array
    if (volts.length > settings.voltsMaxLength) {
        volts = volts.slice(settings.voltsMaxLength * 0.6);
        timestamps = timestamps.slice(settings.voltsMaxLength * 0.6);
    }
}

// find timestamp idx in timestamp array
function getIdxForTimestamp(timestamps, currentTime) {
    return timestamps.findIndex((timestamp) => timestamp === currentTime);
}

// check if for each cycles data are in every command
function enoughDataForP300(cmdTimestamps, commands, compareCycles) {
    return commands.filter((cmd) => cmdTimestamps[cmd].length > compareCycles).length === commands.length;
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
    volts = [];
}

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
    sampleRate: 250,             // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    threshold: 1.8,             // deviation factor
    debug: true             // show console.log
}

let volts = [];
let timestamps = [];
let count = 0;
let cycles = 3; //nr of cycles that will be analysed
let settings = defaultSettings;
var currentCommand; //cmd player is showing
var currentTime; //time player showed cmd

// index of in samples array for
var cmdIndex = {
        playpause: [],
        next: [],
        prev: [],
        volup: [],
        voldown: []
    };

var commands = [
    'playpause',
    'next',
    'prev',
    'volup',
    'voldown'
];
server.startSocketServer();

function getCmdTimefromPlayer(data) {
    currentCommand = data.command;
    currentTime = data.time;
    //console.log("from player: " + data.command + " " + data.time);
};

server.subscribeToCmds(getCmdTimefromPlayer);


function digestSamples(sample) {

    // fetch samples for slottime from requested channel
    if (count < settings.slots) {
        //save timestamp
        timestamps.push(sample.timestamp.toString().slice(0, -1));
        //save samples
        volts.push(Number(sample.channelData[settings.channel - 1] * 1000000));
        count++;
    } else if (count >= settings.slots && typeof currentCommand !== 'undefined') {

        if(typeof cmdIndex[currentCommand] !== "undefined"){
            timeindex = getSampleRow(currentTime);  //get index of currenttime / command
            console.log(currentCommand);
            console.log(timeindex);
            ///Wait until every cmd has enough data for given cycles
            if(!enoughDataForP300(cmdIndex,commands,cycles)) {
                 cmdIndex[currentCommand].push(timeindex);
            } else {
                  console.log(volts.length);
                  console.log(cmdIndex);

                    var compareCmd = [];
                    commands.forEach(function(cmd, i){
                        compareCmd[i] = cmdIndex[cmd].splice(0,cycles);
                    });
                    console.log(cmdIndex);

                  detectP300.getVEP(volts, compareCmd);
                  cmdIndex = [];
            }

        }



        // reset
        count = 0;
    }
}


// find timestamp in samples array
function getSampleRow(currentTime) {
    let timestampsReverse = timestamps.reverse();
    return timestampsReverse.length - timestampsReverse.findIndex(findIndexForTimestamp(currentTime.toString().slice(0, -1))) - 1;
}

//find timestamp in sample that is equal to time from command
function findIndexForTimestamp(currentTime) {
    return function (timestamp) {
        return timestamp === currentTime;
    }
}
// check if for each cycles data are in every command
function enoughDataForP300(cmdIndex,commands,compareCycles) {
    return commands.filter(cmd => cmdIndex[cmd].length > compareCycles).length === commands.length;
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

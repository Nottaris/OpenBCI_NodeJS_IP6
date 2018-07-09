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
const detectP300 = require('./detectP300v3');

const defaultSettings = {
    channel: 1,             // number of channel ( from 1 to 8 ) 1 === OZ for p300
    sampleRate: 250,             // 250Hz
    slots: 112,             // data points per slot ( 450ms === 112 )
    threshold: 1.8,             // deviation factor
    debug: true             // show console.log
}

let volts = [];
let count = 0;
let settings = defaultSettings;
var currentCommand; //cmd player is showing
var currentTime; //time player showed cmd

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
        //save channel data and timestamp
        volts.push({
            time: sample.timestamp.toString().slice(0, -1),
            sample: Number(sample.channelData[settings.channel - 1] * 1000000)
        }); //microVolts

        count++;
    } else if (count >= settings.slots) {
        //delete volts newer than command timestamp
        corvolts = Object.create(volts);     //clone
        timeforCommand = currentTime + 600;    //currentTime plus 600ms
        timeindex = getSampleRow(timeforCommand);  //get index of currenttime / command
        corvolts = corvolts.splice(timeindex, corvolts.length);     //cut of newer stuff
        samples = volts.map(a => a.sample); //throw away timestamps

        //send data to evaluate
        if(typeof currentCommand != 'undefined'){
             detectP300.getVEP(samples, currentCommand, currentTime);
        }


        // reset
        volts = [];
        count = 0;
    }
}


// find timestamp in samples array
function getSampleRow(time) {
    let voltsReverse = volts.reverse();
    return voltsReverse.length - voltsReverse.findIndex(findIndexForTimestamp(time.toString().slice(0, -1))) - 1;
}

//find timestamp in sample that is equal to time from command
function findIndexForTimestamp(time) {
    return function (element) {
        return time === element.time;
    }
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

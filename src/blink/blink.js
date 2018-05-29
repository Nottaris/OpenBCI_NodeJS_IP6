/**
 * extract blinks from eeg signal
 *
 * first approach: direct volt from channel 2
 * second approach: channel 1 -
 *
 * blinks last from 100 to 400ms in real
 * (EEG data: 20-40Hz)
 */

module.exports = {
    getBlinks: function (sample) {
        getSampleAverages(sample);
    },
    setBlinkcount,
    getBlinkcount,
    getSettings,
    setSettings,
    reset
}

const detectBlink = require('./detectBlink');
const server = require('./server');

const defaultSettings  = {
    baselineLengthSec: 5,       // time in seconds for baseline
    channel: 1,                 // number of channel ( from 1 to 8 )
    sampleRate: 250,            // 250Hz
    slots: 10,                  // data points per slot
    threshold: 1.5,              // deviation factor
    debug: true                  // show console.log
}



let averages = [];
let average;
let baseline  = [];
let count = 0;
let avgInterval = 0;
let blinkCount = 0;
let settings = defaultSettings;
let baselineSlots = settings.baselineLengthSec*settings.sampleRate/settings.slots; // number of slots in baseline (at 250Hz)
function getSampleAverages(sample) {

    baseline = getBaseline();

    if (count < settings.slots) {
        avgInterval = avgInterval+Number((sample.channelData[settings.channel-1] * 1000000).toFixed(20)); //microVolts
        count++;
    } else if (count === settings.slots) {
        averages.push(avgInterval/settings.slots);
        average = Number(avgInterval/settings.slots);
        count = 0;
        avgInterval = 0;

        //if baseline is at least 1250 samples (5 sec.) -> detect Blinks
        if(baseline.length*settings.slots>=settings.baselineLengthSec*settings.sampleRate) {
            detectBlink.compareAverages(baseline,average);
        } else {
            process.stdout.write("waiting for baseline...\r");
        }
    }

}

function getBaseline() {
    if(averages.length>baselineSlots+30){ //slip first 30 data points
        return averages.slice(-baselineSlots); // extract baseline form averages
    } else {
        return averages;
    }
}

function setBlinkcount(){
    blinkCount++;
}

function getBlinkcount(){
    return blinkCount;
}

function getSettings(){
    return settings;
}

function setSettings(newSettings) {
    settings =  newSettings ;
}


function setNextCommand() {
    let idx = commands.indexOf(currentCommand);
    currentCommand = commands[idx + 1];
}


function reset(){
     settings = defaultSettings;
     averages = [];
     average;
     baseline  = [];
     count = 0;
     avgInterval = 0;
     blinkCount = 0;
}

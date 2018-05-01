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
    getBlinkcount
}

const detectBlink = require('./detectBlink');

const baselineLengthSec = 5;      // time in seconds for baseline
const slots = 10;                 // data points per slot
const channel = 1;                // number of channel ( from 1 to 8 )
const sampleRate = 250;           // 250Hz
const baselineSlots = baselineLengthSec*sampleRate/slots; // number of slots in baseline (at 250Hz)


let averages = [];
let average;
let baseline  = [];
let count = 0;
let avgInterval = 0;
let blinkCount = 0;

function getSampleAverages(sample) {

    baseline = getBaseline();

    if (count < slots) {
        avgInterval = avgInterval+Number((sample.channelData[channel-1] * 1000000).toFixed(20)); //microVolts
        count++;
    } else if (count === slots) {
        averages.push(avgInterval/slots);
        average = Number(avgInterval/slots);
        count = 0;
        avgInterval = 0;

        //if baseline is at least 1250 samples (5 sec.) -> detect Blinks
        if(baseline.length*slots>=baselineLengthSec*sampleRate) {
            detectBlink.compareAverages(baseline,average,slots);
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
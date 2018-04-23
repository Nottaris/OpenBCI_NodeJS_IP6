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
    }
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
        }
    }

}

function getBaseline() {
    if(averages.length>baselineSlots){
        return averages.slice(10,10+baselineSlots); //skip first 10 data points to minimize error data at start
    } else {
        return averages;
    }
}

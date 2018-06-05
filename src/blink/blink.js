/**
 * extract blinks from eeg signal
 *
 *
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

const mathFunctions = require('../functions/mathFunctions');
//const saveData = require('../functions/saveData');
const detectBlink = require('./detectBlink');


const defaultSettings  = {
    baselineLengthSec: 5,       // time in seconds for baseline
    channel:           1,       // number of channel ( from 1 to 8 )
    sampleRate:      250,       // 250Hz
    slots:            10,       // data points per slot
    threshold:       1.085,       // deviation factor
    debug:          true        // show console.log
}

let data = [];
let medianValues = [];
let baseline = [];
let count = 0;
let blinkCount = 0;
let settings = defaultSettings;
let baselineReady = false;
let baselineSlots = settings.baselineLengthSec * settings.sampleRate / settings.slots; // number of slots in baseline (at 250Hz)

//saveData.getChannelDatafromJSON();

function getSampleAverages(sample) {

    let currentValue = Number((sample.channelData[settings.channel - 1] * 1000000)); //microVolts
    data.push(currentValue);

    if (count < settings.slots) {
        count++;
    } else {
        // detect Blinks (every 10 data points again, ==> every 40 ms)
        baseline = getBaseline();
        count = 0;

        //if baseline is at least 1250 samples (5 sec.)
        if (baselineReady) {

             let currentMedian = mathFunctions.getMedian(baseline);

            // console.log("  currentValue. \t" + currentValue.toFixed(0));
            // console.log("  currentMedian \t" + currentMedian.toFixed(0));

            // if current Value is much lower than currentMedian, somethings going on...
            if(currentValue*settings.threshold < currentMedian){
                 console.log("  ************* " + (currentValue.toFixed(0)-currentMedian.toFixed(0)));
                detectBlink.checkBaseline(baseline);
            }
        } else {
            process.stdout.write("waiting for baseline...\r");
        }
    }

}

// sliding window
function getBaseline() {

    if(!baselineReady && baseline.length >= baselineSlots) {
        baselineReady = true;
    }

    if (data.length > baselineSlots + 30) {   // skip first 30 data slots
        let slidingWindow = mathFunctions.clone(data);
        slidingWindow = slidingWindow.slice(-baselineSlots);    // extract baseline form data
        return slidingWindow;
    } else {
        return data;
    }
}

function setBlinkcount() {
    blinkCount++;
}

function getBlinkcount() {
    return blinkCount;
}

function getSettings() {
    return settings;
}

function setSettings(newSettings) {
    settings = newSettings;
}

function reset() {
    settings = defaultSettings;
    medianValues = [];
    baseline = [];
    count = 0;
    blinkCount = 0;
}

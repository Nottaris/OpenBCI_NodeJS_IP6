/**
 * extract blink-data from eeg signal
 *
 */

module.exports = {
    getBlinks,
    setBlinkcount,
    getBlinkcount,
    getSettings,
    setSettings,
    reset
};

const mathFunctions = require("../functions/mathFunctions");
const detectBlink = require("./detectBlink");

const defaultSettings = {
    baselineLengthSec: 5,       // time in seconds for baseline
    channel:           1,       // number of channel ( from 1 to 8 )
    sampleRate:      250,       // 250Hz
    slots:            10,       // samples per slot
    threshold:         3,       // deviation factor with paste upper bound
    flashInterval:  1500,       // interval in ms to flash commands in player
    skipAfterBlink:    5,       // number of slots skipped after blink
    commands:       ["prev","playpause","next","voldown", "volup"], // musicplayer commands
    debug:          true        // show console.log
};

let slotValues = [];
let medianValues = [];
let baseline = [];
let count = 0;
let blinkCount = 0;
let settings = defaultSettings;
let baselineSlots = settings.baselineLengthSec * settings.sampleRate / settings.slots; // number of slots in baseline (at 250Hz)

/**
 * fetch samples for baseline and send to detect if slotsize is fetched
 *
 */
function getBlinks(sample) {

    baseline = getBaseline();

    if (count < settings.slots) {
        slotValues.push(Number(sample.channelData[settings.channel - 1] * 1000000)); //microVolts
        count += 1;
    } else if (count === settings.slots) {
        let currentMedian = mathFunctions.getMedian(slotValues);
        medianValues.push(currentMedian);
        count = 0;
        slotValues = [];

        //if baseline is at least 1250 samples (5 sec.) -> detect Blinks
        if (baseline.length >= baselineSlots) {
            detectBlink.compareAverages(baseline, currentMedian);
        } else {
            process.stdout.write("waiting for baseline...\r");
        }
    }

}

/**
 * fetch baseline as sliding window
 *
 */
function getBaseline() {
    if (medianValues.length > baselineSlots + 30) {   // skip first 30 data slots
        let slidingWindow = mathFunctions.clone(medianValues);
        slidingWindow = slidingWindow.slice(-baselineSlots);    // extract baseline form medianValues
        return slidingWindow;
    } else {
        return medianValues;
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

/**
 * for testing
 *
 */
function reset() {
    settings = defaultSettings;
    medianValues = [];
    slotValues = [];
    baseline = [];
    count = 0;
    blinkCount = 0;
}
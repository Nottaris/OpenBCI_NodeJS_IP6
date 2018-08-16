/**
 * Blink Detection and flash, execute commands
 *
 */

module.exports = {
    compareAverages: detectBlink
};

const mathFunctions = require("../functions/mathFunctions");
const blink = require("./blink");
const server = require("../socket/server");

let settings;
let init = true;
let skip = 0;

let currentCommand = "prev";

/**
 * get median and standard deviation for baseline and start Blink Detection, log baseline
 * @params: baseline: Array of last window medians, currentMedian: current median to compare with baseline
 */
function detectBlink(baseline, currentMedian) {

    // get median and standard deviation for baseline
    let baselineMedian = mathFunctions.getMedian(baseline);
    let standardDeviation = mathFunctions.getStandardDeviation(baseline);

    // run inital setup for blink control
    if (init) {
        // get settings
        settings = blink.getSettings();

        // show Baseline data
        if (settings.debug) {
            console.log("=================Baseline=================");
            console.log("  Baseline size:\t" + baseline.length);
            console.log("  Baseline median:\t" + mathFunctions.getMedian(baseline).toFixed(2));
            console.log("  Variance:\t\t" + mathFunctions.getVariance(baseline).toFixed(2));
            console.log("  Standard deviation:\t" + mathFunctions.getStandardDeviation(baseline).toFixed(2));
            console.log("  median-standardDev*a:\t " + Number(baselineMedian - standardDeviation * settings.threshold).toFixed(2));
            console.log("  Max Value:\t\t" + mathFunctions.getMaxValue(baseline).toFixed(2));
            console.log("  Min Value:\t\t" + mathFunctions.getMinValue(baseline).toFixed(2));
            console.log("==============================================");
        }

        // start socket server
        server.startSocketServer();

        // flash commands in musicplayer
        startFlashCmd();

        init = false;
    }

    // Check if current median contains a blink
    findBlink(currentMedian, baselineMedian, standardDeviation);

}

/**
 * check if current median is a blink
 * @params: currentMedian: current median to compare with baseline, baselineMedian: median baseline samples, standardDeviation: standard deviation baseline samples,
 *
 */
function findBlink(currentMedian, baselineMedian, standardDeviation) {

    // if currentMedian is smaller then  median - standardDeviation * threshold  it will be classified as a blink
    if (Number(baselineMedian - standardDeviation * settings.threshold) > currentMedian && skip === 0) {
        if (settings.debug) {
            console.log("BLINK: \t value: " + currentMedian.toFixed(2) + "\t at " + new Date());
        }

        // increase blinkcount for mocha tests
        blink.setBlinkcount();

        // send current command to musicplayer to execute
        server.doBlinkCmd(currentCommand);

        // to prevent multiple classification for same blink skip next slots
        skip = settings.slots * settings.skipAfterBlink;
    }

    if (skip > 0) {
        skip -= 1;
    }
}

/**
 * interval for flashing icons in gui
 *
 */
function startFlashCmd() {
    setInterval(function () {
        //send next command to flash on player
        setNextCommand();
        server.sendCmd(currentCommand);
    }, settings.flashInterval);
}

/**
 * iterate through commands
 *
 */
function setNextCommand() {
    let idx = settings.commands.indexOf(currentCommand);
    if(idx >= settings.commands.length -1) {
        currentCommand = settings.commands[0];
    } else {
        currentCommand = settings.commands[idx + 1];
    }
}

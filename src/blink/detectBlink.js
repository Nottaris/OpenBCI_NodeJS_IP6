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
 * init Blink Detection, log baseline
 * @params: baseline: Array of last window medians, currentMedian: current median to compare with baseline
 */
function detectBlink(baseline, currentMedian) {

    let baselineMedian = mathFunctions.getMedian(baseline);
    let standardDeviation = mathFunctions.getStandardDeviation(baseline);

    if (init) {
        server.startSocketServer();
        //get Settings
        settings = blink.getSettings();

        //show Baseline
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
        startFlashCmd();
        init = false;
    }

    //if current value is bigger then  median - standardDeviation * threshold  it is a blink
    if (Number(baselineMedian - standardDeviation * settings.threshold) > currentMedian && skip === 0) {
        if (settings.debug) {
            console.log("BLINK: \t value: " + currentMedian.toFixed(2) + "\t at " + new Date());
        }
        blink.setBlinkcount();

        //send doCommand to execute
        server.doCmd(currentCommand);

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

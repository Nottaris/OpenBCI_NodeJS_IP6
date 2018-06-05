const mathFunctions = require('../functions/mathFunctions');
const blink = require('./blink');
const server = require('../socket/server');

module.exports = {
    compareAverages: detectBlink
};
var settings;
let init = true;
let skip = 0;
const commands = [
    "prev",
    "play",
    "next",
    "voldown",
    "pause",
    "volup",
    "prev"
];
let currentCommand = "play";

/*
 * init Blink Detection, log baseline
 * @params: baseline: Array of last window medians (slidingWindow), currentMedian: current median to compare with baseline
 */

function detectBlink(baseline, currentMedian) {

    //let baselineMedian = mathFunctions.getMedian(baseline);
    //let standardDeviation = mathFunctions.getStandardDeviation(baseline);
    let baselineMin = mathFunctions.getMinValue(baseline);
    let baselineMax = mathFunctions.getMaxValue(baseline);

    //get last 500ms window from baseline (which is 5 sec.)
    let window = mathFunctions.clone(baseline);
    window = window.splice(window.length*0.9);
    let windowMin = mathFunctions.getMinValue(window);
    let windowMax = mathFunctions.getMaxValue(window);


    if (init) {
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
            console.log("  -------");
            console.log("  First value to evaluate as current Median: \t\t");// + currentMedian.toFixed(2));
            console.log("  Min of last 500ms: \t\t" + windowMin.toFixed(2));
            console.log("  Max of last 500ms: \t\t" + windowMax.toFixed(2));
            console.log("==============================================");
        }else{
            startFlushCmd();
        }
        init = false;
    }

           // console.log("  Value to evaluate as current Median: \t\t" + currentMedian.toFixed(2));
           // console.log("  Min of last 500ms: \t\t" + baselineMin.toFixed(2));


    if (skip == 0){

        let diffinWindow = windowMax-windowMin;
        let diffBaseline = baselineMax-baselineMin;

        if(diffinWindow>diffBaseline){
            blinkFound();
        }

    }

    if (skip > 0) {
        skip--;
    }

}


function blinkFound() {

    if (settings.debug) {
        console.log("BLINK at " + new Date());
    }

    blink.setBlinkcount();

    //send doCommand to execute
    server.doBlinkCmd();

    skip = settings.slots * 5;
}


function startFlushCmd() {
    setInterval(function () {
        //send next command to flash on player
        console.log("send cmd"+currentCommand);
        setNextCommand();
        server.sendCmd(currentCommand);
    }, 1000);
}

function setNextCommand() {
    let idx = commands.indexOf(currentCommand);
    currentCommand = commands[idx + 1];
}


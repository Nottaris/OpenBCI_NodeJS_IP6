const mathFunctions = require('../functions/mathFunctions');
const blink = require('./blink');
const server = require('../socket/server');

module.exports = {
    checkBaseline: detectBlink
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

function detectBlink(baseline) {

    //get first 4500ms window from baseline (which is 5 sec.)
    let start = mathFunctions.clone(baseline);
    start = start.splice(0, baseline.length*0.9);
    let startMin = mathFunctions.getMinValue(start);
    let startMax = mathFunctions.getMaxValue(start);
    console.log("start size"+start.length);

    //get last 500ms window from baseline (which is 5 sec.)
    let end = mathFunctions.clone(baseline);
    end = end.splice(baseline.length*0.9, baseline.length*0.1);
    let endMin = mathFunctions.getMinValue(end);
    let endMax = mathFunctions.getMaxValue(end);
     console.log("end size"+end.length);

    if (init) {
        //get Settings
        settings = blink.getSettings();

        //show Baseline
        if (settings.debug) {
            console.log("=================Baseline=================");
            console.log("  Baseline size:\t" + baseline.length);
            console.log("  Max Value:\t\t" + mathFunctions.getMaxValue(baseline).toFixed(2));
            console.log("  Min Value:\t\t" + mathFunctions.getMinValue(baseline).toFixed(2));
            console.log("==============================================");
        }else{
            startFlushCmd();
        }
        init = false;
    }


    if (skip == 0){

        let diffend = endMax-endMin;
        let diffStart = startMax-startMin;

        console.log("  diffend \t\t" + diffend.toFixed(2));
        console.log("  diffStart \t\t" + diffStart.toFixed(2));

        if(diffend>diffStart){


        }
        console.log("  Blink MIN MAX Diff \t\t" + (diffend-diffStart).toFixed(2));
        blinkFound();

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


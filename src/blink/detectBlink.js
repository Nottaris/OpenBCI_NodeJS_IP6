module.exports = {
    compareAverages: detectBlinkOld
};

const mathFunctions = require('../functions/mathFunctions');
const blink = require('./blink');
const server = require('../socket/server');

let settings;
var init = true;
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
var currentCommand = "play";

/*
 * init Blink Detection, log baseline
 * @params: baseline: Array of last window medians, currentMedian: current median to compare with baseline
 */

function detectBlinkOld(baseline, currentMedian) {

    var baselineMedian = mathFunctions.getMedian(baseline);
    var standardDeviation = mathFunctions.getStandardDeviation(baseline);

    if (init) {
        server.startSocketServer();
        //get Settings
        settings = blink.getSettings();

        //show Baseline
        if(settings.debug) {
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
    if (Number(baselineMedian - standardDeviation * settings.threshold) > currentMedian && skip == 0 ) {
        if(settings.debug){
            console.log("BLINK: \t value: "+currentMedian.toFixed(2)+"\t at "+new Date());
        }
       blink.setBlinkcount();

       //send doCommand to execute
       server.doBlinkCmd();

       skip = settings.slots*5;
    }

    if(skip > 0) {
        skip--;
    }

}

function startFlashCmd(){
    setInterval(function(){
        //send next command to flash on player
        setNextCommand();
        server.sendCmd(currentCommand);
    }, 1500);
}

function setNextCommand() {
    let idx = commands.indexOf(currentCommand);
    currentCommand = commands[idx + 1];
}

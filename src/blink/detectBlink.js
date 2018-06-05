const mathFunctions = require('../functions/mathFunctions');
const blink = require('./blink');
const server = require('../socket/server');

module.exports = {
    compareAverages: detectBlink
};
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

function detectBlink(baseline, average) {

    var mean = mathFunctions.getAverage(baseline);
    var standardDeviation = mathFunctions.getStandardDeviation(baseline);

    if (init) {
        //get Settings
        settings = blink.getSettings();

        //show Baseline
        if(settings.debug) {
            console.log("=================Baseline=================");
            console.log("  Baseline size:\t" + baseline.length);
            console.log("  Average(mean):\t" + mathFunctions.getAverage(baseline).toFixed(2));
            console.log("  Variance:\t\t" + mathFunctions.getVariance(baseline).toFixed(2));
            console.log("  Standard deviation:\t" + mathFunctions.getStandardDeviation(baseline).toFixed(2));
            console.log("  mean-standardDev*a:\t " + Number(mean - standardDeviation * settings.threshold).toFixed(2));
            console.log("  Max Value:\t\t" + mathFunctions.getMaxValue(baseline).toFixed(2));
            console.log("  Min Value:\t\t" + mathFunctions.getMinValue(baseline).toFixed(2));
            console.log("==============================================");
        }
        startFlushCmd();
        init = false;
    }

    //if current value is bigger then  mean - standardDeviation * threshold  it is a blink
    if (Number(mean - standardDeviation * settings.threshold) > average && skip == 0 ) {
        if(settings.debug){
            console.log("BLINK: \t value: "+average.toFixed(2)+"\t at "+new Date());
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

function startFlushCmd(){
    setInterval(function(){
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


const mathFunctions = require('../functions/mathFunctions');
const p300 = require('./p300');

module.exports = {
    getVEP: detectP300
};

let settings;
var third = 50;
var init = true;
let skip = 0;
var vppx = {
    play: 0,
    pause: 0,
    next: 0,
    prev: 0,
    volup: 0,
    voldown: 0
};

function detectP300(volts, command) {

    if (init) {
        //get Settings
        settings = p300.getSettings();
        third = Math.floor(Number(volts.length / 3));
        init = false;
    }

    //600ms is volts; for min use 200-600ms L2; for max use 400-600ms L1
    let voltsL1 = volts.slice(third * 2);
    let voltsL2 = volts.slice(third);

    let max = mathFunctions.getMaxValue(voltsL1);
    let min = mathFunctions.getMinValue(voltsL2);

    let vpp = max - min;

    vppx[command] = vpp;

    if (skip <= 0) {
        getCommand();
    } else {
        skip--;
    }

}

function getCommand() {
    var command = "?";
    var maxVppx = mathFunctions.getMaxValue(Object.values(vppx));
    var average = mathFunctions.getAverage(Object.values(vppx));

    if (Number(maxVppx * settings.threshold) > average) {

        command = Object.keys(vppx).find(key => vppx[key] === maxVppx);

        if (settings.debug) {
            console.log("command: " + command);
            console.log("average: " + average);
            console.log("maxVppx: " + maxVppx);
            console.log("vppx[maxVppx]: " + Object.keys(vppx).find(key => vppx[key] === maxVppx));
        }
        console.log("p300: \t value: " + maxVppx.toFixed(2) + " on command: " + command + "\t at " + new Date());
        skip = settings.slots * 2;
        resetVppx();
    }
}


function resetVppx() {
    vppx = {
        play: 0,
        pause: 0,
        next: 0,
        prev: 0,
        volup: 0,
        voldown: 0
    };
}
module.exports = {
    getVEP: detectP300
};


const mathFunctions = require('../functions/mathFunctions');
const p300 = require('./p300');
const server = require('../socket/server');

var PythonShell = require('python-shell');

var settings;
var third = 50;
var counter = 0;
var init = true;
var filter = true;
var vppx = {
    play: 0,
    pause: 0,
    next: 0,
    prev: 0,
    volup: 0,
    voldown: 0
};
var nrOfCommands = Object.keys(vppx).length;
var voltsFiltered = [];

function detectP300(volts, command) {

    //skip init phase after first values are in
    if (init) {
        if(counter===0){
            //get Settings only once
            settings = p300.getSettings();
            third = Math.floor(Number(volts.length / 3));
        }
        if(counter===nrOfCommands){
            init = false;
        }
    }

    if(filter) {

        var pyshell = new PythonShell('/src/pyscripts/butterworthBandpass14.py');

        // received a message sent from the Python script (a simple "print" statement)
        pyshell.stdout.on('data', function (value) {
             //console.log(value);
             //get filtered data back
             voltsFiltered.push(value);
        });

        // sends channel data to the Python script via stdin
        volts.forEach(function(v) {
                pyshell.send(v);
        })

        // end the input stream and allow the process to exit
        pyshell.end(function (err) {
          if (err) throw err;
          console.log('finished');
        });

    }


    // volts is 600ms; for min use 200-600ms "L2"; for max use 400-600ms "L1"
    let voltsL1 = voltsFiltered.slice(third * 2);
    let voltsL2 = voltsFiltered.slice(third);

    let max = mathFunctions.getMaxValue(voltsL1);
    let min = mathFunctions.getMinValue(voltsL2);

    let vpp = max - min;

    // add value to dict prop command
    vppx[command] = vpp;
    counter++;

    //after all vppx are newly set again evaluate getCommand()
    if (!init  &&  counter % nrOfCommands === 0 ) {
       counter = 0;
       getCommand();
    }
}

function getCommand() {
    var command = "?";
    var maxVppx = mathFunctions.getMaxValue(Object.values(vppx));
    var median = mathFunctions.getMedian(Object.values(vppx));
    console.log("Object.values(vppx): " + Object.values(vppx));

    if (Number(maxVppx) > (median * settings.threshold)) {

        command = Object.keys(vppx).find(key => vppx[key] === maxVppx);

        if (settings.debug) {
            console.log("command: " + command +
                        "\t median: " + median +
                        "\t maxVppx: " + maxVppx +
                        "\t vppx[maxVppx]: " + Object.keys(vppx).find(key => vppx[key] === maxVppx));
        }
        console.log("p300: \t value: " + maxVppx.toFixed(2) + " on command: " + command + "\t at " + new Date());

        //send doCommand to execute
        server.doCmd(command);

    }
}

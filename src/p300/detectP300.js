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
var subBase = false;
var filter = true;
var vppx = {
    play: 0,
    pause: 0,
    next: 0,
    prev: 0,
    volup: 0,
    voldown: 0
};
var nrOfCommands = Object.keys(vppx).length;    // aka 6
var baselineVolts = [];


function detectP300(volts, command) {

    if(subBase){
        //add new values to baselineBuffer
        baselineVolts.concat(volts);
        //if baselineBuffer is larger than 12 times volts slot:
        //purge old values from baselineBuffer (remove first (oldest) slot)
        //calculate median and subtract it from current volts
        if (baselineVolts.length > volts.length*13) {
            baselineVolts.splice(0, volts.length);
            //subtract baselineMedian from each value in current slot
            let baselineMedian = mathFunctions.getMedian(baselineVolts);
            volts.map(volt => volt - baselineMedian);
        }
    }

    //skip init phase after first values are in
    if (init) {
        if(counter===0){
            //get Settings only once
            settings = p300.getSettings();
            third = Math.floor(Number(volts.length / 3));
        }
        //on last command coming in set init to false (counter = 5)
        if(counter===nrOfCommands-1){
            init = false;
        }
    }

    if(filter) {

        var voltsFiltered = [];
        const options = {mode: 'text'};
        let pyshell = new PythonShell('/src/pyscripts/butterworthBandpass14.py', options);
        let data = JSON.stringify(volts);

        // sends channel data to the Python script via stdin
        pyshell.send(data).end(function(err){
            if (err){
                console.log("pyshell send err: "+err)
            }
        });

        // received a message sent from the Python script (a simple "print" statement)
        pyshell.stdout.on('data', function (data) {
             //get filtered data back
             let rawdata = data.split(' ');
             for (let i = 0; i < rawdata.length; i++) {
                 if(rawdata[i].length>3 && !isNaN(rawdata[i])){
                    voltsFiltered.push(Number(rawdata[i]));
                 }
             }
        });

        // end the input stream and allow the process to exit
        pyshell.end(function (err) {
          if (err) throw err;
          processP300(voltsFiltered, command);
          voltsFiltered = [];
        });

    }else{
        //not filtered
        processP300(volts, command);
    }
}

function processP300(voltsF, command){
    if(voltsF.length>0){

        // volts is 600ms; for min use 200-600ms "L2"; for max use 400-600ms "L1"
        let voltsL1 = voltsF.slice(third * 2);
        let voltsL2 = voltsF.slice(third);

        let max = mathFunctions.getMaxValue(voltsL1);
        let min = mathFunctions.getMinValue(voltsL2);

        let vpp = max - min;

        // add value to dict prop command
        vppx[command] = vpp;
        counter++;

        //after all vppx are newly set again evaluate getCommand()
        if (!init  &&  (counter % nrOfCommands === 0) ) {
           counter = 0;
           getCommand();
        }
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

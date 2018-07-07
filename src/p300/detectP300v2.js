module.exports = {
    getVEP: detectP300
};


const mathFunctions = require('../functions/mathFunctions');
const p300 = require('./p300');
const server = require('../socket/server');

var PythonShell = require('python-shell');

var settings;
var counter = 0;
var init = true;
var subBase = true;
var baselineReady = false;
var vppx = {
    playpause: 0,
    next: 0,
    prev: 0,
    volup: 0,
    voldown: 0
};
//volts per cmd, append up to 5 cycles each
var volts5 = {
    playpause: [],
    next: [],
    prev: [],
    volup: [],
    voldown: []
};
//averaged volts per cmd
var avgVolts5 = {
    playpause: [],
    next: [],
    prev: [],
    volup: [],
    voldown: []
};
var commands = [
    'playpause',
    'next',
    'prev',
    'volup',
    'voldown'
];
var nrOfCommands = commands.length;    // aka 5
var baselineVolts = [];


function detectP300(volts, command, time) {
    //console.log(volts);
    //console.log("cmd v2 "+command);
    //console.log("time v2 "+time);

    if (init) {
        if (counter === 0) {
            //get Settings only once
            settings = p300.getSettings();
        }
        //after 5 cycles of 5 cmds each = 50 -> counter > 55
        if (counter > 55) {
            init = false;
        }
    }
    counter++;

    //collect volt values sorted by cmd
    volts5[command].push(volts);
    console.log(counter + "cmd: " + command + " volts5[command].length: " + volts5[command].length)

    //if init is over (after 10 cycles aka counter 50) generate baseline
    if (!init) {
        //generate sliding window baseline values (median over every cmd and over 5 cycles)
        commands.forEach(cmd => {
            let cyclecount = volts5[cmd].length; //how many cycles of this cmd are present in volts5
            if (volts5.hasOwnProperty(cmd)) {
                if (cyclecount > 20) {
                    for (var sample = 0; sample < 112; sample++) {  // for 112 values
                        var samples = [];
                        //assuming all arrays have the same amount of numbers
                        for (var cycle = cyclecount - 1; cycle > cyclecount - 11; cycle--) {   //get the latest 10 values
                            samples.push(volts5[cmd][cycle][sample]);
                        }
                        //console.log("samples length should be 10: " + samples.length)
                        baselineVolts.push(mathFunctions.getMedian(samples)); //median over latest 10 values
                        //limit baseline to 112 values
                        if (baselineVolts.length > 112) {
                            baselineVolts.shift();
                            baselineReady = true;
                        }
                    }
                }
            }
        });

        //if subBase===true and baselineReady===true subtract baseline from values
        if (subBase && baselineReady) {
            //subtract baselineVolts from current slot
            commands.forEach(cmd => {
                 for (var sample = 0; sample < 112; sample++) {  // for 112 values
                      volts5[cmd][sample] = volts5[cmd][sample] - baselineVolts[sample];
                       console.log(volts5[cmd][sample]);
                 }

            });

            /*
            //if baselineReady send 5 cycles to python for filter and detect
            if (baselineReady) {
                var voltsFiltered = [];
                const options = {mode: 'text'};
                let pyshell = new PythonShell('/src/pyscripts/butterworthBandpass14.py', options);
                let data = JSON.stringify(volts);

                // sends channel data to the Python script via stdin
                pyshell.send(data).end(function (err) {
                    if (err) {
                        console.log("pyshell send err: " + err)
                    }
                });

                // received a message sent from the Python script (a simple "print" statement)
                pyshell.stdout.on('data', function (data) {
                    //get filtered data back
                    let rawdata = data.split(' ');
                    for (let i = 0; i < rawdata.length; i++) {
                        if (rawdata[i].length > 3 && !isNaN(rawdata[i])) {
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

            }
            */
            //process python result, send cmd if detected


        }
    }


    function processP300(voltsF, command) {
        if (voltsF.length > 0) {

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
            if (!init && (counter % nrOfCommands === 0)) {
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
}
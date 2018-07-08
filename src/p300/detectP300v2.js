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
//volts per cmd
var volts5 = {
    playpause: [],
    next: [],
    prev: [],
    volup: [],
    voldown: []
};
//volts per cmd after baseline subtraction
var volts5based = {
    playpause: [],
    next: [],
    prev: [],
    volup: [],
    voldown: []
};
//commands (as keys for collections)
var commands = [
    'playpause',
    'next',
    'prev',
    'volup',
    'voldown'
];
var nrOfCommands = commands.length;    // aka 5

//baseline array as sliding window (contains the latest values from any command)
var baseline = [];

function detectP300(volts, command, time) {

    if (init) {
        if (counter === 0) {
            //get Settings only once
            settings = p300.getSettings();
        }
        //after 10 cycles of 5 cmds each = 50 -> counter > 55(safety)
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
        //generate sliding window baseline values (median for every cmd and over 5 cycles)
        commands.forEach(cmd => {
            let cyclecount = volts5[cmd].length; //how many cycles of this cmd are present in volts5
            if (volts5.hasOwnProperty(cmd) && cyclecount > 5) {
                for (var sample = 0; sample < 112; sample++) {  // for 112 values
                    var samples = [];
                    //assuming all arrays have the same amount of numbers
                    for (var cycle = cyclecount - 5; cycle < cyclecount; cycle++) {   //get the latest 5 values
                        samples.push(volts5[cmd][cycle][sample]);
                        //console.log(volts5[cmd][cycle][sample] + " cmd:" + cmd + " cycle:" + cycle + " sample:" + sample);
                    }
                    //console.log("samples length should be 5: " + samples.length)
                    baseline.push(mathFunctions.getMedian(samples)); //median over latest 10 values
                    //console.log("mathFunctions.getMedian(samples): " + mathFunctions.getMedian(samples));
                }
            }
        });
        //limit baseline to 112 values
        if (baseline.length > 112) {
            baseline = baseline.splice(0, baseline.length - 112);  //cut of start till end-112
        }
        baselineReady = true;

        //if subBase===true and baselineReady===true subtract baseline from values
        if (subBase && baselineReady) {
            //subtract baseline from current slot
            for (let sample = 0; sample < 112; sample++) {  // for 112 values
                volts[sample] = Number(volts[sample]) - Number(baseline[sample]);
                //console.log("volts[sample] " + volts[sample]);
            }

            //add baseline subtracted volts in volts5based
            volts5based[command].push(volts);
            //get for each cmd the latest volts
            var voltsLatest5cmds = [];
            commands.forEach(cmd => {
                voltsLatest5cmds = voltsLatest5cmds.concat(volts5based[cmd][volts5based[cmd].length - 1]);
            });
            //append Commands to Volts
            var sendVoltsCmds = voltsLatest5cmds.concat(commands);

            //send last 5 commands data to python for filter and detect
            let docommand = "nop"; //no operation detected so far
            const options = {mode: 'text'};
            let pyshell = new PythonShell('/src/pyscripts/butterworthBandpassP300Live.py', options);
            let data = JSON.stringify(sendVoltsCmds);

            // sends channel data to the Python script via stdin
            pyshell.send(data).end(function (err) {
                if (err) {
                    console.log("pyshell send err: " + err)
                }
            });

            // received a message sent from the Python script (a simple "print" statement)
            pyshell.stdout.on('data', function (data) {
                docommand = data;
            });

            // end the input stream and allow the process to exit
            pyshell.end(function (err) {
                if (err) throw err;
                 //process python result, send cmd if detected
                if(docommand !== "nop"){
                    console.log("doCmd was not 'nop':"+docommand);
                    //send doCommand to execute
                    server.doCmd(docommand);
                }
            });

        }
    }
}

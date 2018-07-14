module.exports = {
    getVEP: detectP300
};

//baseline, bandpass and detection in python

const p300 = require('./p300');
const server = require('../socket/server');

var PythonShell = require('python-shell');

var settings;
var counter = 0;
var init = true;
var slotsize = 112;
var cycles = 5;

//volts per cmd
var volts5 = {
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


function detectP300(volts, command, time) {


    if (init) {
        if (counter === 0) {
            //get Settings only once
            settings = p300.getSettings();
            console.log("created volts")
        }
        //after 5 cycles of 5 cmds each = 25 -> counter > 30(safety)
        if (counter > 30) {
            init = false;
        }
    }
    counter++;


    //collect volt values sorted by cmd // 5 cycles * 112 slotsize = 560 samples
    if (typeof volts5[command] !== "undefined") {
        volts5[command].push(volts);
        console.log(counter + "cmd: " + command + " volts5[command].length: " + volts5[command].length);
    }


    //if init is over (after 5 cycles aka counter 25) and 5 cycles are in of every command
    if (!init) {
        var each5Ready = each5Ready(commands, volts5);

        if (each5Ready) {
            //limit data to last 5 cycles
            var voltslast5 = Object.create(volts5);     //clone
            commands.forEach(cmd => {
                let len = voltslast5[cmd].length
                voltslast5[cmd].splice(0, len - cycles);   //cut out from start till end-cycles
            });


            //merge volts in one array
            var volts = [];
            commands.forEach(cmd => {
                volts = volts.concat(voltslast5[cmd]);
            });

            //append Commands to Volts
            var sendVoltsCmds = volts.concat(commands);

            //send last 5 cycles and commands to python for filter and detect
            let docommand = "nop"; //no operation detected so far
            const options = {mode: 'text'};
            let pyshell = new PythonShell('/src/pyscripts/butterworthBandpassP300v3.py', options);
            let data = JSON.stringify(sendVoltsCmds);

            // sends channel data to the Python script via stdin
            pyshell.send(data).end(function (err) {
                if (err) {
                    console.log("pyshell send err: " + err)
                }
            });

            // received a message sent from the Python script (a simple "print" statement)
            pyshell.stdout.on('data', function (data) {
                // Remove all new lines
                docommand = data.replace(/\r?\n|\r/g, "");
            });

            // end the input stream and allow the process to exit
            pyshell.end(function (err) {
                if (err) throw err;
                //process python result, send cmd if detected
                if (docommand !== "nop") {
                    console.log("doCmd was not 'nop':" + docommand);
                    //send doCommand to execute
                    server.doCmd(docommand);
                }
            });

        }

    }

    function each5Ready(commands, volts5) {
        commands.forEach(cmd => {
            if (volts5[command].length < cycles * slotsize) {  // 5 cycles * 112 slotsize = 560 samples
                return false;
            }
        });
        return true;
    }
}
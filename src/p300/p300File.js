// show File in python filter


const openData = require('./../functions/openData');
const server = require('../socket/server');
//const p300 = require('./p300');
var PythonShell = require('python-shell');

var commands =  ['playpause','next','prev','volup', 'voldown'];
const options = {mode: 'text'};
let pyshell = new PythonShell('/src/pyscripts/p300detect.py', options);



// received a message sent from the Python script (a simple "print" statement)
pyshell.stdout.on('data', function (value) {
    console.log(value);
    //TODO: send filtered value to detectBlink
    //blink.getBlinks(value);
});

// sends channel data to the Python script via stdin
baseline =   openData.loadJSON('../../data/p300/ex10_cycles5/5-voldown/1533644995773_1_baseline.json');
volts =   openData.loadJSON('../../data/p300/ex10_cycles5/5-voldown/1533644995766_1_volts.json');
cmdIdx =   openData.loadJSON('../../data/p300/ex10_cycles5/5-voldown/1533644995801_1_cmdIdx.json');


let data = JSON.stringify({volts: volts, baseline: baseline, cmdIdx: cmdIdx});

// sends channel data to the Python script via stdin
pyshell.send(data).end(function (err) {
    if (err) {
        console.log("pyshell send err: " + err)
    }
});


// received a message sent from the Python script (a simple "print" statement)
pyshell.stdout.on('data', function (data) {
        // Remove all new lines
        console.log(data);
        idx = data.replace(/\r?\n|\r/g, "");
        //process python result, send cmd if detected
        if (idx !== "nop") {
            cmd = commands[idx];
            console.log("doCmd was: " + cmd);
            //send doCommand to execute
            // server.doCmd(cmd);
        }
});
// end the input stream and allow the process to exit
pyshell.end(function (err) {
    if (err) throw err;
});



// data.forEach(function(sample) {
//     p300.getP300(sample);
// });


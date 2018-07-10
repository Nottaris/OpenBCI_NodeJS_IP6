module.exports = {
    detectMind: detectMind
};


const mathFunctions = require('../functions/mathFunctions');
const mind = require('./mind');
const server = require('../socket/server');

var PythonShell = require('python-shell');
var docommand = "nop";

function detectMind(volts) {

    const options = {mode: 'text'};
    let pyshell = new PythonShell('/src/pyscripts/mind.py', options);
    let data = JSON.stringify(volts);

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
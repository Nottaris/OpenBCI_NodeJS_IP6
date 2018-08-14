/**
 * process eeg volts from mind control to python
 *
 */

module.exports = {
    detectMind: detectMind
};

const server = require("../socket/server");

let PythonShell = require("python-shell");
let docommand = "nop";

function detectMind(volts) {

    const options = {mode: "text"};
    let pyshell = new PythonShell("/src/pyscripts/mindDetect.py", options);
    let data = JSON.stringify(volts);

    // sends channel data to the Python script via stdin
    pyshell.send(data).end(function (err) {
        if (err) {
            console.log("pyshell send err: " + err)
        }
    });

    // received a message sent from the Python script (a simple "print" statement)
    pyshell.stdout.on("data", function (data) {
        // Remove all new lines
        docommand = data.replace(/\r?\n|\r/g, "");
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err) {
           throw err;
        }
        //process python result, send cmd if detected
        if (docommand !== "nop") {
            console.log("doCmd was not nop:" + docommand);
            //send doCommand to execute
            server.doCmd(docommand);
        }
    });
}
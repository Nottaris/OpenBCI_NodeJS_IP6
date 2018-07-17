/**
 * process eeg volts from p300 control to python
 *
 */

module.exports = {
    getVEP: detectP300
};

const p300 = require('./p300');
const server = require('../socket/server');
const fs = require('fs');

let PythonShell = require('python-shell');

let settings;
let init = true;
let fileNr = 1;

function detectP300(volts, timestamps, cmdTimestamps) {

    if (init) {
        //get Settings only once
        settings = p300.getSettings();
        init = false;
    }

    // console.log("cmd 0: " + timestamps.length + " volts length: " + volts.length + " " + cmdTimestamps[0]);

    //get get index for each timestamp
    cmdIdx = [[], [], [], [], []];
    cmdTimestamps.forEach((cmd, i) => {
        cmd.forEach(currentTime => {
            idx = getIdxForTimestamp(timestamps, currentTime);
            if (idx > -1) {
                cmdIdx[i].push(idx);
            } else {
                console.log("No index for timestamp was found " + currentTime);
            }

        });
    });
    // console.log(cmdTimestamps);
    // console.log(cmdIdx);

    fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_volts.json", volts);
    fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_cmdIdx.json", cmdIdx);
    fileNr++;

    const options = {mode: 'text'};
    let pyshell = new PythonShell('/src/pyscripts/butterworthBandpassP300.py', options);
    let data = JSON.stringify({volts: volts, cmdIdx: cmdIdx});

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
        cmd = settings.commands[idx];
        //process python result, send cmd if detected
        if (cmd !== "nop") {
            console.log("doCmd was: " + cmd);
            //send doCommand to execute
            server.doCmd(cmd);
        }

    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err) throw err;
    });

}

// find timestamp idx in timestamp array
function getIdxForTimestamp(timestamps, currentTime) {
    return timestamps.findIndex(timestamp => timestamp === currentTime);
}
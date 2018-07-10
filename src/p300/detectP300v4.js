module.exports = {
    getVEP: detectP300
};

//baseline, bandpass and detection in python

const p300 = require('./p300');
const server = require('../socket/server');

var PythonShell = require('python-shell');

var settings;
var init = true;


function detectP300(volts, timestamps, cmdTimestamps) {

    if (init) {
        //get Settings only once
        settings = p300.getSettings();
        init = false;
    }

    console.log("cmd 0: " + timestamps.length + " volts length: " + volts.length + " " + cmdTimestamps[0]);

    //get get index for each timestamp
    cmdIdx = [[], [], [], [], []];
    cmdTimestamps.forEach((cmd, i) => {
        cmd.forEach(currentTime => {
            idx = getIdxForTimestamp(timestamps, currentTime.toString().slice(0, -1));
            if (idx > -1) {
                cmdIdx[i].push(idx);
            } else {
                console.log("No index for timestamp was found " + currentTime.toString().slice(0, -1));
            }

        });
    });
    console.log(cmdTimestamps);
    console.log(cmdIdx);
    // const options = {mode: 'json'};
    // let pyshell = new PythonShell('/src/pyscripts/butterworthBandpassP300v4.py', options);
    // let data = {volts: volts, cmdIdx: cmdIdx};
    // console.log(data.cmdIdx);
    // sends channel data to the Python script via stdin
    // pyshell.send(data).end(function (err) {
    //     if (err) {
    //         console.log("pyshell send err: " + err)
    //     }
    // });


    // received a message sent from the Python script (a simple "print" statement)
    // pyshell.stdout.on('data', function (data) {
    //     // Remove all new lines
    //     //docommand = data.replace(/\r?\n|\r/g, "");
    // });
    //
    // // end the input stream and allow the process to exit
    // pyshell.end(function (err) {
    //     if (err) throw err;
    //     //process python result, send cmd if detected
    //     if (docommand !== "nop") {
    //         console.log("doCmd was not 'nop':" + docommand);
    //         //send doCommand to execute
    //         // server.doCmd(docommand);
    //     }
    // });

    //reset


}

// find timestamp idx in timestamp array
function getIdxForTimestamp(timestamps, currentTime) {
    return timestamps.findIndex(timestamp => timestamp === currentTime);
}


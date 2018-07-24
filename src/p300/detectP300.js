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
function detectP300(volts, baseline, timestamps, cmdTimestamps) {

    if (init) {
        //get Settings only once
        settings = p300.getSettings();
        init = false;
    }

    // console.log("cmd 0: " + timestamps.length + " volts length: " + volts.length + " " + cmdTimestamps[0]);

    //get get index for each timestamp
    cmdIdx = [[], [], [], [], []];
    cmdTimestamps.forEach((cmd, i) => {
        cmd.forEach((currentTime, j) => {
            idx = getIdxForTimestamp(timestamps, currentTime);
            if (idx > -1) {
                cmdIdx[i].push(idx);
                console.log(i+" "+settings.commands[i]+" "+idx+" "+timestamps[idx]+" "+volts[idx][0])
            } else {
                console.log("No index for timestamp was found " + currentTime);
            }

        });
    });

    console.log(cmdIdx);

    fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_volts.json", JSON.stringify(volts));
    fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_baseline.json", JSON.stringify(baseline));
    fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_cmdIdx.json", JSON.stringify(cmdIdx));
    fileNr++;

    const options = {mode: 'text'};
    let pyshell = new PythonShell('/src/pyscripts/p300detect.py', options);
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
            cmd = settings.commands[idx];
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
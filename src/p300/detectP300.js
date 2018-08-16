/**
 * call python script to detect P300
 *
 */
module.exports = {
    detectP300
};

const p300 = require("./p300");
const server = require("../socket/server");
const fs = require("fs");


let PythonShell = require("python-shell");

let settings;
let init = true;
let fileNr = 1;

/**
 * call python script to detect P300
 * @param {array} volts - eeg data signal
 * @param {array} baseline - eeg data baseline
 * @param {array} timestamps - of data
 * @param {array} cmdTimestamps - of commands
 */
function detectP300(volts, baseline, timestamps, cmdTimestamps) {

    if (init) {
        //get Settings only once
        settings = p300.getSettings();
        init = false;
    }

    //get index for each timestamp
    let cmdIdx = [[], [], [], [], []];
    cmdTimestamps.forEach(function(cmd, i) {
        cmd.forEach(function(currentTime) {
            let idx = getIdxForTimestamp(timestamps, currentTime);
            if (idx > -1) {
                cmdIdx[i].push(idx);
                if(settings.debug) {
                    console.log(i + " " + settings.commands[i] + " " + idx + " " + timestamps[idx] + " " + volts[idx][0]);
                }
            } else {
                console.log("No index for timestamp was found " + currentTime);
            }
        });
    });

    if(settings.debug){
        console.log(cmdIdx);
        fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_volts.json", JSON.stringify(volts));
        fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_baseline.json", JSON.stringify(baseline));
        fs.writeFile("data/p300/"+Date.now()+"_"+fileNr+"_cmdIdx.json", JSON.stringify(cmdIdx));
        fileNr += 1;
    }


    const options = {mode: "text"};
    let pyshell = new PythonShell("/src/pyscripts/p300detect.py", options);

    let data = JSON.stringify({volts: volts, baseline: baseline, cmdIdx: cmdIdx});

    // sends channel data to the Python script via stdin
    pyshell.send(data).end(function (err) {
        if (err) {
            console.log("pyshell send err: " + err);
        }
    });

    // received a message sent from the Python script (a simple "print" statement)
    pyshell.stdout.on("data", function (data) {
        // Remove all new lines
        let idx = data.replace(/\r?\n|\r/g, "");
        //process python result, send cmd if detected
        if (idx !== "nop") {
            let cmd = settings.commands[idx];
            //send command to musicplayer to execute
            server.doP300Cmd(cmd);
        } else {
            console.log("doCmd was: " + idx);
        }
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err) {
            throw err;
        }
    });

}

/**
 * find timestamp idx in timestamp array
 *
 */
function getIdxForTimestamp(timestamps, currentTime) {
    return timestamps.findIndex((timestamp) => timestamp === currentTime);
}
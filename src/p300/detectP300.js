module.exports = {
    getVEP: detectP300
};

const p300 = require('./p300');

let PythonShell = require('python-shell');

let settings;
let init = true;
let docommand = "nop"; //no operation detected so far

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
        docommand = data.replace(/\r?\n|\r/g, "");
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err) throw err;
        //process python result, send cmd if detected
        if (docommand !== "nop") {
            console.log("doCmd was: " + settings.commands[docommand]);
            //send doCommand to execute
            // server.doCmd(docommand);
        }
    });

}

// find timestamp idx in timestamp array
function getIdxForTimestamp(timestamps, currentTime) {
    return timestamps.findIndex(timestamp => timestamp === currentTime);
}
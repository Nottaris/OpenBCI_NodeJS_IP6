/**
 * show File of recorded P300 eeg data in python filter
 *
 */
const openData = require("./../functions/openData");
const server = require("../socket/server");
server.startSocketServer();

let PythonShell = require("python-shell");

let commands =  ["playpause","next","prev","volup", "voldown"];
const options = {mode: "text"};

let pyshell = new PythonShell("/src/pyscripts/p300detect.py", options);

// sends channel data to the Python script via stdin
let baseline =   openData.loadJSON("../../data/p300/ex4_5_cycles5/test/1532350012450_1_baseline.json");
let volts =   openData.loadJSON("../../data/p300/ex4_5_cycles5/test/1532350012442_1_volts.json");
let cmdIdx =   openData.loadJSON("../../data/p300/ex4_5_cycles5/test/1532350012477_1_cmdIdx.json");


let data = JSON.stringify({volts: volts, baseline: baseline, cmdIdx: cmdIdx});



/**
 * sends channel data to the Python script via stdin
 *
 */
pyshell.send(data).end(function (err) {
    if (err) {
        console.log("pyshell send err: " + err);
    }
});


/**
 * received a message sent from the Python script (a simple "print" statement)
 *
 */
pyshell.stdout.on("data", function (data) {
        // Remove all new lines
        console.log(data);
        let idx = data.replace(/\r?\n|\r/g, "");
        //process python result, send cmd if detected
        if (idx !== "nop") {
            let cmd = commands[idx];
            console.log("doCmd was: " + cmd);
            //send doCommand to execute
             server.doP300Cmd(cmd);
        }
});

/**
 * end the input stream and allow the process to exit
 *
 */
pyshell.end(function (err) {
    if (err) {
        throw err;
    }
});


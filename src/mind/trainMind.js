/**
 * training of MindCmd from eeg signal
 *
 */

module.exports = {
    trainMind: trainMind
};

let PythonShell = require('python-shell');

function trainMind() {

    const options = {mode: 'text'};
    let pyshell = new PythonShell('/src/pyscripts/mindTrain.py', options);

    // received a message sent from the Python script (a simple "print" statement)
    pyshell.stdout.on('data', function (data) {
        // Remove all new lines
        let success = data.replace(/\r?\n|\r/g, "");
        //log success or report failure
        if (success === 'true') {
            console.log("training of was successful");
        } else {
            console.log("training of was not successful. received: " + success);
        }
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err) {
        if (err) throw err;
    });
}
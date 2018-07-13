const openData = require('./../functions/openData');
//const blink = require('./../blink/blink');

var PythonShell = require('python-shell');


console.log("blinkfile");

var data = openData.loadJSON("../../test/data/data-2018-5-1-11-23-10-TESTDATA-5-BLINKS.json");
var pyshell = new PythonShell('/src/pyscripts/butterworthBandpassEyeBlink.py');

// received a message sent from the Python script (a simple "print" statement)
pyshell.stdout.on('data', function (value) {
    console.log(value);
    //TODO: send filtered value to detectBlink
    //blink.getBlinks(value);
});

// sends channel data to the Python script via stdin
data.forEach(function (sample) {
    if (sample.channelData[0] !== 0) {
        pyshell.send((sample.channelData[0] * 1000000).toFixed(20));
    }
})

// end the input stream and allow the process to exit
pyshell.end(function (err) {
    if (err) throw err;
    console.log('finished');
});

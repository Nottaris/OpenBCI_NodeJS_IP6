const openData = require('./../functions/openData');
const p300 = require('./p300');
var PythonShell = require('python-shell');


console.log("p300file");

var data = openData.loadJSON("../../test/data/data-2018-6-12-11-40-26_P300_Versuch3_30s_nur_Cz.json");

var pyshell = new PythonShell('/src/pyscripts/butterworthBandpass.py');

// received a message sent from the Python script (a simple "print" statement)
pyshell.stdout.on('data', function (value) {
     console.log(value);
     //TODO: send filtered value to detectBlink
     //blink.getBlinks(value);
});

// sends channel data to the Python script via stdin
data.forEach(function(sample) {
     if(sample.channelData[4]!==0) {
       pyshell.send((sample.channelData[4]* 1000000));
     }
})


// end the input stream and allow the process to exit
pyshell.end(function (err) {
  if (err) throw err;
  console.log('finished');
});

//
// data.forEach(function(sample) {
//     p300.getP300(sample);
// });
//

// show File in python filter


const openData = require('./../functions/openData');
//const p300 = require('./p300');
var PythonShell = require('python-shell');



var data = openData.loadJSON("../../test/data/data-2018-6-12-15-55-05_P300_Versuch5_30s.json");

var pyshell = new PythonShell('/src/pyscripts/butterworthBandpass.py');

// received a message sent from the Python script (a simple "print" statement)
pyshell.stdout.on('data', function (value) {
     console.log(value);
     //TODO: send filtered value to detectBlink
     //blink.getBlinks(value);
});

// sends channel data to the Python script via stdin
let jsonData=[];
data.forEach(function(sample) {
       jsonData.push(sample.channelData);
})

pyshell.send(JSON.stringify(jsonData));


// end the input stream and allow the process to exit
pyshell.end(function (err) {
  if (err) throw err;
  console.log('finished');
});


// data.forEach(function(sample) {
//     p300.getP300(sample);
// });


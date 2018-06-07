const openData = require('./../functions/openData');
var PythonShell = require('python-shell');




console.log("blinkfile");

 var data = openData.loadJSON("../../test/data/data-2018-5-1-11-23-10-TESTDATA-5-BLINKS.json");


var pyshell = new PythonShell('./../pyscripts/butterworthBandpass.py');

pyshell.stdout.on('data', function (data) {
    console.log(data);
});



data.forEach(function(sample) {
     if(sample.channelData[0]!==0) {
        // sends a message to the Python script via stdin
        pyshell.send(sample.channelData[0] * 1000000);
     }
})


// end the input stream and allow the process to exit
pyshell.end(function (err,code,signal) {
  if (err) throw err;
  console.log('The exit code was: ' + code);
  console.log('The exit signal was: ' + signal);
  console.log('finished');
  console.log('finished');
});


var pyshell = new PythonShell('./../pyscripts/butterworthBandpass.py');

pyshell.stdout.on('data', function (data) {
    console.log(data);
});



data[1].channelData[0]



// end the input stream and allow the process to exit
pyshell.end(function (err,code,signal) {
  if (err) throw err;
  console.log('The exit code was: ' + code);
  console.log('The exit signal was: ' + signal);
  console.log('finished');
  console.log('finished');
});
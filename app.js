/**
 * Start OpenBCI Nodejs with different arguments
 *
 */

const blink = require('./src/blink/blink');
const blinkFile = require('./src/blink/blinkFile');
const saveData = require('./src/functions/saveData');
const plot = require('./src/plot/plot');
const openBoard = require('./src/board/openBoard');

let sampleFunction;


// evaluate command line arguments
switch (process.argv[2]) {
    case "blink" :
        sampleFunction = blink.getBlinks;
        break;
    case "blinkfile" :
        blinkFile.start();
        break;
    case "save" :
        sampleFunction = saveData.saveData;
        break;
    case "plot" :
        sampleFunction = plot.start();
        break;
    default:
        console.log("no arguments");
}

// connect to the board ond process samples with sampleFunction
if(sampleFunction != null) {
    openBoard.start(sampleFunction);
}
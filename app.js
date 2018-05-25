/**
 * Start OpenBCI Nodejs with different arguments
 *
 */

const blink = require('./src/blink/blink');
const blinkFile = require('./src/blink/blinkFile');
const p300 = require('./src/p300/p300');
const p300File = require('./src/p300/p300File');
const saveData = require('./src/functions/saveData');
const streamData = require('./src/functions/streamData');
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
    case "p300" :
        sampleFunction = p300.getP300;
        break;
    case "p300file" :
        p300File.start();
        break;
    case "save" :
        sampleFunction = saveData.saveData;
        break;
    case "stream" :
        streamData.start();
        sampleFunction = streamData.streamData;
        break;
    case "plot" :
        sampleFunction = plot.start();
        break;
    default:
        console.log("no arguments");
}

// connect to the board and process samples with sampleFunction
if(sampleFunction != null) {
    openBoard.start(sampleFunction);
}
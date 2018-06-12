/**
 * Start OpenBCI Nodejs - p300 Control
 *
 */

const p300 = require('./p300');
const openBoard = require('./../board/openBoard');

let sampleFunction = p300.getP300;

const boardSettings  = {
    verbose: true,                                              //  Print out useful debugging events
    debug: false,                                               //  Print out a raw dump of bytes sent and received
    simulate: false,                                             // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [true,true,true,true,false,true,true,true],    // power down unused channel 1 - 8
    control: "p300"                                             // Control type
}

// connect to the board and process samples with sampleFunction
openBoard.start(sampleFunction,boardSettings);

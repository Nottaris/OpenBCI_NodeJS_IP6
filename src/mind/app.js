/**
 * Start OpenBCI Nodejs - Mind Control
 *
 */

const mind = require('./mind');
const openBoard = require('./../board/openBoard');

let sampleFunction = mind.getMind;

const boardSettings  = {
    verbose: true,                                              //  Print out useful debugging events
    debug: false,                                               //  Print out a raw dump of bytes sent and received
    simulate: true,                                             // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false,false,false,false,false,false,false,false],    // power down unused channel 1 - 8
    control: "mind"                                             // Control type
}

// connect to the board and process samples with sampleFunction
openBoard.start(sampleFunction,boardSettings);

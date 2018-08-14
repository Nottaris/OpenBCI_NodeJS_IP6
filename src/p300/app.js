/**
 * Start OpenBCI Nodejs - p300 Control
 *
 */

const p300 = require("./p300");
const openBoard = require("./../board/openBoard");

let sampleFunction = p300.getP300;

const boardSettings = {
    verbose: true,                                              //  Print out useful debugging events
    debug: false,                                               //  Print out a raw dump of bytes sent and received
    simulate: true,                                             // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, false, false, false, false, false, false, false],    // power down unused channel 1 - 8
    port: "COM13",                                               // COM Port OpenBCI dongle
    control: "p300"                                             // Control type
}

/**
 * connect to the board and process samples with sampleFunction
 * @param {sampleFunction} function for processing the eeg samples
 * @param {boardSettings} config settings for the board
 */
openBoard.start(sampleFunction, boardSettings);

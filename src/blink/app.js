/**
 * @fileOverview Start OpenBCI Nodejs - Blink Control
 *
 */

const blink = require("./blink");
const openBoard = require("./../board/openBoard");

let sampleFunction = blink.getBlinks;

const boardSettings = {
    verbose: true,                                              //  Print out useful debugging events
    debug: false,                                               //  Print out a raw dump of bytes sent and received
    simulate: true,                                            // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, true, true, true, true, true, true, true],    // power down unused channel 1 - 8
    port: "COM13",                                               // COM Port OpenBCI dongle
    control: "blink"                                            // Control type
};


/**
 * connect to the board and process samples with sampleFunction
 * @param {sampleFunction} function for processing the eeg samples
 * @param {boardSettings} config settings for the board
 */
openBoard.start(sampleFunction, boardSettings);

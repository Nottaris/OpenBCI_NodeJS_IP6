/**
 * @fileOverview Start OpenBCI Nodejs - Mind Control
 *
 */

const mind = require("./mind");
const openBoard = require("./../board/openBoard");

// function for processing eeg samples
let sampleFunction = mind.getMind;

// OpenBCI Board settings
const boardSettings = {
    verbose: true,                     //  Print out useful debugging events
    debug: false,                      //  Print out a raw dump of bytes sent and received
    simulate: true,                    // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, false, false, false, false, false, false, false],    // power down unused channel 1 - 8
    port: "COM13",                     // COM Port OpenBCI dongle
    control: "mind"                    // Control type
};

/**
 * connect to the board and process samples with sampleFunction
 * @param {sampleFunction} function for processing the eeg samples
 * @param {boardSettings} config settings for the board
 */
openBoard.start(sampleFunction, boardSettings);

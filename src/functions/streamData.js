/**
 * stream eeg data from board
 *
 */

module.exports = {
    streamData
};

const openBoard = require("./../board/openBoard");
const server = require("../socket/server");

server.startSocketServer();

// function for processing eeg samples
let sampleFunction = streamData;

// OpenBCI Board settings
const boardSettings = {
    verbose: true,                     //  Print out useful debugging events
    debug: false,                      //  Print out a raw dump of bytes sent and received
    simulate: true,                    // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, false, false, false, false, false, false, false],    // power down unused channel 1 - 8
    port: "COM13",                     // COM Port OpenBCI dongle
    control: "stream"                    // Control type
};

openBoard.start(sampleFunction, boardSettings);

/**
 * stream eeg data to socket server
 * used for plot
 */
function streamData(sample) {
    // send sample to plot
    server.streamData(sample);
    process.stdout.write("Streaming sample...\r");
}

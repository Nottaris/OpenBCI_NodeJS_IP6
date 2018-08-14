module.exports = {
    streamData
};
const openBoard = require("./../board/openBoard");
const server = require("../socket/server");
let init = true;

const boardSettings = {
    verbose: true,                                                  //  Print out useful debugging events
    debug: false,                                                   //  Print out a raw dump of bytes sent and received
    simulate: false,                                                 // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, false, false, false, false, false, false, false], // power down unused channel 1 - 8
    port: "COM13",
    control: "stream"                                               // Control type
}

let sampleFunction = streamData;
openBoard.start(sampleFunction, boardSettings);


function streamData(sample) {
     if (init) {
         server.startSocketServer();
         init = false;
     }
    //emmit sample event for each event
    server.streamData(sample);
    process.stdout.write("Streaming sample...\r");
}

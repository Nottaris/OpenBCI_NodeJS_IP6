
module.exports = {
    streamData
}
const openBoard = require('./../board/openBoard');
const server = require('../socket/server');
let io;
let app;

const boardSettings  = {
    verbose: true,                                                  //  Print out useful debugging events
    debug: false,                                                   //  Print out a raw dump of bytes sent and received
    simulate: true,                                                 // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false,false,false,false,false,false,false,false], // power down unused channel 1 - 8
    control: "stream"                                               // Control type
}

let sampleFunction = streamData;
openBoard.start(sampleFunction,boardSettings);
console.log(server.listening);

function streamData(sample) {
    //emmit sample event for each event
    server.streamData(sample);
    process.stdout.write("Streaming sample...\r");
}

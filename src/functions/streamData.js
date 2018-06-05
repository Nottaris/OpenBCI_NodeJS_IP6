
module.exports = {
    streamData
}
const openBoard = require('./../board/openBoard');
const http = require('http');
let io;
let app;

const boardSettings  = {
    verbose: true,                                                  //  Print out useful debugging events
    debug: false,                                                   //  Print out a raw dump of bytes sent and received
    simulate: true,                                                 // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false,false,false,false,false,false,false,false], // power down unused channel 1 - 8
    control: "stream"                                               // Control type
}

start();

let sampleFunction = streamData;
openBoard.start(sampleFunction,boardSettings);


function start(){
    // create socket server on port 3000
    app = http.createServer(function(req, res) {});
    io = require('socket.io').listen(app);
    app.listen(3000, function(){
        console.log('listening on *:3000');
    });
}

function streamData(sample) {
    //emmit sample event for each event
    io.emit('sample', { sample: sample });
    process.stdout.write("Streaming sample...\r");
}

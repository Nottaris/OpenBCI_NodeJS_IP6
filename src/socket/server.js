//******** send display commands to player via socket.io ************
module.exports = {
    sendCmd,
    doCmd,
    doBlinkCmd,
    streamData
}

const http = require('http');
const port = 3001;
let io;
let app;

// create socket server on port 3001
app = http.createServer(function(req, res) {});
io = require('socket.io').listen(app);
app.listen(port, function(){
    console.log('listening on *:'+port);
});


function sendCmd(command) {
    //emmit command event for each
    io.emit('command', { command: command });
    process.stdout.write("sending commands...\r");
}

function doCmd(docommand) {
    //emmit command event to execute after its detection
    io.emit('docommand', { docommand: docommand });
    console.log("sent docommand: "+docommand);
}

function doBlinkCmd() {
    //emmit command event to execute after its detection
    io.emit('blinkcommand', {blinkcommand: 'blink'});
    console.log("sent blinkcommand");
}

function streamData(sample) {
    //stream bci data to client
    io.emit('sample', { sample: sample });
}

//******** send display commands to player via socket.io ************

module.exports = {
    sendCmd,
    doCmd,
    doBlinkCmd,
    streamData,
    startSocketServer,
    closeSocketServer,
    subscribeToCmds,
    subscribeToTrainingCmds
}

const http = require('http');
const port = 3001;
let io;
let app;

// create socket server on port 3001
function startSocketServer() {
    app = http.createServer(function (req, res) {
    });
    io = require('socket.io').listen(app);
    io.set('origins', 'http://localhost:3000');

    app.listen(port, function () {
        console.log('listening on *:' + port);
    });

    app.on('error', function (e) {
        console.log("error " + e);
        callback(true);
    });
    io.on('P300command', function (data) {
        console.log("P300command" + data);
    });

}


function subscribeToCmds(callbackP300commandCmd) {
    io.on('connection', function (socket) {
        socket.on('P300command', P300command => callbackP300commandCmd(P300command));
    });
}


function subscribeToTrainingCmds(callbackTrainingCmd) {
    io.on('connection', function (socket) {
        socket.on('training', trainingCmd => callbackTrainingCmd(trainingCmd));
    });
}

function closeSocketServer() {
    app.close();
}


function sendCmd(command) {
    //emmit command event for each
    io.emit('command', {command: command});
    process.stdout.write("sending commands...\r");
}

function doCmd(docommand) {
    //emmit command event to execute after its detection
    io.emit('docommand', {docommand: docommand});
    console.log("sent docommand: " + docommand);
}

function doBlinkCmd(docommand) {
    //emmit command event to execute after blink detection
    io.emit('blinkcommand',  {docommand: docommand});
    console.log("sent blinkcommand");
}

function streamData(sample) {
    //stream bci data to client
    io.emit('sample', {sample: sample});
}

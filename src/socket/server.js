//******** send display commands to player via socket.io ************

module.exports = {
    sendCmd,
    doCmd,
    doBlinkCmd,
    streamData,
    startSocketServer,
    closeSocketServer,
    subscribeToP300Cmds,
    subscribeToTrainingCmds
};

const http = require("http");
const port = 3001;
let io;
let app;

// create socket server on port 3001
function startSocketServer() {
    app = http.createServer();
    io = require("socket.io").listen(app);
    io.set("origins", "http://localhost:*");

    app.listen(port, function () {
        console.log("listening on *:" + port);
    });

    app.on("error", function (e) {
        console.log("error " + e);
    });
}


function subscribeToP300Cmds(callbackP300commandCmd) {
    io.on("connection", function (socket) {
        socket.on("P300command", (P300command) => callbackP300commandCmd(P300command));
    });
}


function subscribeToTrainingCmds(callbackTrainingCmd) {
    io.on("connection", function (socket) {
        socket.on("training", (trainingCmd) => callbackTrainingCmd(trainingCmd));
    });
}

function closeSocketServer() {
    if(app !== undefined){
        app.close();
    }
}


function sendCmd(command) {
    //emmit command event for each
    io.emit("command", {command: command});
    process.stdout.write("sending commands...\r");
}

function doCmd(docommand) {
    //emmit command event to execute after its detection
    io.emit("docommand", {docommand: docommand});
    console.log("sent docommand: " + docommand);
}

function doBlinkCmd(docommand) {
    //emmit command event to execute after blink detection
    io.emit("blinkcommand",  {docommand: docommand});
    console.log("sent blinkcommand");
}

function streamData(sample) {
    //stream bci data to client
    io.emit("sample", {sample: sample});
}

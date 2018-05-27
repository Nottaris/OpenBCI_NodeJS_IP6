//******** send display commands to player via socket.io ************

module.exports = {
    sendCmd,
    doCmd
}



const http = require('http');
let io;
let app;

(function start(){
    // create socket server on port 3001
    app = http.createServer(function(req, res) {});
    io = require('socket.io').listen(app);
    app.listen(3001, function(){
        console.log('listening on *:3001');
    });
})();

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
//**********************************************************


module.exports = {
    start,
    streamData
}

const http = require('http');
let io;
let app;

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

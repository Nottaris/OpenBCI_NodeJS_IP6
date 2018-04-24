

module.exports = {
    start,
    streamData
}
const fs = require('fs');
const http = require('http');
const file = fs.createWriteStream('./big.file');
const samples  = [];
var io;

function start(){
    console.log("start server");
        // NEVER use a Sync function except at start-up!
       // index = fs.readFileSync(__dirname + '/index.html');

    var app = http.createServer(function(req, res) {
        res.writeHead(200, {'Content-Type': 'text/html'});
       // res.end(index);
    });

    io = require('socket.io').listen(app);



// Send current time every 10 secs
  //  setInterval(sendTime, 10000);


    app.listen(3000, function(){
        console.log('listening on *:3000');
    });
}


//save incoming sample's to json file with current date time in filename
function streamData(sample) {
// Send current time to all connected clients
        io.emit('sample', { sample: {channel1: sample.channelData[0],  channel2: sample._count}});

   //samples.push(sample);
}

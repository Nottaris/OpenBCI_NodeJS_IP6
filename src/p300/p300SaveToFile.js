module.exports = {
    getP300: function (sample) {
        digestSamples(sample);
    },
    getSettings,
    setSettings,
    reset
}

const commands = [
    "prev",
    "play",
    "next",
    "voldown",
    "pause",
    "volup"
];

const server = require('../socket/server');
// const detectP300 = require('./detectP300');
// const mathFunctions = require('../functions/mathFunctions');
var init = true;
var shuffleCommands = [0,3,5,4,2,1,5,0,2,3,1,4];
var currentCommand;
const defaultSettings  = {
    channel:      5,             // number of channel ( from 1 to 8 ) 5 === yellow Cz (middle top head) for p300
    sampleRate: 250,             // 250Hz
    slots:      125,             // data points per slot ( 240ms === 60 )
    threshold:  1.8,             // deviation factor
    debug:      true,            // show console.log
    baselineSlots: 0,            // 200ms
    skip:       0              // skip after detectP300
}

let volts = [];
let samples = [];
let baseline = [];
let count = 0;
let cycle = 0;
let cmd = 0;
let skip = 0;
let settings = defaultSettings;
const fs = require('fs');
let stream;
let shuffleIndex = 0;

//get date in format for file name like "data-2018-4-6-21-13-08.json"
options = {
    year: 'numeric', month: 'numeric', day: 'numeric',
    hour: 'numeric', minute: 'numeric', second: 'numeric',
    hour12: false
};

datetime = new Intl.DateTimeFormat('de-CH', options).format(new Date());
formatDate = datetime.replace(' ', '-').replace(/:/g, '-');

streamCommands = fs.createWriteStream("data/data-" + formatDate + "_commands.json", { flags: 'a' });
streamCommands.write("commands data/data-" + formatDate +".json\n");

stream = fs.createWriteStream("data/data-" + formatDate + ".json", { flags: 'a' });

// Connect to socket server and process commands
server.startSocketServer();
flashCommand = (data) => {
    console.log("getting command  "+data.command+" "+data.time);
};
server.subscribeToCmds(flashCommand);





function digestSamples(sample) {
    //console.log("sample");
    samples.push(Number(sample.channelData[settings.channel - 1]));
    var record = JSON.stringify(sample);
    stream.write(record + ",\n");
    if(skip >= 250) {

        if (count === 0) {
            baseline = getBaseline();
        }
        if (baseline.length >= settings.baselineSlots) {
            if (init) {
                // setNextCommand();
                // server.sendCmd(currentCommand);
                init = false;
            }

            //process.stdout.write("detect P300...\r");
            // fetch 800ms of samples from channel 5
            if (count < settings.slots) {
                volts.push(Number(sample.channelData[settings.channel - 1])); //microVolts
                count++;
            } else if (count === settings.slots) {
               // server.sendCmd("play");
                count++;
                //send past 1000ms and past command to evaluate
                // detectP300.getVEP(volts, currentCommand, baseline);
                volts = [];
                count = 0;
                //send next command to flash on player
               // setNextCommand();
               // server.sendCmd(currentCommand);
            }
        }
    } else {
        skip++;
    }
}

// function setNextCommand() {
//     let idx = commands.indexOf(currentCommand);
//     currentCommand = commands[idx + 1];
// }
function setNextCommand() {


    if(shuffleIndex > 11){
        shuffleIndex = 0;
        cmd = 0;
        cycle++;
    }
    if(shuffleIndex === 6){
        cmd = 0;
        cycle++;
    }
    currentCommand = commands[shuffleCommands[shuffleIndex]];
    shuffleIndex++;
    cmd++;
   // console.log(currentCommand);
    //streamCommands.write("test\n");
    var newDate = new Date();
    streamCommands.write(""+cycle+"\t cmd "+cmd+" ("+currentCommand+") \trow: "+samples.length+" \t"+newDate.timeNow()+"\n");
}


function getSettings(){
    return settings;
}

function setSettings(newSettings) {
    settings =  newSettings ;
}

function reset(){
     settings = defaultSettings;
     count = 0;
     volts = [];
}

// sliding window
function getBaseline() {
    if (samples.length > settings.baselineSlots) {   // skip first 30 data slots
        return samples.slice(-settings.baselineSlots);
    } else {
        return samples;
    }
}

// For the time now
Date.prototype.timeNow = function () {
     return ((this.getHours() < 10)?"0":"") + this.getHours() +":"+ ((this.getMinutes() < 10)?"0":"") + this.getMinutes() +":"+ ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
};


// function doCmd(docommand) {
//     //emmit command event to execute after its detection
//     socket.emit('docommand', { docommand: docommand });
//     console.log("sent docommand: "+docommand);
// }
//
// socket.on ('commandP300', function (data) {
//     console.log("P300"+data);
//  //do stuff here
// });

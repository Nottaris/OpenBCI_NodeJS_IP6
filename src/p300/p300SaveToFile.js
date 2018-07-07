module.exports = {
    getP300: function (sample) {
        digestSamples(sample);
    },
    getSettings,
    setSettings,
    reset
}

const commands =  ["next", "voldown", "playpause", "prev", "volup"];
const focus = 1; //command 0-4

const server = require('../socket/server');
// const detectP300 = require('./detectP300');
// const mathFunctions = require('../functions/mathFunctions');
var init = true;

const defaultSettings  = {
    channel:      5,             // number of channel ( from 1 to 8 ) 5 === yellow Cz (middle top head) for p300
    sampleRate: 250,             // 250Hz
    slots:      125,             // data points per slot ( 240ms === 60 )
    threshold:  1.8,             // deviation factor
    debug:      true,            // show console.log
    baselineSlots: 0,            // 200ms
    skip:       0              // skip after detectP300
}

let samples = [];
let count = 0;
let cycle = 1;
let cmd = 0;
let settings = defaultSettings;
const fs = require('fs');
let stream;
timestamps = [];
flashedCmds = [];
cmdRow = [];
//get date in format for file name like "data-2018-4-6-21-13-08.json"
options = {
    year: 'numeric', month: 'numeric', day: 'numeric',
    hour: 'numeric', minute: 'numeric', second: 'numeric',
    hour12: false
};

datetime = new Intl.DateTimeFormat('de-CH', options).format(new Date());
formatDate = datetime.replace(' ', '-').replace(/:/g, '-');

streamCommands = fs.createWriteStream("data/data-" + formatDate + "_commands.json", { flags: 'a' });
streamCommands.write("# commands data/data-" + formatDate +".json\n");
streamCommands.write("# command order: "+commands.toString() +"\n");
stream = fs.createWriteStream("data/data-" + formatDate + ".json", { flags: 'a' });
streamCommands.write("# 1 cycles focus on"+commands[focus]+"\n");
streamCommands.write("cycle ="+cycle+"\n");
streamCommands.write("focus ="+focus+"\n");
streamCommands.write("focusCmd =\""+commands[focus]+"\"\n");
// Connect to socket server
server.startSocketServer();

// Process samples from board
function digestSamples(sample) {
    //save channel data and timestamp
    samples.push({time: sample.timestamp.toString().slice(0, -1), sample: Number(sample.channelData[settings.channel - 1])});
    // write sample to json file
    var record = JSON.stringify(sample);
    stream.write(record + ",\n");
}

//proccess flashed commads from player and create json with commands history
flashCommand = (flashedCmd) => {
    console.log("command: "+flashedCmd.command);
    if(flashedCmd.command !== undefined) {
        if(cmd > commands.length-1){
            cycle++;
            console.log("cycle: "+cycle);
            streamCommands.write("# "+cycle+" cycles focus on"+commands[focus]+"\n");
            streamCommands.write("cycle ="+cycle+"\n");
            streamCommands.write("focus ="+focus+"\n");
            streamCommands.write("focusCmd =\""+commands[focus]+"\"\n");
            cmdRow = [];
            timestamps = [];
            flashedCmds = [];
            cmd = 0;
        }
        cmd++;

        cmdRow.push(getSampleRow(flashedCmd.time));
        timestamps.push(flashedCmd.time);
        flashedCmds.push(flashedCmd.command);
        if(cmd > commands.length-1){
            streamCommands.write("cmdRow = "+JSON.stringify(cmdRow)+"\n");
            streamCommands.write("# timestamps: "+JSON.stringify(timestamps)+"\n");
            streamCommands.write("# commands: "+JSON.stringify(commands)+"\n");
            streamCommands.write("detectP300(data, cmdRow, cycle, focus, focusCmd)\n");
        }
    } else {
        console.log("undefined command");
    }
};
server.subscribeToCmds(flashCommand);

// find timestamp in samples array
function getSampleRow(timestamp){
  let samplesReverse = samples.reverse();
  return samplesReverse.length-samplesReverse.findIndex(findIndexForTimestamp(timestamp.toString().slice(0, -1)))-1;
}

//find timestamp in sample that is <= 2 compared with given timestamp
function findIndexForTimestamp(timestamp) {
  return function(element) {
       return timestamp === element.time;
    }
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

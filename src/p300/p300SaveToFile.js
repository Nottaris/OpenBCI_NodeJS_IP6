
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
var shuffleCommands = [];
var currentCommand;
const defaultSettings  = {
    channel:      5,             // number of channel ( from 1 to 8 ) 5 === yellow Cz (middle top head) for p300
    sampleRate: 250,             // 250Hz
    slots:      125,             // data points per slot ( 500ms === 100 )
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
let skip = 0;
let settings = defaultSettings;
const fs = require('fs');
let stream;

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
function digestSamples(sample) {
    samples.push(Number(sample.channelData[settings.channel - 1]));
    var record = JSON.stringify(sample);
    stream.write(record + ",\n");
    if(skip >= 250) {
        if (count === 0) {
            baseline = getBaseline();
        }
        if (baseline.length >= settings.baselineSlots) {
            if (init) {
                setNextCommand();
                server.sendCmd(currentCommand);
                init = false;
            }

            //process.stdout.write("detect P300...\r");
            // fetch 800ms of samples from channel 5
            if (count < settings.slots) {
                volts.push(Number(sample.channelData[settings.channel - 1])); //microVolts
                count++;
            } else if (count === settings.slots) {
                count++;
                //send past 1000ms and past command to evaluate
                // detectP300.getVEP(volts, currentCommand, baseline);

                volts = [];
                count = 0;
                //send next command to flash on player
                setNextCommand();
                server.sendCmd(currentCommand);
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
    if(shuffleCommands.length  === 0){
        //clone array
        shuffleCommands = commands.slice(0);
        //suffle array in random order
        shuffleCommands.sort(function() { return 0.5 - Math.random() });
        cycle++;
        console.log("New cycle "+cycle);
        cmd = 0
    }
    //set current command and remove command from suffle array

    currentCommand = shuffleCommands.pop();
    cmd++;
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
}
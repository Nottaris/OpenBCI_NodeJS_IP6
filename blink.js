/**
 * extract blinks from eeg signal
 */
module.exports = {
    getBlinks: function (sample) {
        /** Work with sample */
        //console.log(timeConverter(sample.timestamp));
        getAveragesFrom2(sample.channelData[2].toFixed(8));

        //for (let i = 0; i < ourBoard.numberOfChannels(); i++) {
        //console.log(`Channel ${(i + 1)}: ${sample.channelData[i].toFixed(8)} Volts.`);
        // prints to the console
        //  "Channel 1: 0.00001987 Volts."
        //  "Channel 2: 0.00002255 Volts."
        //  ...
        //  "Channel 8: -0.00001875 Volts."
        //console.log(sample);
        // }
    }
}


var count = 0;
var blinkSampleSize = 25; //sample comes in 250 Hz : 100ms are 25 samples
var average = 0;
var averages = [];

// sum up volts from electrode 2 and build average
function getAveragesFrom2(volt2) {
    if (count < 25) {
        average += volt2;
    } else if (count === 25) {
        average = average / 25;
        averages.push(average);
        count = 0;
        compareAverages();
    }
}

// compare last two averages for blink detection
function compareAverages() {
    var size = averages.length;
    if (size > 7) {
        var varianz = averages[size-2]+averages[size-3]+averages[size-4]+averages[size-5]+averages[size-6]/5;
        if (averages[size] - averages[size - 1] > varianz) {
            console.log("did you blink?");
        }
    }
}

// get human readable time
function timeConverter(UNIX_timestamp) {
    var a = new Date(UNIX_timestamp);
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes() < 10 ? '0' + a.getMinutes() : a.getMinutes();
    var sec = a.getSeconds() < 10 ? '0' + a.getSeconds() : a.getSeconds();
    var millisec = a.getMilliseconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec + ':' + millisec;
    return time + " @ " + UNIX_timestamp;
}





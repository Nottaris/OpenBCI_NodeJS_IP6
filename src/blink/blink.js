/**
 * extract blinks from eeg signal
 * 
 * first approach: direct volt from channel 2
 * 
 * blinks last from 100 to 400ms in real
 * (EEG data: 20-40Hz)
 */

module.exports = {
    getBlinks: function (sample) {
        getSampleAverages(sample);
    }
}

const detectBlink = require('./detectBlink');
const slots = 10;
const channel = 0;

let averages = [];
let baseline  = [];
let count = 0;
let avgInterval = 0;



function getSampleAverages(sample) {

    baseline = getBaseline();

    if (count < slots) {
        avgInterval = avgInterval+Number(sample.channelData[channel].toFixed(20) * 1000000); //microVolts
        count++;
    } else if (count === slots) {
        averages.push(avgInterval/slots);
        count = 0;
        avgInterval = 0;

        if(baseline.length>=50) {
            detectBlink.compareAverages(baseline,averages,slots);
        }
    }

}
function getBaseline() {
    if(averages.length>250){
        return averages.slice(0,250); //first 10s
    } else {
        return averages;
    }
}

//
// average = 0;
// count = 0;
// blinkSampleSize = 25; //sample comes in 250 Hz : 100ms are 25 samples
// averages = [];
//
// // sum up volts from electrode 2 and build average
// function getAveragesFrom2(sample) {
//
//     //multiply volts for easier visual comparison
//     var volt2 = sample.channelData[1].toFixed(20) * 100000;
//
//     if (count < 25) {
//         average = average+Number(volt2);
//         count++;
//     } else if (count === 25) {
//         average = average / 25;
//         averages.push(average);
//         count = 0;
//         average = 0;
//         compareAverages(sample);
//     }
// }
//
// // compare last two averages for blink detection
// function compareAverages(sample) {
//     var size = averages.length;
//     if (size > 7) {
//         // varianz over 3 values
//         // var varianz = (Math.abs(averages[size-3])+Math.abs(averages[size-4])+Math.abs(averages[size-5])) / 3;
//
//         // varianz over all values
//         var varianz = averages.reduce(function(sum, a) { return sum + Math.abs(a) }, 0) / (averages.length||1);
//
//         // blink as difference of current slot to last slot
//         var blink = averages[size-1] - averages[size-2];
//
// //        console.log("blink   "+blink);
// //        console.log("varianz "+varianz);
//         process.stdout.write("listening to EEG " + timeConverter(sample.timestamp) + "\r");
//         if (blink > varianz) {
//             console.log("You blinked at "+timeConverter(sample.timestamp));
//         }
//     }
// }
//
// // get human readable time
// function timeConverter(UNIX_timestamp) {
//     var a = new Date(UNIX_timestamp);
//     var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
//     var year = a.getFullYear();
//     var month = months[a.getMonth()];
//     var date = a.getDate();
//     var hour = a.getHours();
//     var min = a.getMinutes() < 10 ? '0' + a.getMinutes() : a.getMinutes();
//     var sec = a.getSeconds() < 10 ? '0' + a.getSeconds() : a.getSeconds();
//     var millisec = a.getMilliseconds() < 10 ? '00' + a.getMilliseconds() : a.getMilliseconds() < 100 ? '0' + a.getMilliseconds() : a.getMilliseconds();;
//     var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec + ':' + millisec;
//     return time; // + " @ " + UNIX_timestamp;
// }
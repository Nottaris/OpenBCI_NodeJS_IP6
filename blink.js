/**
 * extract blinks from eeg signal
 */
module.exports = {
    getBlinks: function (sample) {
        /** Work with sample */
        //console.log(timeConverter(sample.timestamp));
         getAveragesFrom2(sample);

        //for (let i = 0; i < 8; i++) {
          //  console.log("Channel " + (i + 1) + ": " + sample.channelData[i].toFixed(8) + " Volts.");
            // prints to the console
            //  "Channel 1: 0.00001987 Volts."
            //  "Channel 2: 0.00002255 Volts."
            //  ...
            //  "Channel 8: -0.00001875 Volts."
          //}
    }
}


average = 0;
count = 0;
blinkSampleSize = 25; //sample comes in 250 Hz : 100ms are 25 samples
averages = [];

// sum up volts from electrode 2 and build average
function getAveragesFrom2(sample) {
  
    var volt2 = sample.channelData[1].toFixed(20);
      
    if (count < 25) {
        average = average+Number(volt2*100000);
       // console.log("avg count up"+average);
        count++;
    } else if (count === 25) {
        average = average / 25;
        averages.push(average);
        count = 0;
        average = 0;
        compareAverages(sample);
    }
}

// compare last two averages for blink detection
function compareAverages(sample) {
    var size = averages.length;
    if (size > 7) {
        var varianz = (Math.abs(averages[size-3])+Math.abs(averages[size-4])+Math.abs(averages[size-5])) / 3;
        var blink = averages[size-1] - averages[size-2];
       // console.log("blink   "+blink);
       // console.log("varianz "+varianz);
        if (blink > varianz*3) {
            console.log(timeConverter(sample.timestamp));
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
    var millisec = a.getMilliseconds() < 10 ? '00' + a.getMilliseconds() : a.getMilliseconds() < 100 ? '0' + a.getMilliseconds() : a.getMilliseconds();;
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec + ':' + millisec;
    return time + " @ " + UNIX_timestamp;
}





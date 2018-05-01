const openData = require('./../functions/openData');
const blink = require('./blink');

module.exports = {
    start
};

function start() {

    /* OpenBCI-RAW-EyeBlink-V1-2018-04-09_20-08-00.txt
    12s Blink ~Row 2960
    17s Blink ~Row 4150
    22s Doppelblink ~Row 5450
    */
    console.log("blinkfile");

    data = openData.loadJSON("../../data/data-2018-5-1-11-23-10.json");
    // data = openData.loadJSON();

    data.forEach(function(sample) {
        blink.getBlinks(sample);
    });

    console.log(blink.getBlinkcount());

    //data = openData.getFiledata('data/EyeBlink-V1.txt');
    //calculate avg of 10 rows from channel (25 slots per second)
    // for(var j = 0; j<data.length-slots; j=j+slots){
    //     avgInterval = 0;
    //     for(var i = 0; i < slots; i++){
    //         if(data[i+j]){
    //             avgInterval = avgInterval+Number(data[i+j][channel]);
    //         } else {
    //             console.error("No data??");
    //         }
    //     }
    //     averages.push(avgInterval/slots);
    // }
    //
    // //Save first 250 slots(10 seconds) as baseline
    // if(averages.length>250){
    //     baseline = averages.slice(0,250); //first 10s
    // } else {
    //     baseline = averages;
    // }
    //
    // averages.forEach(function(average) {
    //     detectBlink.compareAverages(baseline,average,slots);
    // });

}

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

}

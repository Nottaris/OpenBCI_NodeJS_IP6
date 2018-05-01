const mathFunctions = require('../functions/mathFunctions');
const eegFunctions = require('./../functions/eegFunctions');
const blink = require('./blink');
module.exports = {
    compareAverages: detectBlink
};
let settings;
var init = true;
let skip = 0;

function detectBlink(baseline, average) {

    var mean = mathFunctions.getAverage(baseline);
    var standardDeviation = mathFunctions.getStandardDeviation(baseline);

    if (init) {
        //get Settings
        settings = blink.getSettings();

        //show Baseline
        if(settings.debug) {
            console.log("=================Baseline=================");
            console.log("  Baseline size:\t" + baseline.length);
            console.log("  Average(mean):\t" + mathFunctions.getAverage(baseline).toFixed(2));
            console.log("  Variance:\t\t" + mathFunctions.getVariance(baseline).toFixed(2));
            console.log("  Standard deviation:\t" + mathFunctions.getStandardDeviation(baseline).toFixed(2));
            console.log("  mean-standardDev*a:\t " + Number(mean - standardDeviation * settings.threshold).toFixed(2));
            console.log("  Max Value:\t\t" + mathFunctions.getMaxValue(baseline).toFixed(2));
            console.log("  Min Value:\t\t" + mathFunctions.getMinValue(baseline).toFixed(2));
            console.log("==============================================");
        }

        init = false;
    }

    //if current value is bigger then  mean - standardDeviation * threshold  it is a blink
    if (Number(mean - standardDeviation * settings.threshold) > average && skip == 0 ) {
        if(settings.debug){
            console.log("BLINK: \t value: "+average.toFixed(2)+"\t at "+new Date());
        }
       blink.setBlinkcount();
       skip = settings.slots*5;
    }

    if(skip > 0) {
        skip--;
    }
   
}



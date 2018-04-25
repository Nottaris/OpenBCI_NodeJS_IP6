const mathFunctions = require('../functions/mathFunctions');
const eegFunctions = require('./../functions/eegFunctions');

module.exports = {
    compareAverages: detectBlink
};

const subtractBaseline = true;  //subtract baseline from slots
var showBaseline = true;
let skip = 0;
function detectBlink(baseline, average, slots) {
    //deviation factor
    var a = 1.5;
    var mean = mathFunctions.getAverage(baseline);
    var standardDeviation = mathFunctions.getStandardDeviation(baseline);

    if (subtractBaseline) {
        averages = eegFunctions.subtractBaseline(baseline, average);
    }  

    if (showBaseline) {
        console.log("=================Baseline=================");
        console.log("  Baseline size:\t" + baseline.length);
        console.log("  Average(mean):\t" + mathFunctions.getAverage(baseline).toFixed(2));
        console.log("  Variance:\t\t" + mathFunctions.getVariance(baseline).toFixed(2));
        console.log("  Standard deviation:\t" + mathFunctions.getStandardDeviation(baseline).toFixed(2));
        console.log("  mean-standardDev*a:\t " + Number(mean - standardDeviation * a).toFixed(2));
        console.log("  Max Value:\t\t" + mathFunctions.getMaxValue(baseline).toFixed(2));
        console.log("  Min Value:\t\t" + mathFunctions.getMinValue(baseline).toFixed(2));
        console.log("==============================================");
        showBaseline = false;
    }

    //  process.stdout.write(average.toFixed(2)+"\r");
        //if current value is bigger then  mean - standardDeviation * a  it is a blink
        if (Number(mean - standardDeviation * a) > average && skip == 0) {
               console.log("BLINK: \t value: "+average.toFixed(2)+"\t at "+new Date());
               skip = slots*5;
        }
        if(skip > 0) {
            skip--;
        }
   
}



const mathFunctions = require('../functions/mathFunctions');

module.exports = {
    compareAverages: detectBlink
};


function detectBlink(baseline, averages, slots){
    //deviation factor
    var a=1.5;
    var mean = mathFunctions.getAverage(baseline);
    var standardDeviation = mathFunctions.getStandardDeviation(baseline);

    if(baseline.length==250){
        console.log("==============================================");
        console.log("  Average size:\t\t"+averages.length);
        console.log("  Baseline size:\t"+baseline.length);
        console.log("  Average(mean):\t"+mathFunctions.getAverage(baseline).toFixed(2));
        console.log("  Variance:\t\t"+mathFunctions.getVariance(baseline).toFixed(2));
        console.log("  Standard deviation:\t"+mathFunctions.getStandardDeviation(baseline).toFixed(2));
        console.log("  mean-standardDev*a:\t "+Number(mean-standardDeviation*a).toFixed(2));
        console.log("  Max Value:\t\t"+mathFunctions.getMaxValue(baseline).toFixed(2));
        console.log("  Min Value:\t\t"+mathFunctions.getMinValue(baseline).toFixed(2));
        console.log("==============================================");
    }

    for (var i=0; i<averages.length; i++) {
            //if current value is bigger then  mean - standardDeviation * a  it is a blink
            if(Number(mean-standardDeviation*a) > averages[i]){
                console.log("BLINK: Row: "+i*slots+"-"+(i*slots+slots)+"\t diff: "+mathFunctions.percentageChange(averages[i],mean).toFixed(2)+"%\t value: "+Number(averages[i]).toFixed(2));

                //skip next 25 slots (1 second)
                if(i+25<averages.length){
                    i=i+25;
                } else {
                    i = averages.length;
                }
            }
    }
}



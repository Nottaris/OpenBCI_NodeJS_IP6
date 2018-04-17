const mathFunctions = require('../functions/mathFunctions');

module.exports = {
    compareAverages: detectBlink
};


function detectBlink(baseline, averages, slots){
    console.log("==============================================");
    console.log("  Average size:\t\t"+averages.length);
    console.log("  Baseline size:\t"+baseline.length);
    console.log("  Average(mean):\t"+mathFunctions.getAverage(baseline).toFixed(2));
    console.log("  Variance:\t\t"+mathFunctions.getVariance(baseline).toFixed(2));
    console.log("  Standard deviation:\t"+mathFunctions.getStandardDeviation(baseline).toFixed(2));
    console.log("  Max Value:\t\t"+mathFunctions.getMaxValue(averages).toFixed(2));
    console.log("  Min Value:\t\t"+mathFunctions.getMinValue(averages).toFixed(2));
    console.log("==============================================");

    var mean = mathFunctions.getAverage(baseline);
    var standardDeviation = mathFunctions.getStandardDeviation(baseline);

    //deviation factor
    var a=-50;

    for (var i=0; i<averages.length; i++) {

        //compare only values that are significant smaller then mean
        if((averages[i]+standardDeviation) < mean){

            //if difference between value and mean is bigger then deviation factor a it is a blink
            if(a > mathFunctions.procentageChange(averages[i],mean)){
                console.log("BLINK: Row: "+i*slots+"-"+(i*slots+slots)+"\t diff: "+mathFunctions.procentageChange(averages[i],mean).toFixed(2)+"%\t value: "+Number(averages[i]).toFixed(2));

                //skip next 25 slots (1 second)
                if(i+25<averages.length){
                    i=i+25;
                } else {
                    i = averages.length;
                }
            }

        }
    }
}



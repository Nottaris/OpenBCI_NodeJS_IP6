const mathFunctions = require('../functions/mathFunctions');

module.exports = {
    subtractBaseline
}

// returns average minus baseline averages
function subtractBaseline(baseline, average){
    let absBaseline = Math.abs(mathFunctions.getAverage(baseline));
    let result;
    if(average>0){
        result = average - absBaseline;
    }else{
        result = average + absBaseline;
    }
    return result;
}
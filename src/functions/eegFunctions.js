module.exports = {
    subtractBaseline,
    subtractBaselineAllChannels
};

const mathFunctions = require("../functions/mathFunctions");

// returns average minus baseline averages for one Channel Data
function subtractBaseline(baseline, average) {
    let absBaseline = Math.abs(mathFunctions.getAverage(baseline));
    let result;
    if (average > 0) {
        result = average - absBaseline;
    } else {
        result = average + absBaseline;
    }
    return result;
}

// returns average minus baseline averages for all Channels
function subtractBaselineAllChannels(baseline, average) {
    let absBaseline = [];
    for (let index = 0; index < baseline.length; index++) {
        let element = Math.abs(mathFunctions.getAverage(baseline[index]));
        absBaseline.push(element);
    }
    let result = [];
    for (let index = 0; index < absBaseline.length; index++) {
        if (average[index] > 0) {
            result.push(average[index] - absBaseline[index]);
        } else {
            result.push(average[index] + absBaseline[index]);
        }
    }
    return result;
}
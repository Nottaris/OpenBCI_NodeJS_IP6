/**
 * eeg Functions to subtract baseline data
 *
 */
module.exports = {
    subtractBaseline,
    subtractBaselineAllChannels
};

const mathFunctions = require("../functions/mathFunctions");


/**
 * returns average minus baseline averages for one Channel Data
 *
 */
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

/**
 * returns average minus baseline averages for all Channels
 *
 */
function subtractBaselineAllChannels(baseline, average) {
    let absBaseline = [];

    baseline.forEach(function(baselineSample) {
        let element = Math.abs(mathFunctions.getAverage(baselineSample));
        absBaseline.push(element);
    });

    let result = [];

    absBaseline.forEach(function(absSample, index) {
        if (average[index] > 0) {
            result.push(average[index] - absSample);
        } else {
            result.push(average[index] + absSample);
        }
    });
    return result;
}
/**
 * Math Functions
 *
 */

module.exports = {
    percentageChange,
    getAverage,
    getVariance,
    getStandardDeviation,
    getMaxValue,
    getMinValue,
    getMedian,
    clone
};


/**
 * Percentage Change (newValue - oldValue) / |oldValue| *100
 *
 */
function percentageChange(newValue, oldValue) {
    return (newValue - oldValue) / Math.abs(oldValue) * 100;
}


/**
 * average value from array
 *
 */
function getAverage(array) {
    return array.reduce((total, num) => total + num, 0) / array.length;
}

/**
 * median value from array
 *
 */
function getMedian(array) {
    array.sort(function (a, b) {
        return a - b;
    });

    if (array.length === 0) {
        return 0;
    }
    let half = Math.floor(array.length / 2);
    return array[half];
}

/**
 * deviation of average value from array
 *
 */
function getVariance(array) {
    let mean = getAverage(array);
    return array.reduce(function (pre, cur) {
        pre = pre + Math.pow((cur - mean), 2);
        return pre;
    }, 0) / array.length;
}

/**
 *  standard deviation as square root of variance
 *
 */
function getStandardDeviation(array) {
    return Math.sqrt(getVariance(array));
}

/**
 * Get max value form array
 *
 */
function getMaxValue(array) {
    return array.reduce(function (a, b) {
        return Math.max(a, b);
    });
}

/**
 * Get min value form array
 *
 */
function getMinValue(array) {
    return array.reduce(function (a, b) {
        return Math.min(a, b);
    });
}

/**
 * Get deep copy of array
 *
 */
function clone(array) {
    return JSON.parse(JSON.stringify(array));
}
module.exports = {
    percentageChange,
    getAverage,
    getVariance,
    getStandardDeviation,
    getMaxValue,
    getMinValue
}

// Percentage Change (newValue - oldValue) / |oldValue| *100
function percentageChange(newValue,oldValue){
    return (newValue-oldValue)/Math.abs(oldValue)*100;
}

// average value from array
function getAverage(array){
    return array.reduce((total, num) => total+num, 0)/array.length;
}

//  deviation of average value from array
function getVariance(array) {
    var mean =  getAverage(array);
    return array.reduce(function(pre, cur) {
        pre = pre + Math.pow((cur - mean), 2);
        return pre;
    }, 0)/array.length;
}

function getStandardDeviation(array) {
    return Math.sqrt(getVariance(array));
}

// Get max value form array
function getMaxValue(array) {
    return array.reduce(function (a, b) {
        return Math.max(a, b);
    });
}
// Get min value form array
function getMinValue(array) {
    return array.reduce(function (a, b) {
        return Math.min(a, b);
    });
}


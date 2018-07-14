// test the mathFunctions
const mathFunctions = require('./../src/functions/mathFunctions');
var assert = require('assert');

describe('mathFunctions', function () {
    describe('#percentageChange()', function () {
        it('(3-6)/Math.abs(6)*100 should be -50', function () {
            assert.equal(mathFunctions.percentageChange(3, 6), -50);
            assert.equal(mathFunctions.percentageChange(6, 3), 100);
        });
    });
    describe('#getAverage()', function () {
        it('[10,20] should be 15', function () {
            assert.deepEqual(mathFunctions.getAverage([10, 20]), 15);
            assert.deepEqual(mathFunctions.getAverage([-10, 20]), 5);
            assert.deepEqual(mathFunctions.getAverage([-10, -20]), -15);
            assert.deepEqual(mathFunctions.getAverage([-10, 20, 33, 44.55]), 21.8875);
        });
    });
    describe('#getVariance()', function () {
        it('[10,20] should be 15', function () {
            assert.deepEqual(mathFunctions.getVariance([10, 20]), 25);
            assert.deepEqual(mathFunctions.getVariance([-10, 20]), 225);
            assert.deepEqual(mathFunctions.getVariance([-10, -20]), 25);
            assert.deepEqual(mathFunctions.getVariance([-10, 20, 33, 44.55]), 414.36296874999994);
        });
    });
    describe('#getStandardDeviation()', function () {
        it('[10,20] should be 5', function () {
            assert.deepEqual(mathFunctions.getStandardDeviation([10, 20]), 5);
            assert.deepEqual(mathFunctions.getStandardDeviation([-10, 20]), 15);
            assert.deepEqual(mathFunctions.getStandardDeviation([-10, -20]), 5);
            assert.deepEqual(mathFunctions.getStandardDeviation([-10, 20, 33, 44.55]), 20.355907465647409);
        });
    });
    describe('#getMaxValue()', function () {
        it('[10,20] should be 20', function () {
            assert.deepEqual(mathFunctions.getMaxValue([10, 20]), 20);
            assert.deepEqual(mathFunctions.getMaxValue([-10, 20]), 20);
            assert.deepEqual(mathFunctions.getMaxValue([-10, -20]), -10);
            assert.deepEqual(mathFunctions.getMaxValue([-10, 20, 33, 44.55]), 44.55);
        });
    });
    describe('#getMinValue()', function () {
        it('[10,20] should be 20', function () {
            assert.deepEqual(mathFunctions.getMinValue([10, 20]), 10);
            assert.deepEqual(mathFunctions.getMinValue([-10, 20]), -10);
            assert.deepEqual(mathFunctions.getMinValue([-10, -20]), -20);
            assert.deepEqual(mathFunctions.getMinValue([-10, 20, 33, 44.55]), -10);
        });
    });
    describe('#getMedian()', function () {
        it('[10,20,21,22] should be 20', function () {
            assert.deepEqual(mathFunctions.getMedian([10, 20, 21, 22]), 21);
            assert.deepEqual(mathFunctions.getMedian([-20, 20, 21, 22]), 21);
        });
    });
});
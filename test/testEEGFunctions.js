// test the eegFunctions
const eegFunctions = require('./../src/functions/eegFunctions');
var assert = require('assert');

describe('eegFunctions', function () {
    describe('#subtractBaseline()', function () {
        it('10 minus avg(2,4,6) should be 6', function () {
            assert.equal(eegFunctions.subtractBaseline([2, 4, 6], 10), 6);
        });
    });
    describe('#subtractBaselineAllChannels()', function () {
        it('[10,20] minus avg[(2,4,6),(4,6,8)] should be [6,14]', function () {
            assert.deepEqual(eegFunctions.subtractBaselineAllChannels([[2, 4, 6], [4, 6, 8]], [10, 20]), [6, 14]);
        });
    });
});
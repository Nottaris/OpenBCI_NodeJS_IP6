const eegFunctions = require('./../src/functions/eegFunctions');

// test the eegFunctions
var assert = require('assert');

describe('eegFunctions', function() {
  describe('#subtractBaseline()', function() {
    it('should 6', function() {
      assert.equal(eegFunctions.subtractBaseline([2,4,6], 10), 6);
    });
  });
});

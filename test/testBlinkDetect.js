// test the openData
const blink = require('./../src/blink/blink');
const openData = require('./../src/functions/openData');
const testfile = "../../test/data/data-2018-5-1-11-23-10-TESTDATA-5-BLINKS.json";
var assert = require('assert');

var settings = blink.getSettings();

describe('blink', function () {
  before(function () {
      data = openData.loadJSON(testfile);

  });

    beforeEach(function() {
      blink.reset();
        settings = blink.getSettings();
        settings.debug = false;
        blink.setSettings(settings);
    });

  describe('#detectBlinks', function() {
    it('5 blinks should be detected', function (done) {

      data.forEach(function(sample) {
          blink.getBlinks(sample);
      });

      assert.equal(blink.getBlinkcount(), 5);
      done();
    });
  });
  describe('#detectBlinks with threshold of 0.5', function() {
     it('5 blinks with threshold of 0.5', function (done) {
        settings.threshold = 0.5;
        blink.setSettings(settings);

        data.forEach(function(sample) {
            blink.getBlinks(sample);
        });

        assert.equal(blink.getBlinkcount(), 5);
        settings.threshold = 1.5;
        done();
    });
  });
    describe('#detectBlinks blinks with threshold 3.0', function() {
        it('5 blinks with threshold 3.0', function (done) {
            settings.threshold = 3;
            blink.setSettings(settings);
            data.forEach(function(sample) {
                blink.getBlinks(sample);
            });

            assert.equal(blink.getBlinkcount(), 5);
            settings.threshold = 1.5;
            done();
        });
    });
    afterEach(function() {
        blink.reset();
    });
    after(function () {
        data = null;
    });
});
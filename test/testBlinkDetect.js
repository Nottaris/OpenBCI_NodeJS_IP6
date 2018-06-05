// test the openData
const blink = require('./../src/blink/blink');
const openData = require('./../src/functions/openData');

let assert = require('assert');

let settings = blink.getSettings();

describe('blink - with Paste', function () {
  before(function () {
      const testfile = "../../test/data/data-2018-5-1-11-23-10-TESTDATA-5-BLINKS.json";
      data = openData.loadJSON(testfile);

  });

    beforeEach(function() {
      blink.reset();
        settings = blink.getSettings();
        settings.debug = false;
        blink.setSettings(settings);
    });

  describe('#detectBlinks default threshold', function() {
    it('5 blinks should be detected', function (done) {

      data.forEach(function(sample) {
          blink.getBlinks(sample);
      });

      assert.equal(blink.getBlinkcount(), 5);
      done();
    });
  });
  describe('#detectBlinks with threshold of 1.3', function() {
     it('5 blinks with min. threshold of 1.3', function (done) {
        settings.threshold = 1.3;
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
        it('5 blinks with max. threshold 3.0', function (done) {
            settings.threshold = 4.2;
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

describe('blink - no Paste', function () {
    before(function () {
        const testfile2 = "../../test/data/data-2018-5-1-19-32-11-TESTDATA-5-BLINKS-NoPaste.json";
        data = openData.loadJSON(testfile2);

    });

    beforeEach(function() {
        blink.reset();
        settings = blink.getSettings();
        settings.debug = false;
        blink.setSettings(settings);
    });

    describe('#detectBlinks default threshold', function() {
        it('5 blinks should be detected', function (done) {

            data.forEach(function(sample) {
                blink.getBlinks(sample);
            });

            assert.equal(blink.getBlinkcount(), 5);
            done();
        });
    });
    describe('#detectBlinks with min. threshold of 1.4', function() {
        it('5 blinks with threshold of 1.4', function (done) {
            settings.threshold = 1.4;
            blink.setSettings(settings);

            data.forEach(function(sample) {
                blink.getBlinks(sample);
            });

            assert.equal(blink.getBlinkcount(), 5);
            settings.threshold = 1.5;
            done();
        });
    });
    describe('#detectBlinks blinks with max. threshold 2.0', function() {
        it('5 blinks with threshold 2.0', function (done) {
            settings.threshold = 2.0;
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
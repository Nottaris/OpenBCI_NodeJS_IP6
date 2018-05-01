// test the openData
const openData = require('./../src/functions/openData');
var assert = require('assert');
const fs = require('fs');
const testfilepath = "test/data/OpenDataTest";

describe('openData', function () {
  before(function () {
    var stream = fs.createWriteStream(testfilepath+'.txt', { flags: 'a' });
    stream.write("123");
    stream.close;
  });
  describe('#getFiledata()', function () {
    it('data/testdata.txt should be "123"', function () {
      assert.equal(openData.getFiledata(testfilepath+'.txt'), "123");
    });
  });
  after(function () {
    fs.unlink(testfilepath+'.txt', (err) => {
      if (err) throw err;
    });
  });
  before(function () {
    var stream = fs.createWriteStream(testfilepath+'.json', { flags: 'a' });
    stream.write(JSON.stringify({key:123}));
    stream.close;
  });
  describe('#loadJSON()', function () {
    it('data/testdata.json should be {key:123}', function () {
      assert.equal(openData.getFiledata(testfilepath+'.json'), '{"key":123}');
    });
  });
  after(function () {
    fs.unlink(testfilepath+'.json', (err) => {
      if (err) throw err;
    });
  });
});
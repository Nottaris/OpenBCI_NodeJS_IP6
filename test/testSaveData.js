// test the saveData
const saveData = require('./../src/functions/saveData');
const openData = require('./../src/functions/openData');
var assert = require('assert');
const fs = require('fs');
const data = {key:123};

describe('saveData', function () {
  before(function(){
    saveData.start();
  });
  describe('#saveData()', function () {
    it('should save without error', function (done) {
      saveData.start();
      saveData.saveData(data);
      done();
    });
  });
  describe('#loadJSON()', function () {
    it('should be [content]', function () {
      let newestFile = saveData.getNewestFile();
      saveData.fixJsonFile('./data/'+newestFile);
      assert.equal(openData.getFiledata('./data/'+newestFile), '[{"key":123}]');
    });
  });
  after(function () {
    let newestFile = saveData.getNewestFile();
    fs.unlink('./data/'+newestFile, (err) => {
      if (err) throw err;
    });
  });
});
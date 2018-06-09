// test the openData
const openData = require('./../src/functions/openData');
const assert = require('assert');
const fs = require('fs');
const testfilepath = "test/data/";

describe('openData', function () {


    before(function () {
        var streamTxt = fs.createWriteStream(testfilepath + 'OpenDataTestTxT.txt', {flags: 'a'});
        streamTxt.write("123");
        streamTxt.close;

        var streamJson = fs.createWriteStream(testfilepath + 'OpenDataTestJson.json', {flags: 'a'});
        streamJson.write(JSON.stringify({key: 123}));
        streamJson.close;

    });


    describe('#getFiledata()', function () {
        it('data/testdata.txt should be "123"', function () {
            assert.equal(openData.getFiledata(testfilepath + 'OpenDataTestTxT.txt'), "123");
        });
    });

    describe('#loadJSON()', function () {
        it('data/testdata.json should be {key:123}', function () {
            assert.equal(openData.getFiledata(testfilepath + 'OpenDataTestJson.json'), '{"key":123}');
        });
    });


    after(function () {
        fs.unlink(testfilepath + 'OpenDataTestTxT.txt', (err) => {
            if (err) throw err;
        });

        fs.unlink(testfilepath + 'OpenDataTestJson.json', (err) => {
            if (err) throw err;
        });

    });


});
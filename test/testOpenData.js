// test the openData
const openData = require('./../src/functions/openData');
const openData2 = require('./../src/functions/openData');
const assert = require('assert');
const fs = require('fs');
const testfilepath = "test/data/";

describe('openData', function () {


    before(function () {

        var streamJson = fs.createWriteStream(testfilepath + 'OpenDataTestJson.json', {flags: 'a'});
        streamJson.write(JSON.stringify({key: 123}));
        streamJson.close;

        var streamTxt = fs.createWriteStream(testfilepath + 'OpenDataTestTxT.txt', {flags: 'a'});
        streamTxt.write("123,456,789");
        streamTxt.close;

    });

    this.timeout(15000);


    describe('#getFiledata()', function () {
        it('test/data/OpenDataTestTxT.txt should be "\'123\',\'456\',\'789\'"', function () {
            assert.deepStrictEqual(openData2.getFiledata(testfilepath + 'OpenDataTestTxT.txt'), [['123', '456', '789']]);
        });
    });

    describe('#loadJSON()', function () {
        it('test/data/OpenDataTestJson.json should be {key:123}', function () {
            assert.equal(openData.getFiledata(testfilepath + 'OpenDataTestJson.json'), '{"key":123}');
        });
    });


    after(function () {

        this.timeout(15000);

        fs.unlink(testfilepath + 'OpenDataTestJson.json', (err) => {
            if (err) throw err;
        });

        fs.unlink(testfilepath + 'OpenDataTestTxT.txt', (err) => {
            if (err) throw err;
        });

    });


});
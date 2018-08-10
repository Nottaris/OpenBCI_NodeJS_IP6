// test the openData
const openData = require('./../src/functions/openData');
const openData2 = require('./../src/functions/openData');
const assert = require('assert');
const fs = require('fs');
const testfilepath = "test/data/";

describe('openData', function () {


    before(function () {

        let filepath = testfilepath + 'OpenDataTestJson.json';
        fs.writeFileSync(filepath, JSON.stringify({key: 123}), (err) =>{
            if (err) throw err;
        });

        let filepath2 = testfilepath + 'OpenDataTestTxT.txt';
        fs.writeFileSync(filepath2, "123,456,789", (err) =>{
            if (err) throw err;
        });
    });



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


        fs.unlink(testfilepath + 'OpenDataTestJson.json', (err) => {
            if (err) throw err;
        });

        fs.unlink(testfilepath + 'OpenDataTestTxT.txt', (err) => {
            if (err) throw err;
        });

    });


});
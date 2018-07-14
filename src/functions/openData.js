/**
 * import data from eeg signal csv of json file
 *
 */
// mymodule.js
module.exports = {
    getFiledata,
    loadJSON
}

//csv
const fs = require('fs');
const defaultFilename = "data/data.txt"
//json
const defaultJson = 'data/jsondata.json';

//read csv
function getFiledata(filename) {
    if (filename == null) {
        filename = defaultFilename;
    }
    var str = fs.readFileSync(filename, 'utf8');
    var rows = str.split('\n');
    var cells = rows.map(row => row.split(','));
    return cells;
}

//read json
function loadJSON(filename) {
    if (filename == null) {
        filename = defaultJson;
    }
    return require(filename);
}
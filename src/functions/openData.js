/**
 * import data from eeg signal csv file
 * 
 */
// mymodule.js
module.exports = {
    getFiledata
}

const fs = require('fs');
const defaultFilename = "data/data.txt"


function getFiledata(filename) {
    if(filename==null){
        filename = defaultFilename;
    }
    var str = fs.readFileSync(filename, 'utf8');
    var rows = str.split('\n');
    var cells = rows.map(row => row.split(','));
    return cells;
}
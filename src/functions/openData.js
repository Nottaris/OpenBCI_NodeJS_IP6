/**
 * import data from eeg signal csv file
 * 
 */

const fs = require('fs');
const filename = "data/data.txt"
//var stream = fs.createReadStream(filename);
fs.readFile(filename, 'utf8', function (err, data) {
    if (err) throw err;
    console.log('OK: ' + filename);
    var filedata = data;
    var rows = data.split('\n');
    var cells = rows.map(row => row.split(','));
    return cells;
})



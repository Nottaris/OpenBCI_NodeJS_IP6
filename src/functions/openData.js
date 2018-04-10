/**
 * import data from eeg signal csv file
 * 
 */
// mymodule.js
module.exports = {
    getFiledata
}

const fs = require('fs');
const filename = "data/data.txt"
var cells;


var str = fs.readFile(filename, 'utf8', function (err, data) {
    if (err) throw err;
    console.log('OK: ' + filename);
})


function getFiledata() {

    var str = fs.readFileSync(filename, 'utf8');
    var rows = str.split('\n');
    cells = rows.map(row => row.split(','));
    return cells;
}
/**
 * import data from eeg signal csv file
 * 
 */
// mymodule.js
module.exports = {
    getTest,
    getFiledata
}

const fs = require('fs');
const filename = "data/data.txt"
var cells;
//var stream = fs.createReadStream(filename);

function getFiledata() {
    console.log("getFiledata");
    var result = () => fs.readFile(filename, 'utf8', function (err, data) {
        if (err) throw err;
        console.log('OK: ' + filename);
        var filedata = data;
        var rows = data.split('\n');
        cells = rows.map(row => row.split(','));
        console.log(cells[1]);
    })
    return cells;
}
getFiledata();
function getTest() {
    return "test";
}
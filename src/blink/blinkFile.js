const data = require('./../functions/openData');
module.exports = {
    start
};
//var cells = [];

function start() {
    var cells = data.getFiledata();
    console.log("BlinkFile"+cells[1]);
}
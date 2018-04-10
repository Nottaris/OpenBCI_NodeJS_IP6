const data = require('./../functions/openData');
module.exports = {
    start
};

function start() {
    var cells = data.getFiledata();
    for (i = 0; i < 10; i++) {
        console.log("BlinkFile"+cells[i]);
    }

}
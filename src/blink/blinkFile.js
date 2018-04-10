const openData = require('./../functions/openData');

module.exports = {
    start
};
let data;

function start() {
    data = openData.getFiledata();
    for (i = 0; i < 10; i++) {
        console.log("Channel 1: "+data[i][1]+"  Channel 2: "+data[i][2]);
    }

}
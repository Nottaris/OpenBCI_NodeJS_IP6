//stream File instead of live data to p300

const openData = require('./../functions/openData');
const p300 = require('./p300');

var data = openData.loadJSON("../../test/data/p300_exp_3/data-2018-7-6-14-32-40.json");
let counter = 0;


setInterval(function () {
    if (counter < data.length) {
        p300.getP300(data[counter]);
        counter++;
    } else {
        console.log("file finished");
    }
}, 4);
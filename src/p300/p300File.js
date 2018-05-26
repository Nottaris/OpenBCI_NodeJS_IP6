const openData = require('./../functions/openData');
const p300 = require('./p300');

module.exports = {
    start
};

function start() {

    console.log("p300file");

    var data = openData.loadJSON("../../data/data-2018-4-17-21-30-56.json");

    data.forEach(function(sample) {
        p300.getP300(sample);
    });
}

const openData = require('./../functions/openData');
const p300 = require('./p300');



console.log("p300file");

var data = openData.loadJSON("../../data/data-2018-5-1-11-23-10.json");

data.forEach(function(sample) {
    p300.getP300(sample);
});


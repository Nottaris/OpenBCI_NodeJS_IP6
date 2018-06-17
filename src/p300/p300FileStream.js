//stream File instead of live data to p300

const openData = require('./../functions/openData');
const p300 = require('./p300');

var data = openData.loadJSON("../../test/data/data-2018-6-12-15-55-05_P300_Versuch5_30s.json");
let counter = 0;



setInterval(function(){
    if (counter < data.length){
            p300.getP300(data[counter]);
            counter++;
    }else{
        console.log("file finished");
    }
    }, 4);
const openData = require('./../functions/openData');

module.exports = {
    start
};

const avgSize = 10;
const varianzSize = 3000;
const channel=1;

let data;
let averages = [];


function start() {

    /* OpenBCI-RAW-EyeBlink-V1-2018-04-09_20-08-00.txt
    12s Blink
    17s Blink
    22s Doppelblink
    28s rechts Zwnkern
    32s mund bewegen */


    data = openData.getFiledata();

    //calculate avg of 10 rows from channel
    for(var j = 0; j<data.length-avgSize; j=j+avgSize){
        avgInterval = 0;
        for(var i = 0; i < avgSize; i++){
            if(data[i+j]){
                avgInterval = avgInterval+Number(data[i+j][channel]);
            } else {
                console.error("No data??");
            }
        }
        averages.push(avgInterval/avgSize);
    }
    compareAverages();
}

function getVarianz(averages){
    if(averages.length>varianzSize){
        averages = averages.slice(0, varianzSize);
    }
    return averages.reduce(function(sum, a) { return sum + Math.abs(a) }, 0) / (averages.length||1);
}

function compareAverages(){
    var varianz = getVarianz(averages);

    // calculate difference between varianz and averages
    for (var i=0; i<averages.length; i++) {
        difference = Math.abs(Number(averages[i]) - varianz);
        if(difference > varianz){
            console.log("Row: "+i*avgSize+"-"+(i*avgSize+avgSize)+"\t diff: "+difference.toFixed(2)+"\t value: "+Number(averages[i]).toFixed(2)+"\t varianz: "+varianz.toFixed(2));
        }
     }
}
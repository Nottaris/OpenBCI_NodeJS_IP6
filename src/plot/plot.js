/**
 * plot data
 */

var once = 0;

module.exports = {
    plot: function (sample) {
        /*
        for (let i = 0; i < 8; i++) {
            console.log("Channel " + (i + 1) + ": " + sample.channelData[i].toFixed(8) + " Volts.");
        }
        */

        (function doOnce(){
            if(once===0){
                console.log("plot");
                openBrowser();
            }
            once++;
        })();

        function openBrowser() {
            var sys = require('sys')
            var exec = require('child_process').exec;

            exec("open /Users/mjair/Documents/GitHub/OpenBCI_NodeJS_IP6/src/plot/index.html", function (err, stdout, stderr) {
                console.log(stdout);
            });
        }
    }
}


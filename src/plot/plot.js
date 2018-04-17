/**
 * plot data
 */

var once = 0;

module.exports = {
    plot: function (sample) {
      
        (function doOnce(){
            if(once===0){
                console.log("plot");
                openBrowser();
            }
            once++;
        })();

        function openBrowser() {
            var exec = require('child_process').exec;

            exec("open ./src/plot/index.html", function (err, stdout, stderr) {
                console.log(stderr);
            });
        }
    }
}


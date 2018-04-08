/**
 * plot data
 */
module.exports = {
    plot: function (sample) {
       console.log("plot");
       
        for (let i = 0; i < 8; i++) {
            console.log("Channel " + (i + 1) + ": " + sample.channelData[i].toFixed(8) + " Volts.");
        }
    }
}


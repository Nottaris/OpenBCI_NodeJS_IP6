/**
 * extract blinks from eeg signal
 */
module.exports = {
    getBlinks: function(sample) {
       /** Work with sample */
    console.log(timeConverter(sample.timestamp));
    
    //for (let i = 0; i < ourBoard.numberOfChannels(); i++) {
            //console.log(`Channel ${(i + 1)}: ${sample.channelData[i].toFixed(8)} Volts.`);
            // prints to the console
            //  "Channel 1: 0.00001987 Volts."
            //  "Channel 2: 0.00002255 Volts."
            //  ...
            //  "Channel 8: -0.00001875 Volts."
            //console.log(sample);
    // }
    }
 }

 

function timeConverter(UNIX_timestamp){
    var a = new Date(UNIX_timestamp * 1000);
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes() < 10 ? '0' + a.getMinutes() : a.getMinutes();
    var sec = a.getSeconds() < 10 ? '0' + a.getSeconds() : a.getSeconds();        
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
    return time;
}
  
  
      
        
  
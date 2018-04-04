/**
 * export data from eeg signal
 * 
 * sample ===
 * 
 *       { accelData: [ 0, 0, 0 ],
 *       channelData:
 *       [ -9.834767560335107e-7,
 *           -0.0000468492563783236,
 *           -0.000045038765077443725,
 *           -0.000019222500231564074,
 *           0.000023156407255698115,
 *           0.000003330409923840752,
 *           0.000018753113598002625,
 *           0.000029794875358924313 ],
 *       auxData: <Buffer 00 00 00 00 00 00>,
 *       sampleNumber: 27,
 *       startByte: 160,
 *       stopByte: 192,
 *       valid: true,
 *       timestamp: 1522762092162,
 *       boardTime: 0,
 *       _count: 283 }
 * 
 */

options = {
    year: 'numeric', month: 'numeric', day: 'numeric',
    hour: 'numeric', minute: 'numeric', second: 'numeric',
    hour12: false
};
datetime = new Intl.DateTimeFormat('de-CH', options).format(new Date());
formatDate = datetime.replace(' ', '-').replace(/:/g, '-');

module.exports = {

    saveData: function (sample) {
        var record = JSON.stringify(sample);
        var fs = require('fs');
        var stream = fs.createWriteStream("data/data-" + formatDate + ".json", { flags: 'a' });
        stream.write(record + "\n");
    }
}




/**
 * export (save) data from eeg signal to a json file
 * 
 * sample ===
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
 */

module.exports = {
    saveData,
    fixJsonFile,
    getNewestFile
}

//get date in format for file name like "data-2018-4-6-21-13-08.json" 
options = {
    year: 'numeric', month: 'numeric', day: 'numeric',
    hour: 'numeric', minute: 'numeric', second: 'numeric',
    hour12: false
};
datetime = new Intl.DateTimeFormat('de-CH', options).format(new Date());
formatDate = datetime.replace(' ', '-').replace(/:/g, '-');

//save incoming sample's to json file with current date time in filename
function saveData(sample) {
    var record = JSON.stringify(sample);
    const fs = require('fs');
    var stream = fs.createWriteStream("data/data-" + formatDate + ".json", { flags: 'a' });
    stream.write(record + ",\n")
    process.stdout.write("save data...\r");
}

//add [] brackets around file from saveData()
function fixJsonFile() {
    const fs = require('fs');
    var path = "./data/";
    var files = fs.readdirSync(path);
    var newestfile = getNewestFile();
    var pathToFile = path+newestfile;
    var content = fs.readFileSync(pathToFile, 'utf8');
    var contentCut = content.substring(0, content.length - 2); //remove last ,\n
    var fixed = '['+contentCut+']';
    fs.writeFileSync(pathToFile,fixed,'utf8');
}

//get latest file from ./data/
//Source: https://stackoverflow.com/a/37014317
function getNewestFile() {
    const fs = require('fs');
    var path = "./data/";
    var files = fs.readdirSync(path);
    var out = [];
    files.forEach(function(file) {
        var stats = fs.statSync(path + "/" +file);
        if(stats.isFile()) {
            out.push({"file":file, "mtime": stats.mtime.getTime()});
        }
    });
    out.sort(function(a,b) {
        return b.mtime - a.mtime;
    })
    return (out.length>0) ? out[0].file : "";
}
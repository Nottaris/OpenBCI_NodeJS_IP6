/**
 * export (save) data from eeg signal to a json file
 * additional functions to fix json file after sample stream
 * (if stream gets cut off, the closing "]" is missing)
 *
 */

module.exports = {
    saveData,
    fixJsonFile,
    getNewestFile,
    start
};

const openBoard = require("./../board/openBoard");
const fs = require("fs");

const boardSettings = {
    verbose: true,                                                  //  Print out useful debugging events
    debug: false,                                                   //  Print out a raw dump of bytes sent and received
    simulate: false,                                                // Full functionality, just mock data. Must attach Daisy module by setting
    channelsOff: [false, false, false, false, false, false, false, false],  // power down unused channel 1 - 8
    control: "save"                                                 // Control type
}

let stream;

if (process.argv[2] === "start") {
    start();
}

/**
 * connect to the board and process samples with sampleFunction
 *
 */
function start() {
    console.log(start);
    let sampleFunction = saveData;
    openBoard.start(sampleFunction, boardSettings);

    //get date in format for file name like "data-2018-4-6-21-13-08.json"
    options = {
        year: "numeric", month: "numeric", day: "numeric",
        hour: "numeric", minute: "numeric", second: "numeric",
        hour12: false
    };

    datetime = new Intl.DateTimeFormat("de-CH", options).format(new Date());
    formatDate = datetime.replace(" ", "-").replace(/:/g, "-");

    stream = fs.createWriteStream("data/data-" + formatDate + ".json", {flags: "a"});
}


/**
 * save incoming sample"s to json file with current date time in filename
 *
 */
function saveData(sample) {
    let record = JSON.stringify(sample);
    stream.write(record + ",\n");
    process.stdout.write("save data...\r");
}

/**
 * add [] brackets around file from saveData()
 *
 */
function fixJsonFile() {
    const fs = require("fs");
    let path = "./data/";
    let files = fs.readdirSync(path);
    let newestfile = getNewestFile();
    let pathToFile = path + newestfile;
    let content = fs.readFileSync(pathToFile, "utf8");
    let contentCut = content.substring(0, content.length - 2); //remove last ,\n
    let fixed = "[" + contentCut + "]";
    fs.writeFileSync(pathToFile, fixed, "utf8");
}

/**
 * get latest file from ./data/
 * Source: https://stackoverflow.com/a/37014317
 * @return {string} latest filepath
 */
function getNewestFile() {
    let path = "./data/";
    let files = fs.readdirSync(path);
    let out = [];
    files.forEach(function (file) {
        let stats = fs.statSync(path + "/" + file);
        if (stats.isFile()) {
            out.push({"file": file, "mtime": stats.mtime.getTime()});
        }
    });
    out.sort(function (a, b) {
        return b.mtime - a.mtime;
    })
    return (out.length > 0) ? out[0].file : "";
}

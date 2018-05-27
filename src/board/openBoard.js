/**
 * This is an example from the readme.md
 * On windows you should run with PowerShell not git bash.
 * Install
 *   [nodejs](https://nodejs.org/en/)
 *
 * To run:
 *   change directory to this file `cd examples/debug`
 *   do `npm install`
 *   then `npm start`
 */

const saveData = require('./../functions/saveData'); //to fix JsonFiles in cleanup

const debug = false; // Pretty print any bytes in and out... it's amazing...
const verbose = true; // Adds verbosity to functions

const Cyton = require('openbci-cyton');
let ourBoard = new Cyton({
    simulate: true,
    debug: debug,
    verbose: verbose
});

module.exports = {
    start
};

function start(sampleFunction){
    ourBoard.autoFindOpenBCIBoard().then(portName => {
   // var portName = "COM13";
        if (portName) {
            /**
             * Connect to the board with portName
             * Only works if one board is plugged in
             * i.e. ourBoard.connect(portName).....
             */



            ourBoard.connect(portName) // Port name is a serial port name, see `.listPorts()`
                .then(() => {
                    ourBoard.syncRegisterSettings()
                        .then((cs) => {
                            return ourBoard.streamStart();
                        })
                        .catch((err) => {
                            console.log('err', err);
                            return ourBoard.streamStart();
                        })
                        .catch((err) => {
                            console.log('fatal err', err);
                            process.exit(0);
                        });

                    //log firmware version
                    if(debug){
                        console.log("Firmware:");
                        console.log("== v2: " + ourBoard.usingVersionTwoFirmware());
                        console.log("== v3: " + ourBoard.usingVersionThreeFirmware());
                        console.log(">= v2: " + ourBoard.usingAtLeastVersionTwoFirmware());
                    }


                    //.channelSet(channelNumber,powerDown,gain,inputType,bias,srb2,srb1)
                    ourBoard.channelSet(1,true,24,'normal',true,true,false);
                    ourBoard.channelSet(2,true,24,'normal',true,true,false);
                    ourBoard.channelSet(3,true,24,'normal',true,true,false);
                    ourBoard.channelSet(4,true,24,'normal',true,true,false);
                    ourBoard.channelSet(5,false,24,'normal',true,true,false);
                    ourBoard.channelSet(6,true,24,'normal',true,true,false);
                    ourBoard.channelSet(7,true,24,'normal',true,true,false);
                    ourBoard.channelSet(8,true,24,'normal',true,true,false);

                    ourBoard.on('sample', (sample) => {
                        sampleFunction(sample);
                    });
                });
        } else {
            /** Unable to auto find OpenBCI board */
            console.log('Unable to auto find OpenBCI board');
        }
    });

    function exitHandler(options, err) {
        if (options.cleanup) {
            if (verbose) console.log('clean');
            ourBoard.removeAllListeners();
            /** Do additional clean up here */
            if(process.argv[2]==='save'){
                console.log("fix is called");
                saveData.fixJsonFile();
            }
        }
        if (err) console.log(err.stack);
        if (options.exit) {
            if (verbose) console.log('exit');
            ourBoard.disconnect().catch(console.log);
        }
    }

    if (process.platform === 'win32') {
        const rl = require('readline').createInterface({
            input: process.stdin,
            output: process.stdout
        });

        rl.on('SIGINT', function () {
            process.emit('SIGINT');
        });
    }

    // do something when app is closing
    process.on('exit', exitHandler.bind(null, {
        cleanup: true
    }));

    // catches ctrl+c event
    process.on('SIGINT', exitHandler.bind(null, {
        exit: true
    }));

    // catches uncaught exceptions
    process.on('uncaughtException', exitHandler.bind(null, {
        exit: true
    }));
}
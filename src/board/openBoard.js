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

module.exports = {
    start
};

function start(sampleFunction,boardSettings){
    const debug = boardSettings.debug; // Pretty print any bytes in and out... it's amazing...
    const verbose = boardSettings.verbose; // Adds verbosity to functions

    const Cyton = require('openbci-cyton');
    let ourBoard = new Cyton({
        simulate: boardSettings.simulate,
        debug: debug,
        verbose:  verbose
    });


    ourBoard.autoFindOpenBCIBoard()
        .then(portName => {
                if (portName) {
                    connectToBoard(portName);
                } else {
                    /** Unable to auto find OpenBCI board */
                    console.log('Unable to auto find OpenBCI board');
                }
            })
        .catch((err) => {
            //Workaraound: If autofind board doesn't work(windows 10) try it with COM13
            var portName = "COM13";
            connectToBoard(portName);
        });

        function connectToBoard(portName){
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
                    // deactivate unused channels and activate bias and srb2
                    boardSettings.channelsOff.forEach(function(channelState,index){
                        ourBoard.channelSet(index+1,channelState,24,'normal',true,true,false);
                    });

                    ourBoard.on('sample', (sample) => {
                        sampleFunction(sample);
                    });
                });
        }

    function exitHandler(options, err) {
        if (options.cleanup) {
            if (verbose) console.log('clean');
            ourBoard.removeAllListeners();
            /** Do additional clean up here */
            if(boardSettings.control === 'save'){
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
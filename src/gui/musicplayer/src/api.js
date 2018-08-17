import openSocket from "socket.io-client";

const socket = openSocket("http://localhost:3001");

//******** socket.io to listen to commands from node apps *****

function subscribeToP300Cmds(callbackExecCmd) {
    // Execute doP300command in player
    socket.on("doP300command", (doP300command) => callbackExecCmd(doP300command));

    socket.on("error", console.error.bind(console));
    socket.on("message", console.log.bind(console));
}


function subscribeToBlinkCmds(callbackFlashCmd, callbackExecCmd) {
    // flash command in player
    socket.on("command", (command) => callbackFlashCmd(command));
    // Execute doBlinkcommand in player
    socket.on("doBlinkcommand", (doBlinkcommand) => callbackExecCmd(doBlinkcommand));

    socket.on("error", console.error.bind(console));
    socket.on("message", console.log.bind(console));
}


function subscribeToMindCmds(callbackExecCmd) {
    // Execute doMindcommand in player
    socket.on("doMindcommand", (doMindcommand) => callbackExecCmd(doMindcommand));

    socket.on("error", console.error.bind(console));
    socket.on("message", console.log.bind(console));
}

function sendP300Cmd(command, timestamp) {
    //send flashed command and timestamp to server
    socket.emit("P300command", {command: command, time: timestamp});
}

function sendTrainingCmd(command) {
    //send init training for command x
    socket.emit("training", {command: command});
}

export {subscribeToP300Cmds, subscribeToMindCmds, sendP300Cmd, sendTrainingCmd, subscribeToBlinkCmds};

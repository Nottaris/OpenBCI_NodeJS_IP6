import openSocket from 'socket.io-client';
const  socket = openSocket('http://localhost:3001');

//******** socket.io to listen to commands from p300 *****

function subscribeToCmds(callbackFlashCmd, callbackExecCmd, callbackBlinkCmd) {
  socket.on('command', command => callbackFlashCmd(command));
  socket.on('docommand', docommand => callbackExecCmd(docommand));
  socket.on('blinkcommand', _ => callbackBlinkCmd());

  socket.on('error', console.error.bind(console));
  socket.on('message', console.log.bind(console));
}

function sendP300Cmd(command,timestamp) {
    //send flashed command and timestamp to server
    socket.emit('P300command', { command: command, time: timestamp });
    //console.log("sending P300commands: "+command+" "+timestamp);
}

export { subscribeToCmds, sendP300Cmd };

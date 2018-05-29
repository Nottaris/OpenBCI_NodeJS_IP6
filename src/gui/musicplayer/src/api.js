import openSocket from 'socket.io-client';
const  socket = openSocket('http://localhost:3001');

//******** socket.io to listen to commands from p300 *****

function subscribeToCmds(callbackFlashCmd, callbackExecCmd) {
  socket.on('command', command => callbackFlashCmd(command));
  socket.on('docommand', docommand => callbackExecCmd(docommand));

  socket.on('error', console.error.bind(console));
  socket.on('message', console.log.bind(console));
}

export { subscribeToCmds };

import openSocket from 'socket.io-client';
const  socket = openSocket('http://localhost:3001');

//******** socket.io to listen to commands from p300 *****

function subscribeToCmds(callback) {
  socket.on('command', command => callback(command));

  socket.on('error', console.error.bind(console));
  socket.on('message', console.log.bind(console));
}

export { subscribeToCmds };

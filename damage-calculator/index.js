const express = require('express');
const http = require('http');
const ws = require('ws');

const app = express();

const server = http.createServer(app);

const wss = new ws.Server({ server });

wss.on('connection', (socket) => {
    socket.on('message', (data) => {
        console.log(`Recieved ${data}`);
    });
    socket.on('close', (code) => {
        console.log(`Socket closed! (CODE ${code})`);
    });
    socket.send("Hello from the server!");
});

// Start the server
server.listen(process.env.PORT || 3000, () => {
    console.log(`Server started on port ${server.address().port}`);
})

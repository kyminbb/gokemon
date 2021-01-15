const express = require('express');
const http = require('http');
const ws = require('ws');
const calc = require('./calc');

const app = express();
const server = http.createServer(app);
const wss = new ws.Server({ server });

wss.on('connection', socket => {
    socket.on('message', msg => {
        let res;
        try {
            const data = JSON.parse(msg);
            const damage = calc.calcDamage(data);
            res = JSON.stringify({ status: 'success', data: damage });
        } catch (err) {
            const errMsg = err instanceof SyntaxError
                ? 'Failed to parse the request.'
                : 'Failed to calculate the damage.';
            res = JSON.stringify({ status: 'error', data: null, message: errMsg });
        }
        socket.send(res);
        socket.close();
    });

    socket.on('close', code => console.log(`Socket closed! (CODE ${code})`));
});


// Start the server
server.listen(process.env.PORT || 3000, () => {
    console.log(`Server started on port ${server.address().port}`);
});

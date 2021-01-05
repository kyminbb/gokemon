const express = require('express');
const http = require('http');
const ws = require('ws');

const calc = require('@smogon/calc');
const gen = calc.Generations.get(8);
const mode = { NAME1: 0, NAME2: 1, MOVE: 2 }

const app = express();

const server = http.createServer(app);

const wss = new ws.Server({ server });

wss.on('connection', (socket) => {
    let curMode = mode.NAME1;
    let pokemon1, pokemon2, move;
    socket.send('What is the name of your Pokemon?');
    socket.on('message', (data) => {
        switch (curMode) {
            case mode.NAME1: 
                console.log(`Pokemon 1: ${data}`);
                pokemon1 = new calc.Pokemon(gen, data);
                curMode = mode.NAME2;
                socket.send('What is the name of the enemy Pokemon?');
                break;
            case mode.NAME2: 
                console.log(`Pokemon 2: ${data}`);
                pokemon2 = new calc.Pokemon(gen, data);
                curMode = mode.MOVE;
                socket.send('Which skill do you use?');
                break;
            case mode.MOVE:
                console.log(`Move: ${data}`);
                move = new calc.Move(gen, data);
                const result = calc.calculate(gen, pokemon1, pokemon2, move);
                socket.send(`Possible damages: ${result.damage}`);
                socket.close();
                break;
            default:
                return;
        }
    });

    socket.on('close', (code) => {
        console.log(`Socket closed! (CODE ${code})`);
    });
});

// Start the server
server.listen(process.env.PORT || 3000, () => {
    console.log(`Server started on port ${server.address().port}`);
})

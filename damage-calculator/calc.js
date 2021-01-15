const smogon = require('@smogon/calc');
const gen = smogon.Generations.get(8);

const getPokemon = ({ name, ...params }) => {
    const options = { ...params };
    return new smogon.Pokemon(gen, name, options);
};

const getMoves = data => data.map(moveName => new smogon.Move(gen, moveName));

const getField = data => new smogon.Field();

const average = arr => {
    if (arr == 0 || arr.length == 0) return 0;
    const sum = arr.reduce((x, y) => x + y, 0);
    return sum / arr.length;
}

const getAverageDamages = (attacker, defender, moves) => {
    const res = {};
    moves.forEach(move => {
        res[move.name] = average(smogon.calculate(gen, attacker, defender, move).damage);
    });
    return res;
};

exports.calcDamage = ({ from, to }) => {
    const attacker = getPokemon(from);
    const defender = getPokemon(to);
    const moves = getMoves(from.moves);
    return getAverageDamages(attacker, defender, moves);
};
const smogon = require('@smogon/calc');
const gen = smogon.Generations.get(8);

const getPokemon = ({ name, ...params }) => {
    const options = { ...params };
    return new smogon.Pokemon(gen, name, options);
};

const getMove = data => new smogon.Move(gen, data);

const getField = data => new smogon.Field();

const avg = arr => {
    if (arr == 0 || arr.length == 0) return 0;
    const sum = arr.reduce((x, y) => x + y, 0);
    return sum / arr.length;
}

exports.calcDamage = ({ from, to }) => {
    const attacker = getPokemon(from);
    const defender = getPokemon(to);
    const move = getMove(from.moves[0]);
    const result = smogon.calculate(gen, attacker, defender, move);
    return avg(result.damage);
};
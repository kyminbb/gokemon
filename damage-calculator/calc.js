const smogon = require('@smogon/calc');
const gen = smogon.Generations.get(8);

const getPokemon = ({ name, hp, ...params }) => {
    const options = { curHP: hp, ...params };
    return new smogon.Pokemon(gen, name, options);
};

const getMove = data => new smogon.Move(gen, data);

const getField = data => new smogon.Field();

exports.calcDamage = ({ from, to }) => {
    const attacker = getPokemon(from);
    const defender = getPokemon(to);
    const move = getMove(from.moves[0]);
    return smogon.calculate(gen, attacker, defender, move).damage;
};
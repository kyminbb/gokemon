import asyncio
import json
from poke_env.player.random_player import RandomPlayer
from poke_env.player.utils import cross_evaluate
from tabulate import tabulate
from poke_env.player.player import Player
from poke_env.environment.battle import Battle


def parse_pokemon(poke):
    pkt = dict()
    poke_name = str(poke).split()[0]
    pkt["name"] = poke_name[0].upper() + poke_name[1:]
    pkt["gender"] = poke.gender.name
    pkt["level"] = poke.level
    pkt["stats"] = dict()
    stats = poke.stats
    for s in stats.keys():
        pkt["stats"][s] = stats[s]
    pkt["boosts"] = dict()
    boosts = poke.boosts
    for b in boosts.keys():
        pkt["boosts"][b] = boosts[b]
    pkt["ability"] = poke.ability
    pkt["item"] = str(poke.item)
    if poke.status is None:
        pkt["status"] = "NONE"
    else:
        pkt["status"] = poke.status.name
    pkt["hp"] = poke.current_hp
    pkt["moves"] = list(poke.moves.keys())
    return pkt


class MaxDamagePlayer(Player):
    def choose_move(self, battle: Battle) -> str:
        curr_poke = battle.active_pokemon
        oppo_poke = battle.opponent_active_pokemon
        pkt = dict()
        pkt["from"] = parse_pokemon(curr_poke)
        pkt["to"] = parse_pokemon(oppo_poke)
        print(json.dumps(pkt))
        print("=" * 10)
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves,
                            key=lambda move: move.base_power)
            return self.create_order(best_move)
        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)


async def main():
    random_player = RandomPlayer(battle_format="gen8randombattle")
    max_damage_player = MaxDamagePlayer(battle_format="gen8randombattle")
    await max_damage_player.battle_against(random_player, n_battles=100)
    print(f"Max damage player won {max_damage_player.n_won_battles} out of 100 battles")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.get_event_loop().run_until_complete(main())

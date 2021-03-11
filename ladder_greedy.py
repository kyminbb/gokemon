import asyncio

from gokemon.greedy_player import GreedyPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.server_configuration import ShowdownServerConfiguration


async def start_battle_with(player):
    await player.ladder(1)


if __name__ == '__main__':
    greedy_player = GreedyPlayer(
        player_configuration=PlayerConfiguration("GokemonRox", "gokemon"),
        server_configuration=ShowdownServerConfiguration
    )
    greedy_player.connect_to_calculator()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_battle_with(greedy_player))
    greedy_player.close_calculator()

    print(greedy_player.n_won_battles, greedy_player.n_lost_battles)

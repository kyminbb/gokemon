import json
import asyncio

from poke_env.player.player import Player
from poke_env.player.battle_order import BattleOrder
from websocket import create_connection

DAMAGE_API = "ws://protected-stream-83870.herokuapp.com/"


class GreedyPlayer(Player):
    def __init__(self,
                 player_configuration=None,
                 battle_format="gen8randombattle",
                 max_concurrent_battles=1,
                 server_configuration=None,
                 team=None,
                 ) -> None:
        super().__init__(player_configuration=player_configuration,
                         battle_format=battle_format,
                         max_concurrent_battles=max_concurrent_battles,
                         server_configuration=server_configuration,
                         team=team)
        self.damage_calculator = None

    def connect_to_calculator(self):
        if self.damage_calculator is not None:
            self.close_calculator()
        self.damage_calculator = create_connection(DAMAGE_API)

    def close_calculator(self):
        close_msg = json.dumps({"status": "done"})
        self.damage_calculator.send(close_msg)
        self.damage_calculator.close()
        self.damage_calculator = None

    def _get_current_damage(self, battle):
        pass

    def _parse_api_message(self, from_poke, to_poke, battle):
        msg = dict()
        msg["from"] = dict()
        msg["from"]["name"] = str(from_poke).split(" ")[0]
        msg["from"]["moves"] = [move for move in from_poke.moves]

        msg["to"] = dict()
        msg["to"]["name"] = str(to_poke).split(" ")[0]
        return json.dumps(msg)

    def _get_max_damage_move(self, battle):
        msg = self._parse_api_message(battle.active_pokemon,
                                      battle.opponent_active_pokemon,
                                      battle)
        self.damage_calculator.send(msg)
        resp = self.damage_calculator.recv()
        result = json.loads(resp)["data"]
        print(result)
        idx = max(range(len(result)), key=lambda i: list(result.values())[i])
        print(idx)
        return self.create_order(battle.available_moves[idx])

    def choose_move(self, battle):
        if not battle.available_moves:
            return self.choose_random_move(battle)
        else:
            return self._get_max_damage_move(battle)

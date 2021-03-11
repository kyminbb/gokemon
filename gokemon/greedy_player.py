import json

from poke_env.player.player import Player
from websocket import create_connection

from gokemon._link import DAMAGE_API


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
        msg["from"]["boosts"] = from_poke.boosts
        msg["to"] = dict()
        msg["to"]["name"] = str(to_poke).split(" ")[0]
        return json.dumps(msg)

    def _get_max_damage_move(self, from_poke, to_poke, battle):
        msg = self._parse_api_message(from_poke, to_poke, battle)
        self.damage_calculator.send(msg)
        resp = self.damage_calculator.recv()
        result = json.loads(resp)["data"]
        idx = max(range(len(result)), key=lambda i: list(result.values())[i])
        return list(from_poke.moves.values())[idx], list(result.values())[idx]

    def _get_max_damage_switch(self, battle):
        damages = dict()
        if not battle.available_switches:
            return None, 0
        for switch in battle.available_switches:
            move, dam = self._get_max_damage_move(
                switch,
                battle.opponent_active_pokemon,
                battle
            )
            damages[switch] = (move, dam)
        switch = max(damages.keys(), key=lambda s: damages[s][1])
        return switch, damages[switch][1]

    def choose_move(self, battle):
        poke, damage_s = self._get_max_damage_switch(battle)

        if not battle.available_moves:
            if battle.active_pokemon.fainted:
                return self.create_order(poke)
            else:
                return self.choose_default_move()

        move, damage_m = self._get_max_damage_move(
            battle.active_pokemon,
            battle.opponent_active_pokemon,
            battle
        )
        print(f"{poke} can do {damage_s}")
        print(f"{battle.active_pokemon} can do {damage_m} with {move}")
        if damage_s - damage_m > 50:
            return self.create_order(poke)
        else:
            if move in battle.available_moves:
                return self.create_order(move)
            else:
                return self.choose_default_move()

from tkinter import *
from logic.BoardHouse import BoardHouse
from logic.Player import Player
from constants import NUM_CASAS, PLAYER_AMOUNT
from utils.lowercase_and_underscore import lowercase_and_underscore

class GameManager:
    def __init__(self, players, dice):
        self.players = self._create_players(players)
        self.dice = dice
        self.turns = 0
        self.player_turn = self.players[0]

    def get_next_player_turn(self):
        player_index = self.players.index(self.player_turn)
        players_length = len(self.players)

        for i in range(player_index + 1, players_length):
            if self.players[i].is_playing:
                self.player_turn = self.players[i]
                return
        
        for i in range(0, player_index):
            if self.players[i].is_playing:
                self.player_turn = self.players[i]
                return

        raise ValueError('Player was not found')

    def _create_players(self, players) -> list[Player]:
        colors = ['red','yellow', 'blue']
        players = sorted(players, key=lambda x: int(x[2]))
        instances = []
        for player in players:
            [name, created_at, turn] = player
            player_id = lowercase_and_underscore(name)
            instances.append(Player(player_id, turn, colors[int(turn)-1]))
        return instances

    def find_player(self, player_name: str) -> Player:
        player_id = lowercase_and_underscore(player_name)
        for player in self.players:
            if player.player_id == player_id:
                return player
        raise ValueError('Player was not found')

    def roll_dice(self):
        self.turns += 1
        steps = self.dice.roll()
        self.player_turn.posicao += steps
        self.player_turn.posicao %= NUM_CASAS
        return steps

    def handle_new_casa_events(self, player: Player):
        casa = BoardHouse.from_posicao(player.posicao)

        player.handle_default_turn_income()

        player.dinheiro += casa.transaction

        try:
            child_required_cases = [
                BoardHouse.CHILD_GRADUATION, BoardHouse.SCHOOL_CHANGE, 
                BoardHouse.CHILDREN_WEDDING, BoardHouse.MUSIC_LESSON, 
                BoardHouse.SPORTS_COMPETITION, BoardHouse.BIRTHDAY_PARTY
            ]
            if casa in child_required_cases and player.child_amount == 0:
                raise ValueError("A child is required for this position. So no events will be reflected back to you this turn.")
            casa.handle_event(player)
        except Exception as err:
            return casa.title, err.args[0]
        else:
            return casa.title, casa.description
        
    def to_dict(self):
        return {
            'players': [player.to_dict() for player in self.players],
            'dice': self.dice.number,
            'turns': self.turns,
            'player_turn': self.player_turn.to_dict()
        }
    
    def update_game_state(self, data: dict):
        self.dice.number = data['dice']
        self.turns = data['turns']

        for player_data in data['players']:
            player = self.find_player(player_data['player_id'])
            player.update(player_data)

        self.player_turn = self.find_player(data['player_turn']['player_id'])

    @property
    def is_game_finish(self):
        players_with_nonpositive_money = list(filter(lambda player: player.dinheiro < 0, self.players))

        return (len(players_with_nonpositive_money) >= (PLAYER_AMOUNT-1)) or self.turns > 90

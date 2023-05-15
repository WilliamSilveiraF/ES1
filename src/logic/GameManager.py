from tkinter import *
from logic.BoardHouse import BoardHouse
from logic.Player import Player
from contants import NUM_CASAS

class GameManager:
    def __init__(self, players, dice):
        self.players = players
        self.dice = dice

    def roll_dice(self, player: Player):
        steps = self.dice.roll()
        player.posicao += steps
        return steps

    def update_player_position(self, player):
        player.posicao %= NUM_CASAS  # Atualiza a posição do player no tabuleiro

    def handle_new_casa_events(self, jogador: Player):
        casa = BoardHouse.from_posicao(jogador.posicao)

        jogador.handle_default_turn_income()

        jogador.dinheiro += casa.transaction

        try:
            child_required_cases = [
                BoardHouse.CHILD_GRADUATION, BoardHouse.SCHOOL_CHANGE, 
                BoardHouse.CHILDREN_WEDDING, BoardHouse.MUSIC_LESSON, 
                BoardHouse.SPORTS_COMPETITION, BoardHouse.BIRTHDAY_PARTY
            ]
            if casa in child_required_cases and jogador.child_amount == 0:
                raise ValueError("A child is required for this position. So no events will be reflected back to you this turn.")
            casa.handle_event(jogador)
        except Exception as err:
            return casa.title, err.args[0]
        else:
            return casa.title, casa.description
from tkinter import *
import tkinter as tk
from logic.Player import Player
from contants import ALTURA_TABULEIRO
from gui.CardFactory import CardFactory

class RightFrame:
    def __init__(self, master, width, height, players: list[Player]):
        self.right_frame = tk.Canvas(master, width=width, height=height, bg='white')
        self.right_frame.pack(side="right")
        self.cards = CardFactory(self.right_frame, ALTURA_TABULEIRO, players)

    def update_cards(self, players: list[Player]):
        self.cards.refresh_cards(players)
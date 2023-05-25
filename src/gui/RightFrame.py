from tkinter import *
import tkinter as tk
from logic.Player import Player
from contants import ALTURA_TABULEIRO
from typing import List
from collections import namedtuple

Card = namedtuple("Card", ["field", "value"])

class CardFactory:
    def __init__(self, frame, board_height, players: list[Player]):
        self.frame = frame
        self.card_width = int(0.8 * 300)
        self.card_height = int(board_height / 4)
        self.card_space = int((board_height - 3 * self.card_height) / 4)
        self.x1 = (300 - self.card_width) // 2
        self.card_attributes = ['#ebf8ff', '#70cdf6', '#aadef5', '#043c50']
        self.card_texts = self.create_cards(players)

    def _create_card(self, player: Player, i: int) -> List[Card]:
        y1 = self.card_space * (i + 1) + self.card_height * i
        x2 = self.x1 + self.card_width
        y2 = y1 + self.card_height
        # shadow
        self._create_rounded_rect(self.x1+5, y1+5, x2+5, y2+5, radius=20, fill=self.card_attributes[0])
        # card
        self._create_rounded_rect(self.x1, y1, x2, y2, radius=20, fill=self.card_attributes[1], outline=self.card_attributes[2])
        self.frame.create_text(self.x1 + 10, y1 + 10, text=f'#{player.player_id}', anchor="nw", font=("Arial", 14, "bold"), fill=self.card_attributes[3])
        card_content = player.get_card_content()
        card_texts = []
        y_start = self.card_space * (i + 1) + self.card_height * i + 40
        for line in card_content:
            field_text = self.frame.create_text(self.x1 + 10, y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#22471a')
            value_text = self.frame.create_text(self.x1 + self.card_width - 10, y_start, text=line['value'], anchor="ne", font=("Arial", 12), fill='#22471a')
            card_texts.append(Card(field_text, value_text))
            y_start += 22
        return card_texts

    def create_cards(self, players: List[Player]):
        card_texts = []
        for i, player in enumerate(players):
            card_texts.append(self._create_card(player, i))
        return card_texts

    def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Draw a rounded rectangle"""
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1, 
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]
        return self.frame.create_polygon(points, **kwargs, smooth=True)

class RightFrame:
    def __init__(self, master, width, height, players: list[Player]):
        self.right_frame = tk.Canvas(master, width=width, height=height, bg='white')
        self.right_frame.pack(side="right")
        self.cards = CardFactory(self.right_frame, ALTURA_TABULEIRO, players)

    def _update_card(self, players: list[Player]):
        pass
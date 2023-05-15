from tkinter import *
import tkinter as tk
from logic.Player import Player
from contants import ALTURA_TABULEIRO


class RightFrame:
    def __init__(self, master, width, height):
        self.right_frame = tk.Canvas(master, width=width, height=height, bg='white')
        self.right_frame.pack(side="right")

        self.first_card_texts = []
        self.second_card_texts = []
        self.third_card_texts = []

        self._create_cards()

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
        return self.right_frame.create_polygon(points, **kwargs, smooth=True)

    def _create_cards(self):
        self.first_card_texts = []
        self.second_card_texts = []
        self.third_card_texts = []
        
        card_width = int(0.8 * 300)
        card_height = int(ALTURA_TABULEIRO / 4)
        card_space = int((ALTURA_TABULEIRO - 3 * card_height) / 4)

        x1 = (300 - card_width) // 2
        subtitles = ["#Jogador 1", "#Jogador 2", "#Jogador 3"]

        for i in range(3):
            if i == 0:
                [shadow_color, card_bg, card_outline, card_title] = ['#d1e8aa', '#c8df99', '#8ac543', '#22471a']
            else:
                [shadow_color, card_bg, card_outline, card_title] = ['#ebf8ff', '#70cdf6', '#aadef5', '#043c50']

            y1 = card_space * (i + 1) + card_height * i
            x2 = x1 + card_width
            y2 = y1 + card_height
            # shadow
            self._create_rounded_rect(x1+5, y1+5, x2+5, y2+5, radius=20, fill=shadow_color)
            # card
            self._create_rounded_rect(x1, y1, x2, y2, radius=20, fill=card_bg, outline=card_outline)
            self.right_frame.create_text(x1 + 10, y1 + 10, text=subtitles[i], anchor="nw", font=("Arial", 14, "bold"), fill=card_title)

        default_card_lines = [
            { 'field': 'Bank', 'value': f'U$$ {Player.INIT_BANK}' },
            { 'field': 'Salary', 'value': f'U$$ {Player.INIT_SALARY}' },
            { 'field': 'Childs', 'value': '0' },
            { 'field': 'Retirement', 'value': 'U$$ 0' },
            { 'field': 'Life insurance', 'value': 'No' },
            { 'field': 'Vehicle insurance', 'value': 'No' }
        ]
        y_start = card_space + 40

        for line in default_card_lines:
            field_text = self.right_frame.create_text(x1 + 10, y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#22471a')
            value_text = self.right_frame.create_text(x1 + card_width - 10, y_start, text=line['value'], anchor="ne", font=("Arial", 12, "bold"), fill='#22471a')
            self.first_card_texts.append((field_text, value_text))
            y_start += 22

        y_start = 2 * card_space + card_height + 40

        for line in default_card_lines:
            field_text = self.right_frame.create_text(x1 + 10, y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#043c50')
            value_text = self.right_frame.create_text(x1 + card_width - 10, y_start, text=line['value'], anchor="ne", font=("Arial", 12), fill='#043c50')
            self.second_card_texts.append((field_text, value_text))
            y_start += 22

        y_start = 3 * card_space + 2 * card_height + 40

        for line in default_card_lines:
            self.right_frame.create_text(x1 + 10, y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#043c50')
            self.right_frame.create_text(x1 + card_width - 10, y_start, text=line['value'], anchor="ne", font=("Arial", 12), fill='#043c50')
            y_start += 22

    def _update_card(self, card_number, new_lines):
        if card_number == 1:
            texts = self.first_card_texts
        elif card_number == 2:
            texts = self.second_card_texts
        else:
            texts = self.third_card_texts

        for i, line in enumerate(new_lines):
            self.right_frame.itemconfig(texts[i][0], text=line['field'])
            self.right_frame.itemconfig(texts[i][1], text=line['value'])
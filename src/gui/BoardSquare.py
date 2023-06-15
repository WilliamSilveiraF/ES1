from tkinter import *
from PIL import Image, ImageTk
from constants import LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates

class BoardSquare:
    def __init__(self, canvas, pos, color, subcolor, image=None, special=False):
        self.canvas = canvas
        self.pos = pos
        self.color = color
        self.subcolor = subcolor
        self.image = image
        self.image_obj = None
        self.special = special  # additional attribute to handle special cases

    def draw(self):
        x, y = get_board_house_coordinates(self.pos)
        center_x = x + LARGURA_CASA / 2
        center_y = y + LARGURA_CASA / 2

        fill_color = "#043C50" if self.special else self.color
        self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill=fill_color, outline="black")
        
        if self.image:
            self.image_obj = ImageTk.PhotoImage(Image.open(f"media/{self.image}.png"))
            self.canvas.create_image(center_x, center_y, image=self.image_obj)
        elif not self.special:
            self.canvas.create_text(center_x, center_y, text=str(self.pos+1), fill=self.subcolor, font=("Arial", 12, "bold"))

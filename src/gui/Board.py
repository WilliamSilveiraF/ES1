from tkinter import *
from PIL import Image, ImageTk
from constants import LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates

CORES = ["#e6bd22", "#148bc6", "#c01960", "#54ad39"]
LIGHT_CORES = ["#edde22", "#56c2f0", "#e76da8", "#b3d880"]

#img = Image.open('media/cake.png')
#img_resized = img.resize((40, 40))
#img_resized.save('media/resized_cake.png')

class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw_board_spaces()

    def draw_board_spaces(self):
        for i in list(range(10, 20)) + list(range(20, 30)) + list(range(0, 10)) + list(range(30, 36)):
            x, y = get_board_house_coordinates(i)
            cor = CORES[i % len(CORES)]
            subcor = LIGHT_CORES[i % len(LIGHT_CORES)]

            # Calculate center of casa
            center_x = x + LARGURA_CASA / 2
            center_y = y + LARGURA_CASA / 2
            
            if i == 0:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill="#043C50", outline="black")
                self.arrow_image = ImageTk.PhotoImage(Image.open("media/cake_celebration.png"))
                self.canvas.create_image(center_x, center_y, image=self.arrow_image)
            elif i == 18:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill="#043C50", outline="black")
                self.skull_image = ImageTk.PhotoImage(Image.open("media/skull.png"))
                self.canvas.create_image(center_x, center_y, image=self.skull_image)
            else:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill=cor, outline="black")
                self.canvas.create_text(center_x, center_y, text=str(i+1), fill=subcor, font=("Arial", 12, "bold"))        

    
    def draw_players(self, players):
        raio = LARGURA_CASA // 6

        for i, player in enumerate(players):
            if player.is_playing:
                x, y = get_board_house_coordinates(player.posicao)
    
                x += (LARGURA_CASA / 2) - raio
                if i == 0:
                    y += ((LARGURA_CASA) / 10)
                elif i == 1:
                    y += (LARGURA_CASA / 2) - raio
                elif i == 2:
                   y += ((9 * LARGURA_CASA) / 10) - (2 * raio)
                player.pino = self.draw_player(x, y, player.cor, raio)

    def draw_player(self, x, y, cor, raio):
        centro_x, centro_y = x + raio, y + raio
        pino = self.canvas.create_oval(centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio, fill=cor)
        return pino

    def delete_all_players(self, players):
        for player in players:
            if player.pino:
                self.canvas.delete(player.pino)
                player.pino = None
            
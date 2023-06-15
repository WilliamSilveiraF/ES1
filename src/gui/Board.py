from tkinter import *
from constants import LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates
from gui.BoardSquare import BoardSquare

CORES = ["#e6bd22", "#148bc6", "#c01960", "#54ad39"]
LIGHT_CORES = ["#edde22", "#56c2f0", "#e76da8", "#b3d880"]
IMAGES = ["cake_celebration", "mortarboard", "birth", "lottery", "mounteverest", "promotion", "adoption", "robbery", "backpacking", "internship", 
          "childgraduation", "investment", "coralreefdive", "postgrad", "schoolchange", "lifeinsurance", "marathon", "entrepreneur", "skull", 
          "inheritance", "spacetravel", "retirement", "childrenwedding", "carinsurance", "africansafari", "careerchange", "musiclesson", "incometax", 
          "antarticexpedition", "volunteer", "sportscompetition", "charityhouse", "motorcyclejourney", "remotework", "familytrip", "carcrash"]

class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.squares = []
        self.create_squares()
        self.draw_board_spaces()

    def create_squares(self):
        positions = list(range(10, 20)) + list(range(20, 30)) + list(range(0, 10)) + list(range(30, 36))
        for i in positions:
            color = CORES[i % len(CORES)]
            subcolor = LIGHT_CORES[i % len(LIGHT_CORES)]
            image = IMAGES[i] if 0 <= i < 36 else None
            special = i == 0 or i == 18
            self.squares.append(BoardSquare(self.canvas, i, color, subcolor, image, special))

    def draw_board_spaces(self):
        for square in self.squares:
            square.draw()
    
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
            
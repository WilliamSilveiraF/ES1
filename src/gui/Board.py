from tkinter import *
from PIL import Image, ImageTk
from constants import LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates

CORES = ["#e6bd22", "#148bc6", "#c01960", "#54ad39"]
LIGHT_CORES = ["#edde22", "#56c2f0", "#e76da8", "#b3d880"]

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
                if i == 1:
                    self.mortarboard = ImageTk.PhotoImage(Image.open("media/mortarboard.png"))
                    self.canvas.create_image(center_x, center_y, image=self.mortarboard)
                elif i == 2:
                    self.birth = ImageTk.PhotoImage(Image.open("media/birth.png"))
                    self.canvas.create_image(center_x, center_y, image=self.birth)
                elif i == 3:
                    self.lottery = ImageTk.PhotoImage(Image.open("media/lottery.png"))
                    self.canvas.create_image(center_x, center_y, image=self.lottery)
                elif i == 4:
                    self.mounteverest = ImageTk.PhotoImage(Image.open("media/mounteverest.png"))
                    self.canvas.create_image(center_x, center_y, image=self.mounteverest)
                elif i == 5:
                    self.promotion = ImageTk.PhotoImage(Image.open("media/promotion.png"))
                    self.canvas.create_image(center_x, center_y, image=self.promotion)
                elif i == 6:
                    self.adoption = ImageTk.PhotoImage(Image.open("media/adoption.png"))
                    self.canvas.create_image(center_x, center_y, image=self.adoption)
                elif i == 7:
                    self.robbery = ImageTk.PhotoImage(Image.open("media/robbery.png"))
                    self.canvas.create_image(center_x, center_y, image=self.robbery)
                elif i == 8:
                    self.backpacking = ImageTk.PhotoImage(Image.open("media/backpacking.png"))
                    self.canvas.create_image(center_x, center_y, image=self.backpacking)
                elif i == 9:
                    self.internship = ImageTk.PhotoImage(Image.open("media/internship.png"))
                    self.canvas.create_image(center_x, center_y, image=self.internship)
                elif i == 10:
                    self.childgraduation = ImageTk.PhotoImage(Image.open("media/childgraduation.png"))
                    self.canvas.create_image(center_x, center_y, image=self.childgraduation)
                elif i == 11:
                    self.investment = ImageTk.PhotoImage(Image.open("media/investment.png"))
                    self.canvas.create_image(center_x, center_y, image=self.investment)
                elif i == 12:
                    self.coralreefdive = ImageTk.PhotoImage(Image.open("media/coralreefdive.png"))
                    self.canvas.create_image(center_x, center_y, image=self.coralreefdive)
                elif i == 13:
                    self.postgrad = ImageTk.PhotoImage(Image.open("media/postgrad.png"))
                    self.canvas.create_image(center_x, center_y, image=self.postgrad)
                elif i == 14:
                    self.schoolchange = ImageTk.PhotoImage(Image.open("media/schoolchange.png"))
                    self.canvas.create_image(center_x, center_y, image=self.schoolchange)
                elif i == 15:
                    self.lifeinsurance = ImageTk.PhotoImage(Image.open("media/lifeinsurance.png"))
                    self.canvas.create_image(center_x, center_y, image=self.lifeinsurance)
                elif i == 16:
                    self.marathon = ImageTk.PhotoImage(Image.open("media/marathon.png"))
                    self.canvas.create_image(center_x, center_y, image=self.marathon)
                elif i == 17:
                    self.entrepreneur = ImageTk.PhotoImage(Image.open("media/entrepreneur.png"))
                    self.canvas.create_image(center_x, center_y, image=self.entrepreneur)
                elif i == 18:
                    self.familytrip = ImageTk.PhotoImage(Image.open("media/familytrip.png"))
                    self.canvas.create_image(center_x, center_y, image=self.familytrip)
                elif i == 19:
                    self.inheritance = ImageTk.PhotoImage(Image.open("media/inheritance.png"))
                    self.canvas.create_image(center_x, center_y, image=self.inheritance)
                elif i == 20:
                    self.spacetravel = ImageTk.PhotoImage(Image.open("media/spacetravel.png"))
                    self.canvas.create_image(center_x, center_y, image=self.spacetravel)
                elif i == 21:
                    self.retirement = ImageTk.PhotoImage(Image.open("media/retirement.png"))
                    self.canvas.create_image(center_x, center_y, image=self.retirement)
                elif i == 22:
                    self.childrenwedding = ImageTk.PhotoImage(Image.open("media/childrenwedding.png"))
                    self.canvas.create_image(center_x, center_y, image=self.childrenwedding)
                elif i == 23:
                    self.carinsurance = ImageTk.PhotoImage(Image.open("media/carinsurance.png"))
                    self.canvas.create_image(center_x, center_y, image=self.carinsurance)
                elif i == 24:
                    self.africansafari = ImageTk.PhotoImage(Image.open("media/africansafari.png"))
                    self.canvas.create_image(center_x, center_y, image=self.africansafari)
                elif i == 25:
                    self.careerchange = ImageTk.PhotoImage(Image.open("media/careerchange.png"))
                    self.canvas.create_image(center_x, center_y, image=self.careerchange)
                elif i == 26:
                    self.musiclesson = ImageTk.PhotoImage(Image.open("media/musiclesson.png"))
                    self.canvas.create_image(center_x, center_y, image=self.musiclesson)
                elif i == 27:
                    self.incometax = ImageTk.PhotoImage(Image.open("media/incometax.png"))
                    self.canvas.create_image(center_x, center_y, image=self.incometax)
                elif i == 28:
                    self.antarticexpedition = ImageTk.PhotoImage(Image.open("media/antarticexpedition.png"))
                    self.canvas.create_image(center_x, center_y, image=self.antarticexpedition)
                elif i == 29:
                    self.volunteer = ImageTk.PhotoImage(Image.open("media/volunteer.png"))
                    self.canvas.create_image(center_x, center_y, image=self.volunteer)
                elif i == 30:
                    self.sportscompetition = ImageTk.PhotoImage(Image.open("media/sportscopetition.png"))
                    self.canvas.create_image(center_x, center_y, image=self.sportscompetition)
                elif i == 31:
                    self.charityhouse = ImageTk.PhotoImage(Image.open("media/charityhouse.png"))
                    self.canvas.create_image(center_x, center_y, image=self.charityhouse)
                elif i == 32:
                    self.motorcyclejourney = ImageTk.PhotoImage(Image.open("media/motorcyclejourney.png"))
                    self.canvas.create_image(center_x, center_y, image=self.motorcyclejourney)
                elif i == 33:
                    self.remotework = ImageTk.PhotoImage(Image.open("media/remotework.png"))
                    self.canvas.create_image(center_x, center_y, image=self.remotework)
                elif i == 34:
                    self.brithdayparty = ImageTk.PhotoImage(Image.open("media/brithdayparty.png"))
                    self.canvas.create_image(center_x, center_y, image=self.brithdayparty)
                elif i == 35:
                    self.carcrash = ImageTk.PhotoImage(Image.open("media/carcrash.png"))
                    self.canvas.create_image(center_x, center_y, image=self.carcrash)
                else:
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
            
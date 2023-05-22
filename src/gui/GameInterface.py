from tkinter import *
import tkinter as tk
from components.CustomDialog import CustomDialog
from logic.Player import Player
from gui.Board import Board
from gui.Dice import Dice
from gui.RightFrame import RightFrame
from contants import NUM_CASAS, LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates
from utils.lowercase_and_underscore import lowercase_and_underscore
from logic.GameManager import GameManager

class GameInterface:
    def __init__(self, master, player_name, players):
        self.master = master
        self.master.geometry(f"{LARGURA_TABULEIRO+300}x{ALTURA_TABULEIRO}")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self._create_menu()
        self._create_canvas()

        self.right_frame = RightFrame(self.frame, 300, ALTURA_TABULEIRO)

        self.board = Board(self.canvas)

        self.player_name = player_name
        
        self.dice = Dice(self.canvas, self.frame, command=lambda: self.handle_dice_roll())
        self.game_logic = GameManager(players, self.dice)
        self.on_hold_player = self.game_logic.find_player(self.player_name)

        self._create_player_text()
        self._create_game_title()

        self.board.draw_players(self.game_logic.players)

    def update_on_holder_player(self):
        self.on_hold_player = self.game_logic.find_player(self.player_name)

    def update_player_position(self, player):
        raio = LARGURA_CASA // 6
        player.posicao %= NUM_CASAS  # Atualiza a posição do player no tabuleiro
        x, y = get_board_house_coordinates(player.posicao)
        i = self.game_logic.players.index(player)
        
        x += (LARGURA_CASA / 2) - raio
        if i == 0:
            y += ((LARGURA_CASA) / 10)
        elif i == 1:
            y += (LARGURA_CASA / 2) - raio
        elif i == 2:
           y += ((9 * LARGURA_CASA) / 10) - (2 * raio) 
       
        centro_x, centro_y = x + raio, y + raio
        self.canvas.coords(player.pino, centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio)

    def _create_menu(self):
        self.menubar = Menu(self.master)
        self.menubar.option_add('*tearOff', FALSE)
        self.master['menu'] = self.menubar

        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.menu_file.add_command(label='Restaurar estado inicial', command=self.start_game)

    def _create_canvas(self):
        self.canvas = tk.Canvas(self.frame, width=LARGURA_TABULEIRO, height=ALTURA_TABULEIRO, bg='white')
        self.canvas.pack(side="left")

    def _create_right_frame(self):
        self.right_frame = tk.Canvas(self.frame, width=300, height=ALTURA_TABULEIRO, bg='white')
        self.right_frame.pack(side="right")

    def _create_player_text(self):
        self.player_text = self.canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 10, 
                                                    text=f"#{self.on_hold_player.player_id}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")

    def _create_game_title(self):
        self.canvas.create_text(LARGURA_CASA + 20, ALTURA_TABULEIRO - LARGURA_CASA - 20, text="The Game Of Life",
                        anchor='sw', font=("Futura", 12, "italic"), fill="black")

    def _update_card(self, card_number, new_lines):
        self.right_frame._update_card(card_number, new_lines)

    def handle_dice_roll(self):
        steps = self.game_logic.roll_dice(self.on_hold_player)
        self.dice.draw(steps)
        self.game_logic.update_player_position(self.on_hold_player)
        self.update_player_position_on_board(self.on_hold_player)
        title, message = self.game_logic.handle_new_casa_events(self.on_hold_player)
        self.show_dialog(title, message)

        if self.on_hold_player.is_broke:
            self.on_hold_player.set_out_of_match()

            self.dice.roll_btn.destroy()
            self.dice.erase()
            # TODO SET DISABLED MODE IN CARD, RENDER A TITLE CONTAINING THAT THE PLAYER LOST

        new_card_content = self.on_hold_player.get_card_content()
        self._update_card(1, new_card_content)

    def update_player_position_on_board(self, player):
        raio = LARGURA_CASA // 6
        x, y = get_board_house_coordinates(player.posicao)
        i = self.game_logic.players.index(player)
        
        x += (LARGURA_CASA / 2) - raio
        if i == 0:
            y += ((LARGURA_CASA) / 10)
        elif i == 1:
            y += (LARGURA_CASA / 2) - raio
        elif i == 2:
           y += ((9 * LARGURA_CASA) / 10) - (2 * raio) 
       
        centro_x, centro_y = x + raio, y + raio
        self.canvas.coords(player.pino, centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio)

    def show_dialog(self, title, message):
        CustomDialog(self.master, title=title, message=message)
        
    def start_game(self):
        print('start game')
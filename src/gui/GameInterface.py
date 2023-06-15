from tkinter import *
import tkinter as tk
from tkinter import messagebox
from components.CustomDialog import CustomDialog
from logic.Player import Player
from gui.Board import Board
from gui.Dice import Dice
from gui.RightFrame import RightFrame
from constants import NUM_CASAS, LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates
from utils.lowercase_and_underscore import lowercase_and_underscore
from logic.GameManager import GameManager

class GameInterface:
    def __init__(self, master, player_name, players, dog_server_interface):
        self.dog_server_interface = dog_server_interface
        self.master = master
        self.master.geometry(f"{LARGURA_TABULEIRO+300}x{ALTURA_TABULEIRO}")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self._create_menu()
        self._create_canvas()

        self.board = Board(self.canvas)

        self.player_name = player_name
        
        self.dice = Dice(self.canvas, self.frame, command=lambda: self.handle_dice_roll())
        self.game_logic = GameManager(players, self.dice)

        self._create_player_text()
        self._create_game_title()

        self.board.draw_players(self.game_logic.players)
        self.right_frame = RightFrame(self.frame, 300, ALTURA_TABULEIRO, self.game_logic.players)
        self.toggle_dice_visibility()
        
    def toggle_dice_visibility(self):
        on_hold_player = self.game_logic.find_player(self.player_name)
        
        if on_hold_player == self.game_logic.player_turn:
            self.dice.show_roll_btn()
        else:
            self.dice.hide_roll_btn()

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
                                                    text=f"#{self.player_name}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")

    def _create_game_title(self):
        self.canvas.create_text(LARGURA_CASA + 20, ALTURA_TABULEIRO - LARGURA_CASA - 20, text="The Game Of Life",
                        anchor='sw', font=("Futura", 12, "italic"), fill="black")

    def refresh_ui(self):
        self.right_frame.update_cards(self.game_logic.players)
        self.toggle_dice_visibility()
        self.dice.draw(self.game_logic.dice.number)

        self.update_players_position_on_the_board()
    
    def update_players_position_on_the_board(self):
        self.board.delete_all_players(self.game_logic.players)
        self.board.draw_players(self.game_logic.players)

    def handle_move(self, move):
        self.game_logic.update_game_state(move['game_logic'])
        self.refresh_ui()

        if self.game_logic.is_game_finish:
            self.show_the_winner()

    def handle_dice_roll(self):
        steps = self.game_logic.roll_dice()
        self.dice.draw(steps)
        title, message = self.game_logic.handle_new_casa_events(self.game_logic.player_turn)
        self.show_dialog(title, message)

        if self.game_logic.player_turn.is_broke:
            self.game_logic.player_turn.set_out_of_match()
            self.show_dialog('Game over', 'You lost the match!!')        
        
        
        if not self.game_logic.is_game_finish:
            self.game_logic.get_next_player_turn()

        self.dog_server_interface.send_move({ 'match_status': 'next', 'game_logic': self.game_logic.to_dict()})
        self.refresh_ui()
        
        if self.game_logic.is_game_finish:
            print(vars(self.game_logic))
            self.show_the_winner()


    def show_the_winner(self):
        winner = self.game_logic.get_winner()
        messagebox.showinfo(f'There is a winner in the match', f'The player #{winner.player_id} won the match')
        self.master.destroy()

    def show_dialog(self, title, message, command=None):
        CustomDialog(self.master, title=title, message=message, command=command)
        
    def start_game(self):
        print('start game')
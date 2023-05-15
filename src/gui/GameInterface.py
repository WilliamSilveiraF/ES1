from tkinter import *
import tkinter as tk
from components.CustomDialog import CustomDialog
from logic.BoardHouse import BoardHouse
from logic.Player import Player
from gui.Board import Board
from gui.Dice import Dice
from contants import NUM_JOGADORES, NUM_CASAS, LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA
from utils.get_board_house_coordinates import get_board_house_coordinates

class GameInterface:
    def __init__(self, master, player_name):
        self.master = master
        self.master.geometry(f"{LARGURA_TABULEIRO+300}x{ALTURA_TABULEIRO}")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self._create_menu()
        self._create_canvas()
        self._create_right_frame()

        self.board = Board(self.canvas)

        self.players = self._create_players()

        self.player_name = player_name
        self._create_player_text()
        
        self.dice = Dice(self.canvas, self.frame, command=lambda: self.roll_dice(self.players[0]))

        self._create_game_title()

        self._create_cards()

        self.board.draw_players(self.players)

    def atualizar_posicao_jogador(self, player):
        raio = LARGURA_CASA // 6
        player.posicao %= NUM_CASAS  # Atualiza a posição do player no tabuleiro
        x, y = get_board_house_coordinates(player.posicao)
        i = self.players.index(player)
        
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

    def _create_players(self):
        cores = ['red','yellow', 'blue']
        players = []
        for i in range(NUM_JOGADORES):
            player = Player(f'Jogador {i + 1}', cores[i])
            players.append(player)
        return players

    def _create_player_text(self):
        self.player_text = self.canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 10, 
                                                    text=f"#{self.player_name}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")

    def _create_game_title(self):
        self.canvas.create_text(LARGURA_CASA + 20, ALTURA_TABULEIRO - LARGURA_CASA - 20, text="The Game Of Life",
                        anchor='sw', font=("Futura", 12, "italic"), fill="black")

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

    def roll_dice(self, player: Player):
        steps = self.dice.roll()
        player.posicao += steps
        self.dice.draw(steps)
        self.atualizar_posicao_jogador(player)
        self.handle_new_casa_events(player)

        if player.is_broke:
            player.set_out_of_match()

            self.dice.roll_btn.destroy()
            self.dice.erase()
            # TODO SET DISABLED MODE IN CARD, RENDER A TITLE CONTAINING THAT THE PLAYER LOSED

        new_card_content = player.get_card_content()
        self._update_card(1, new_card_content)

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
            CustomDialog(self.master, title=casa.title, message=err.args[0])
        else:
            CustomDialog(self.master, title=casa.title, message=casa.description)

    def start_game(self):
        print('start game')
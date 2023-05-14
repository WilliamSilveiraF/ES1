from tkinter import *
import tkinter as tk
from tkinter import ttk
from random import randint
from PIL import Image, ImageTk
from components.CustomDialog import CustomDialog
from logic.BoardHouse import BoardHouse
from logic.Player import Player
from contants import NUM_JOGADORES, NUM_CASAS, LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA, COMPRIMENTO_LADO


CORES = ["#e6bd22", "#148bc6", "#c01960", "#54ad39"]
LIGHT_CORES = ["#edde22", "#56c2f0", "#e76da8", "#b3d880"]


class GameInterface:
    def __init__(self, master, player_name):
        self.master = master
        self.master.geometry(f"{LARGURA_TABULEIRO+300}x{ALTURA_TABULEIRO}")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self._create_menu()
        self._create_canvas()
        self._create_right_frame()

        self.jogadores = self._create_players()

        self.player_name = player_name
        self._create_player_text()
        self._create_roll_btn()
        self._create_game_title()

        self._create_cards()

        self.draw_board_spaces()
        self.draw_players()

    def atualizar_posicao_jogador(self, player):
        raio = LARGURA_CASA // 6
        player.posicao %= NUM_CASAS  # Atualiza a posição do player no tabuleiro
        x, y = self.coordenadas_casa(player.posicao)
        i = self.jogadores.index(player)
        
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
    def _create_roll_btn(self):
        style = ttk.Style()
        style.configure("Dice.TButton", bordercolor="black", borderwidth=4, relief="groove",
                        font=("Arial", 10, "bold"), background="white")
        style.layout("Dice.TButton",
                     [('Button.border', {'sticky': 'nswe', 'border': '1', 'children':
                         [('Button.padding', {'sticky': 'nswe', 'border': '1', 'children':
                             [('Button.label', {'sticky': 'nswe'})]})]})])

        self.btn_girar = ttk.Button(self.frame, text="Roll Dice",
                                    command=lambda: self.girar_dado(self.jogadores[0]), style="Dice.TButton", cursor="hand2")
        self.btn_girar.place(x=LARGURA_TABULEIRO // 2 - self.btn_girar.winfo_reqwidth() // 2,
                             y=ALTURA_TABULEIRO // 2 + LARGURA_CASA)

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

    
    def draw_board_spaces(self):
        for i in list(range(10, 20)) + list(range(20, 30)) + list(range(0, 10)) + list(range(30, 36)):
            x, y = self.coordenadas_casa(i)
            cor = CORES[i % len(CORES)]
            subcor = LIGHT_CORES[i % len(LIGHT_CORES)]

            # Calculate center of casa
            center_x = x + LARGURA_CASA / 2
            center_y = y + LARGURA_CASA / 2
            
            if i == 0:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill="#53c7f8", outline="black")
                self.arrow_image = ImageTk.PhotoImage(Image.open("media/right-arrow-resized.png"))
                self.canvas.create_image(center_x, center_y, image=self.arrow_image)

            else:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill=cor, outline="black")
                self.canvas.create_text(center_x, center_y, text=str(i+1), fill=subcor, font=("Arial", 12, "bold"))        

    
    def draw_players(self):
        raio = LARGURA_CASA // 6

        for i, jogador in enumerate(self.jogadores):
            x, y = self.coordenadas_casa(jogador.posicao)

            x += (LARGURA_CASA / 2) - raio
            if i == 0:
                y += ((LARGURA_CASA) / 10)
            elif i == 1:
                y += (LARGURA_CASA / 2) - raio
            elif i == 2:
               y += ((9 * LARGURA_CASA) / 10) - (2 * raio)
            jogador.pino = self.desenhar_jogador(x, y, jogador.cor, raio)

    def desenhar_jogador(self, x, y, cor, raio):
        centro_x, centro_y = x + raio, y + raio
        pino = self.canvas.create_oval(centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio, fill=cor)
        return pino

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
    
    def coordenadas_casa(self, index):
        espaco = (LARGURA_TABULEIRO - LARGURA_CASA) / (COMPRIMENTO_LADO - 1)
        x, y = 0, 0
        if index < COMPRIMENTO_LADO:
            x = index * espaco
            y = 0
        elif index < 2 * COMPRIMENTO_LADO - 1:
            x = LARGURA_TABULEIRO - LARGURA_CASA
            y = (index - COMPRIMENTO_LADO + 1) * espaco
        elif index < 3 * COMPRIMENTO_LADO - 2:
            x = LARGURA_TABULEIRO - LARGURA_CASA - (index - 2 * COMPRIMENTO_LADO + 2) * espaco
            y = ALTURA_TABULEIRO - LARGURA_CASA
        else:
            x = 0
            y = ALTURA_TABULEIRO - LARGURA_CASA - (index - 3 * COMPRIMENTO_LADO + 3) * espaco
        return x, y

    def desenhar_dado(self, numero):
        centro_x, centro_y = LARGURA_TABULEIRO // 2, ALTURA_TABULEIRO // 2
        lado = LARGURA_CASA
        meio_lado = lado // 2
        raio = LARGURA_CASA // 8
        dist_multiplier = 2

        self._erase_dice()

        self.dado_rectangle = self.canvas.create_rectangle(centro_x - meio_lado, centro_y - meio_lado, centro_x + meio_lado, centro_y + meio_lado, fill="white", outline="black")

        pontos = {
            1: [(0, 0)],
            2: [(-1, -1), (1, 1)],
            3: [(-1, -1), (0, 0), (1, 1)],
            4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)],
            6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
        }

        self.dado_ovals = []
        for dx, dy in pontos[numero]:
            x = centro_x + dx * raio * dist_multiplier
            y = centro_y + dy * raio * dist_multiplier
            oval = self.canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill="black")
            self.dado_ovals.append(oval)
    
    def _erase_dice(self):
        if hasattr(self, 'dado_rectangle'):
            self.canvas.delete(self.dado_rectangle)
        if hasattr(self, 'dado_ovals'):
            for oval in self.dado_ovals:
                self.canvas.delete(oval)
            self.dado_ovals = []

    def _criar_btn_girar(self):
        style = ttk.Style()
        style.configure("Dice.TButton", bordercolor="black", borderwidth=4, relief="groove",
                        font=("Arial", 10, "bold"), background="white")
        style.layout("Dice.TButton",
                     [('Button.border', {'sticky': 'nswe', 'border': '1', 'children':
                         [('Button.padding', {'sticky': 'nswe', 'border': '1', 'children':
                             [('Button.label', {'sticky': 'nswe'})]})]})])

        self.btn_girar = ttk.Button(self.frame, text="Roll Dice",
                                    command=lambda: self.girar_dado(self.jogadores[0]), style="Dice.TButton", cursor="hand2")
        self.btn_girar.place(x=LARGURA_TABULEIRO // 2 - self.btn_girar.winfo_reqwidth() // 2,
                             y=ALTURA_TABULEIRO // 2 + LARGURA_CASA)

    def girar_dado(self, player: Player):
        passos = randint(1, 6)
        player.posicao += passos

        self.canvas.delete("dado")
        self.desenhar_dado(passos)
        self.atualizar_posicao_jogador(player)
        self.handle_new_casa_events(player)

        if player.is_broke:
            player.set_out_of_match()
            
            self.btn_girar.destroy()
            self._erase_dice()
            
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
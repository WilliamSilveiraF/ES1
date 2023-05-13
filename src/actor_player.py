from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from random import randint
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from PIL import Image, ImageTk
from components.CustomDialog import CustomDialog
from utils.mask_dollar import mask_dollar
from logic.BoardHouse import BoardHouse
from logic.Player import Player
from contants import NUM_JOGADORES, NUM_CASAS, LARGURA_TABULEIRO, ALTURA_TABULEIRO, LARGURA_CASA, COMPRIMENTO_LADO


CORES = ["#e6bd22", "#148bc6", "#c01960", "#54ad39"]
LIGHT_CORES = ["#edde22", "#56c2f0", "#e76da8", "#b3d880"]


class ActorPlayer(DogPlayerInterface):
    def __init__(self, master):
        self.master = master
        self.dog_server_interface = DogActor()
        self.player_name = ''
        self.init_interface = None
        self.game_interface = None

        self.render_init_interface()

        self.master.mainloop()

    def start_match(self):
        start_status = self.dog_server_interface.start_match(3)
        message = start_status.get_message()
        
        return message

    def start_game(self):
        self.player_name = self.init_interface.name_var.get()  # Store the player name

        if not self.player_name.strip() or self.player_name.strip() == 'Enter your name':  # Check if player_name is empty
            messagebox.showwarning("Warning", "Player name is required")  # Show warning messagebox
            return  # Exit the function
        
        conn_message = self.dog_server_interface.initialize(self.player_name, self)
        messagebox.showinfo(message=conn_message)

        if conn_message != 'Conectado a Dog Server':
            return

        #match_message = self.start_match() FIXME remove comments
        #if match_message == 'Jogadores insuficientes':
        #    self.init_interface.set_waiting_other_players()
        #    return

        self.render_game_interface()
        
    def render_init_interface(self):
        if self.game_interface:
            self.game_interface.frame.destroy()
            self.game_interface = None

        self.player_name = ''
        self.init_interface = InitInterface(self.master)
        self.init_interface.button.configure(command=self.start_game)

    def render_game_interface(self):
        if self.init_interface:
            self.init_interface.frame.destroy()  # Close the initial page
            self.init_interface = None
        
        self.game_interface = GameInterface(self.master, self.player_name)

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        self.render_game_interface()

    def receive_withdrawal_notification(self):
        messagebox.showwarning("Warning", "Some player left, this is the end of the game.")
        self.render_init_interface()

class InitInterface(ActorPlayer):
    def __init__(self, master):
        self.master = master

        # Load and adjust the background image
        self.image = Image.open("media/initpage.jpg")  # replace "path_to_your_image.jpg" with your image file path
        img_width, img_height = self.image.size
        new_width = LARGURA_TABULEIRO+300
        new_height = int((new_width / img_width) * img_height)  # maintain aspect ratio

        self.image = self.image.resize((new_width, new_height), Image.ANTIALIAS)  # resize the image
        self.photo_image = ImageTk.PhotoImage(self.image)

        self.master.geometry(f"{new_width}x{new_height}")  # Set the window size

        self.frame = Frame(self.master)
        self.frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.frame, width=new_width, height=new_height)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor="nw")

        # Create an entry for the name
        self.name_var = StringVar()
        self.name_entry = Entry(self.frame, textvariable=self.name_var)
        self.name_entry.place(relx=0.5, rely=0.80, anchor="center")
        self.name_entry.insert(0, "Enter your name")
        self.name_entry.bind("<FocusIn>", self.add_placeholder)
        self.name_entry.bind("<FocusOut>", self.clear_placeholder)

        # Create and place the button
        style = ttk.Style()
        style.configure("C.TButton",
                        foreground="#FFFFFF",
                        background="#198754",
                        font=("Arial", 20, "bold"),
                        padding=10)
        style.map("C.TButton",
                  foreground=[('pressed', '#FFFFFF'), ('active', '#FFFFFF')],
                  background=[('pressed', '!disabled', '#4cae4c'), ('active', '#8cbe8c')]
                  )
        self.button = ttk.Button(self.frame, text="Jogar", style="C.TButton", cursor="hand2")
        self.button.pack(side="bottom", pady=20)
        self.button.place(relx=0.5, rely=0.9, anchor="center")

    def add_placeholder(self, event):
        if self.name_entry.get() == 'Enter your name':
            self.name_entry.delete(0, END)
    
    def clear_placeholder(self, event):
        if self.name_entry.get() == '':
            self.name_entry.insert(0, 'Enter your name')

    def set_waiting_other_players(self):
        style = ttk.Style()
        style.configure("Blue.TButton",
                foreground="white",
                background="#2596be",
                font=("Arial", 20, "bold"),
                padding=10)
        style.map("C.TButton",
                  foreground=[],
                  background=[]
                  )
        self.name_entry.destroy()
        self.button.configure(text="Aguardando outros Jogadores", command=None, style="Blue.TButton", cursor='watch')

class GameInterface:
    def __init__(self, master, player_name):
        self.master = master
        self.master.geometry(f"{LARGURA_TABULEIRO+300}x{ALTURA_TABULEIRO}")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # set the window size for the game interface
       
        self.menubar = Menu(self.master)
        self.menubar.option_add('*tearOff', FALSE)
        self.master['menu'] = self.menubar
        
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.menu_file.add_command(label='Restaurar estado inicial', command=self.start_game)

        self.canvas = tk.Canvas(self.frame, width=LARGURA_TABULEIRO, height=ALTURA_TABULEIRO, bg='white')
        self.canvas.pack(side="left")

        self.right_frame = tk.Canvas(self.frame, width=300, height=ALTURA_TABULEIRO, bg='white')
        self.right_frame.pack(side="right")

        self.jogadores = self._criar_jogadores()

        self.player_name = player_name
        self.player_text = self.canvas.create_text(LARGURA_CASA + 10, LARGURA_CASA + 10, 
                                                    text=f"#{player_name}", anchor="nw",
                                                    font=("Arial", 16, "bold"), fill="#172934")
        self._criar_btn_girar()
        
        self.canvas.create_text(LARGURA_CASA + 20, ALTURA_TABULEIRO - LARGURA_CASA - 20, text="The Game Of Life",
                        anchor='sw', font=("Futura", 12, "italic"), fill="black")

        self._criar_cards()

        self.desenhar_casas()
        self.desenhar_jogadores()

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

    def desenhar_casas(self):
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
    
    def _criar_jogadores(self):
        cores = ['red','yellow', 'blue']
        jogadores = []
        for i in range(NUM_JOGADORES):
            jogador = Player(f'Jogador {i + 1}', cores[i])
            jogadores.append(jogador)
        return jogadores

    
    def desenhar_jogadores(self):
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

    def _criar_cards(self):
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
def main():
    root = Tk()
    ActorPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

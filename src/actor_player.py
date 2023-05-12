from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from random import randint
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from PIL import Image, ImageTk
from components.CustomDialog import CustomDialog
from utils.mask_dollar import mask_dollar
from enum import Enum
import math

NUM_JOGADORES = 5
NUM_CASAS = 36
LARGURA_TABULEIRO = 800
ALTURA_TABULEIRO = 800
LARGURA_CASA = 80
COMPRIMENTO_LADO = 10
CORES = ["#e6bd22", "#148bc6", "#c01960", "#54ad39"]
LIGHT_CORES = ["#edde22", "#56c2f0", "#e76da8", "#b3d880"]

class Jogador:
    def __init__(self, player_id, cor, posicao, salario):
        self.player_id = player_id
        self.cor = cor
        self.posicao = posicao
        self.salario = salario
        self.child_amount = 0
        self.dinheiro = 100000
        self.is_retired = False
        self.is_playing = True
        self.is_life_insured = False
        self.is_vehicle_insured = False

    def increase_salary_10_percent(self):
        self.salario = math.ceil(1.1 * self.salario)
    
    def increase_salary_20_percent(self):
        self.salario = math.ceil(1.2 * self.salario)
    
    def add_child(self):
        if self.child_amount == 4:
            raise ValueError('A player can only have up to 4 children. So no events will be reflected back to you this turn.')
        self.child_amount += 1

    def handle_default_turn_income(self):
        COST_BY_CHILD = -500
        transaction = self.salario

        if self.is_retired:
            transaction += 5000

        transaction += self.child_amount * COST_BY_CHILD

        self.dinheiro += transaction

    def apply_income_tax(self):
        BASE = 0.7
        self.dinheiro = math.ceil(BASE * self.dinheiro)
    
    def handle_internship(self):
        self.dinheiro -= math.ceil(0.5 * self.salario)
    
    def handle_volunter_work(self):
        self.dinheiro -= self.salario

    def buy_life_insurance(self):
        if self.is_life_insured:
            raise ValueError("Player already has life insurance. So no events will be reflected back to you this turn.")

        self.dinheiro -= 10000
        self.is_life_insured = True

    def buy_car_insurance(self):
        if self.is_vehicle_insured:
            raise ValueError("Player already has vehicle insurance. So no events will be reflected back to you this turn.")
        
        self.dinheiro -= 8000
        self.is_vehicle_insured = True

    def set_retirement(self):
        if self.is_retired:
            raise ValueError('You already is retired. So no events will be reflected back to you this turn.')
        self.is_retired = True
        
class Casa(Enum):
    INIT = (0, 'Init House', 'Today is your lucky day! By passing at the beginning, you have won U$$ 60000.', 60000)
    GRADUATION = (1, 'You graduated', 'Congratulations, you graduated!! With that you must pay tuition of U$$ 20000 from your college.', -20000)
    BIRTH = (2, 'Birth', 'Congratulations, a new child has joined your family!. Remember, with every joy comes new responsibilities. Each turn you must pay U$$ 500 by child.', 0)
    LOTTERY = (3, 'Lottery', "You've won the lottery! Collect an immediate U$$ 75000 bonus to represent your winnings.", 75000)
    MOUNT_EVEREST = (4, 'Mount Everest Expedition', "You've decided to climb Mount Everest! Pay U$$ 5000 to cover the expedition costs.", -5000)
    PROMOTION = (5, 'Promotion', 'Congratulations, your salary increases by 10 percent.', 0)
    ADOPTION = (6, 'Adoption', 'Your heart and home have expanded with the adoption of a child. Celebrate this moment and remember, every child is a bundle of joy and a responsibility to shape the future. Each turn you must pay U$$ 500 by child.', 0)
    ROBBERY = (7, 'Robbery', "Unfortunately, you've been robbed. Pay U$$ 10000 to represent the financial loss.", -10000)
    BACKPACKING = (8, 'Backpacking Trip', "You've decided to go backpacking through Europe! Pay U$$ 15000 to cover the trip costs.", -15000)
    INTERNSHIP = (9, 'Internship', 'You have landed an internship in your field! This is a great step towards your career. You will gain valuable experience, but you will earn only half your salary this turn as internships are typically low-paying.', 0)
    CHILD_GRADUATION = (10, "Child's Graduation", 'Your child has hit a significant milestone - university graduation! This proud moment comes with expenses. Make a U$$ 5000 payment to cover the cost of the graduation ceremony, from the gown to the celebratory dinner.', -5000)
    INVESTMENT = (11, 'Investment', "You've decided to invest some money. You will gain U$$ 12500.", 12500)
    CORAL_REEF_DIVE = (12, 'Coral Reef Dive', "You've decided to dive in the Coral Reef! Pay U$$ 6000 to cover the dive costs.", -6000)
    POST_GRADUATION = (13, 'Post-Graduation', 'You have completed your postgraduate studies! This milestone is an important step in your career and deserves a reward. Collect U$$ 10000 bonus to reflect your increased qualifications.', 10000)
    SCHOOL_CHANGE = (14, 'School Change', "Your child's education journey requires a school change. Whether it's due to a move or just seeking better opportunities, there are costs involved. Pay U$$ 7000 for the move, new uniforms, and other related expenses.", -7000)
    LIFE_INSURANCE = (15, 'Life Insurance', "You've decided to buy life insurance. Pay U$$ 10000 to represent the insurance premium.", 0) 
    MARATHON = (16, 'Marathon', "You've decided to run a marathon! Pay U$$ 2500 to cover the registration and training costs.", -2500)
    ENTREPRENEUR = (17, 'Entrepreneur', 'You have taken the bold step of starting your own business! This exciting venture comes with its costs. Pay U$$ 25000 to cover the startup costs.', -25000)
    FAMILY_TRIP = (18, 'Family Trip', "Quality time alert! You're taking a well-deserved family trip. It's time for relaxation and adventures. Pay U$$ 12000 for the trip expenses, including travel, accommodation, and daily allowances.", -12000)
    INHERITANCE = (19, 'Inheritance', "You've inherited a large sum of money. Collect U$$ 100000 bonus to represent the inheritance.", 100000)
    SPACE_TRAVEL = (20, 'Space Travel', "You've decided to go to space! Pay U$$ 30000 to cover the travel costs.", -30000)
    RETIREMENT = (21, 'Retirement', "You've retired after a long and successful career! It's time to relax and enjoy the fruits of your labor. Now, you will collect U$$ 5000 bonus each turn.", 0)
    CHILDREN_WEDDING = (22, "Children's Wedding", "Your child is getting married! A proud and emotional moment for you. However, weddings can be expensive. Pay U$$ 17500 for the wedding party, from the venue to the food and the decorations.", -17500)
    CAR_INSURANCE = (23, 'Car Insurance', "You've decided to buy car insurance. Pay U$$ 8000 amount to represent the insurance premium.", 0)
    AFRICAN_SAFARI = (24, 'African Safari', "You've decided to go on a safari in Africa! Pay U$$ 16000 amount to cover the trip costs.", -16000)
    CAREER_CHANGE = (25, 'Career Change', 'You have decided to change your career! This brave move opens up new opportunities, your salary increases by 20 percent.', 0)
    MUSIC_LESSON = (26, 'Music Lesson', 'Your children have shown an interest in music and want to learn an instrument. This could be the start of a lifelong passion or even a career. Pay U$$ 2500 for the music lessons, including the cost of the instrument and the tutor.', -2500)
    INCOME_TAX = (27, 'Income Tax', "It's income tax time. Pay 30 percent of your total money to represent your taxes.", 0)
    ANTARCTIC_EXPEDITION = (28, 'Antarctic Expedition', "You've decided to visit Antarctica! Pay U$$ 22500 to cover the trip costs.", -22500)
    VOLUNTEER_WORK = (29, 'Volunteer Work', 'You have decided to do volunteer work. This noble act might not provide a salary this turn, but it brings a great sense of fulfillment.', 0)
    SPORTS_COMPETITION = (30, 'Sports Competition', "Your children have entered a sports competition! They're excited and nervous. Pay U$$ 3000 for the sports equipment, team uniforms, and other related expenses.", -3000)
    CHARITY_HOUSE = (31, 'Charity House', "You've decided to make a generous donation to a charity that's close to your heart. Pay U$$ 10000 amount to represent your charitable contribution.", -10000)
    MOTORCYCLE_JOURNEY = (32, 'Motorcycle Journey on Route 66', "You've decided to ride Route 66 on a motorcycle! Pay U$$ 8000 to cover the trip costs.", -8000)
    REMOTE_WORK = (33, 'Remote Work', 'You have landed the opportunity to work remotely! This gives you more flexibility and time to spend with family or on hobbies. Receive your normal salary this turn and gain U$$ 3000 bonus to represent the savings on transportation and work clothes.', 3000)
    BIRTHDAY_PARTY = (34, 'Birthday Party', "It's time to celebrate! One of your children has a birthday. You're throwing a party complete with cake, games, and party favors. Pay U$$ 7500 for the party expenses.", -7500)
    WINDFALL = (35, 'Windfall', "You've received an unexpected windfall, perhaps from a forgotten investment or a distant relative. Collect U$$ 20000 bonus to represent the unexpected influx of money.", 20000)

    def __init__(self, posicao, title, description, transaction):
        self.posicao = posicao
        self.title = title
        self.description = description
        self.transaction = transaction

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
        self.cash_text = self.canvas.create_text(LARGURA_TABULEIRO - LARGURA_CASA - 10, LARGURA_CASA + 10,
                                                  text=f"R$ 1000", anchor="ne",
                                                  font=("Arial", 16, "bold"), fill="green")
        self._criar_btn_girar()
        
        self.canvas.create_text(LARGURA_CASA + 20, ALTURA_TABULEIRO - LARGURA_CASA - 20, text="The Game Of Life",
                        anchor='sw', font=("Futura", 12, "italic"), fill="black")

        self._criar_cards()

        self.desenhar_casas()
        self.desenhar_jogadores()

    def atualizar_posicao_jogador(self, jogador):
        jogador.posicao %= NUM_CASAS  # Atualiza a posição do jogador no tabuleiro
        x, y = self.coordenadas_casa(jogador.posicao)
        i = self.jogadores.index(jogador)
        x += i * 10  # Ajuste na posição horizontal do jogador para evitar sobreposição
        y += i * 10  # Ajuste na posição vertical do jogador para evitar sobreposição
        raio = LARGURA_CASA // 6  # Reduzir o tamanho do pino do jogador alterando o valor do raio
        centro_x, centro_y = x + raio, y + raio
        self.canvas.coords(jogador.pino, centro_x - raio, centro_y - raio, centro_x + raio, centro_y + raio)

    def desenhar_casas(self):
        for i in list(range(10, 20)) + list(range(20, 30)) + list(range(0, 10)) + list(range(30, 36)):
            x, y = self.coordenadas_casa(i)
            cor = CORES[i % len(CORES)]
            subcor = LIGHT_CORES[i % len(LIGHT_CORES)]

            # Calculate center of casa
            center_x = x + LARGURA_CASA / 2
            center_y = y + LARGURA_CASA / 2
            
            if i == 0:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill="#fefefe", outline="black")
                self.canvas.create_text(center_x, center_y, text=str(i+1), fill='#172934', font=("Arial", 12, "bold"))
            else:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill=cor, outline="black")
                self.canvas.create_text(center_x, center_y, text=str(i+1), fill=subcor, font=("Arial", 12, "bold"))        
    
    def _criar_jogadores(self):
        cores = ['red', 'blue', 'green', 'yellow', 'purple']
        jogadores = []
        for i in range(NUM_JOGADORES):
            jogador = Jogador(f'Jogador {i + 1}', cores[i], 0, 0)
            jogadores.append(jogador)
        return jogadores

    
    def desenhar_jogadores(self):
        for i, jogador in enumerate(self.jogadores):
            x, y = self.coordenadas_casa(jogador.posicao)
            x += i * 10  # Ajuste na posição horizontal do jogador para evitar sobreposição
            y += i * 10  # Ajuste na posição vertical do jogador para evitar sobreposição
            jogador.pino = self.desenhar_jogador(x, y, jogador.cor)

    def desenhar_jogador(self, x, y, cor):
        raio = LARGURA_CASA // 6  # Reduzir o tamanho do pino do jogador alterando o valor do raio
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
            ###fbe34c
            y1 = card_space * (i + 1) + card_height * i
            x2 = x1 + card_width
            y2 = y1 + card_height
            # shadow
            self._create_rounded_rect(x1+5, y1+5, x2+5, y2+5, radius=20, fill=shadow_color)
            # card
            self._create_rounded_rect(x1, y1, x2, y2, radius=20, fill=card_bg, outline=card_outline)
            self.right_frame.create_text(x1 + 10, y1 + 10, text=subtitles[i], anchor="nw", font=("Arial", 14, "bold"), fill=card_title)

        first_card_lines = [
            { 'field': 'Bank', 'value': 'U$$ 100000' },
            { 'field': 'Salary', 'value': 'U$$ 5000' },
            { 'field': 'Childs', 'value': 'U$$ 0' },
            { 'field': 'Retirement', 'value': 'U$$ 5000' },
            { 'field': 'Life insurance', 'value': 'Yes' },
            { 'field': 'Vehicle insurance', 'value': 'Yes' }
        ]
        y_start = card_space + 40

        for line in first_card_lines:
            self.right_frame.create_text(x1 + 10, y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#22471a')
            self.right_frame.create_text(x1 + card_width - 10, y_start, text=line['value'], anchor="ne", font=("Arial", 12, "bold"), fill='#22471a')
            y_start += 22

        second_card_lines = [
            { 'field': 'Bank', 'value': 'U$$ 142500' },
            { 'field': 'Salary', 'value': 'U$$ 5500' },
            { 'field': 'Childs', 'value': 'U$$ 0' },
            { 'field': 'Retirement', 'value': 'U$$ 0' },
            { 'field': 'Life insurance', 'value': 'No' },
            { 'field': 'Vehicle insurance', 'value': 'Yes' }
        ]
        y_start = 2 * card_space + card_height + 40

        for line in second_card_lines:
            self.right_frame.create_text(x1 + 10, y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#043c50')
            self.right_frame.create_text(x1 + card_width - 10, y_start, text=line['value'], anchor="ne", font=("Arial", 12), fill='#043c50')
            y_start += 22
        
        third_card_lines = [
            { 'field': 'Bank', 'value': 'U$$ 142500' },
            { 'field': 'Salary', 'value': 'U$$ 5500' },
            { 'field': 'Childs', 'value': 'U$$ 0' },
            { 'field': 'Retirement', 'value': 'U$$ 0' },
            { 'field': 'Life insurance', 'value': 'No' },
            { 'field': 'Vehicle insurance', 'value': 'Yes' }
        ]
        y_start = 3 * card_space + 2 * card_height + 40

        for line in third_card_lines:
            self.right_frame.create_text(x1 + 10, y_start, text=line['field'], anchor="nw", font=("Arial", 12, "bold"), fill='#043c50')
            self.right_frame.create_text(x1 + card_width - 10, y_start, text=line['value'], anchor="ne", font=("Arial", 12), fill='#043c50')
            y_start += 22

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

        self.canvas.delete("dado")
        self.canvas.create_rectangle(centro_x - meio_lado, centro_y - meio_lado, centro_x + meio_lado, centro_y + meio_lado, fill="white", outline="black", tags="dado")

        pontos = {
            1: [(0, 0)],
            2: [(-1, -1), (1, 1)],
            3: [(-1, -1), (0, 0), (1, 1)],
            4: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
            5: [(-1, -1), (-1, 1), (0, 0), (1, -1), (1, 1)],
            6: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
        }

        for dx, dy in pontos[numero]:
            x = centro_x + dx * raio * dist_multiplier
            y = centro_y + dy * raio * dist_multiplier
            self.canvas.create_oval(x - raio, y - raio, x + raio, y + raio, fill="black")
    
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
    
    def handle_new_casa_events(self, jogador: Jogador):
        new_pos = jogador.posicao

        for casa in Casa:
            if new_pos == casa.posicao:
                
                jogador.handle_default_turn_income()
                
                jogador.dinheiro += casa.transaction
                
                try:
                    is_required_child = casa == Casa.CHILD_GRADUATION or casa == Casa.SCHOOL_CHANGE or casa == Casa.CHILDREN_WEDDING \
                        or casa == Casa.MUSIC_LESSON or casa == Casa.SPORTS_COMPETITION or casa == Casa.BIRTHDAY_PARTY

                    if is_required_child and jogador.child_amount == 0:
                        raise ValueError("A child is required for this position. So no events will be reflected back to you this turn.")

                    if casa == Casa.BIRTH or casa == Casa.ADOPTION:
                        jogador.add_child()
                    elif casa == Casa.PROMOTION:
                        jogador.increase_salary_10_percent()
                    elif casa == Casa.INTERNSHIP:
                        jogador.handle_internship()
                    elif casa == Casa.LIFE_INSURANCE:
                        jogador.buy_life_insurance()
                    elif casa == Casa.CAR_INSURANCE:
                        jogador.buy_car_insurance()
                    elif casa == Casa.RETIREMENT:
                        jogador.set_retirement()
                    elif casa == Casa.CAREER_CHANGE:
                        jogador.increase_salary_20_percent()
                    elif casa == Casa.INCOME_TAX:
                        jogador.apply_income_tax()
                    elif casa == Casa.VOLUNTEER_WORK:
                        jogador.handle_volunter_work()
                except Exception as err:
                    CustomDialog(self.master, title=casa.title, message=err.args[0])
                else:
                    CustomDialog(self.master, title=casa.title, message=casa.description)
                self.canvas.itemconfigure(self.cash_text, text=f"U$$ {jogador.dinheiro}")
                break
        
        
        #d = CustomDialog(self.master, title="You landed on a special casa!", 
        #                    message=f"{self.player_name} landed on casa 5.", buttons=buttons)

    def girar_dado(self, jogador):
        passos = randint(1, 6)
        jogador.posicao += passos

        centro_x, centro_y = LARGURA_TABULEIRO // 2, ALTURA_TABULEIRO // 2
        self.canvas.delete("dado")
        self.desenhar_dado(passos)
        self.atualizar_posicao_jogador(jogador)
        self.handle_new_casa_events(jogador)
    
    def start_game(self):
        print('start_game')

def main():
    root = Tk()
    ActorPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

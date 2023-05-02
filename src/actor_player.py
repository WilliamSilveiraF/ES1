from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from random import randint
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor

NUM_JOGADORES = 5
NUM_CASAS = 40
LARGURA_TABULEIRO = 800
ALTURA_TABULEIRO = 800
LARGURA_CASA = 80
COMPRIMENTO_LADO = NUM_CASAS // 4
CORES = ["#f3d997", "#bae6af", "#f88379", "#eeeeee"]

class Jogador:
    def __init__(self, nome, cor, posicao, salario):
        self.nome = nome
        self.cor = cor
        self.posicao = posicao
        self.salario = salario
        self.dinheiro = 0

class GameInterface:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=LARGURA_TABULEIRO, height=ALTURA_TABULEIRO, bg='white')
        self.canvas.pack(side="left")

        self.right_frame = tk.Canvas(self.frame, width=300, height=ALTURA_TABULEIRO, bg='white')
        self.right_frame.pack(side="right")

        self.jogadores = self._criar_jogadores()

        self.cash_text = self.canvas.create_text(LARGURA_TABULEIRO - LARGURA_CASA - 10, LARGURA_CASA + 10,
                                                  text=f"R$ 1000", anchor="ne",
                                                  font=("Arial", 16, "bold"), fill="green")
        self._criar_btn_girar()
        
        self.canvas.create_text(LARGURA_TABULEIRO // 2, ALTURA_TABULEIRO // 2 + LARGURA_CASA + 20, text="Jogo da Vida",
                                font=("Futura", 30, "bold italic"), fill="black")

        self._criar_cards()

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
        for i in range(NUM_CASAS):
            x, y = self.coordenadas_casa(i)
            cor = CORES[i % len(CORES)]
            if i == 0:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill="#343434", outline="black")
            else:
                self.canvas.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill=cor, outline="black")

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

    def _criar_cards(self):
        card_width = int(0.8 * 300)
        card_height = int(ALTURA_TABULEIRO / 4)
        card_space = int((ALTURA_TABULEIRO - 3 * card_height) / 4)

        x1 = (300 - card_width) // 2
        subtitles = ["Perfil", "Seguros", "Dívidas"]

        for i in range(3):
            y1 = card_space * (i + 1) + card_height * i
            x2 = x1 + card_width
            y2 = y1 + card_height
            self.right_frame.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
            self.right_frame.create_text(x1 + 10, y1 + 10, text=subtitles[i], anchor="nw", font=("Arial", 14, "bold"))

        first_card_lines = ["Quantidade de filhos: 0", "Status civil: Solteiro", "Ações: Não", "Carreira: Negócios"]
        y_start = card_space + 40

        for line in first_card_lines:
            self.right_frame.create_text(x1 + 10, y_start, text=line, anchor="nw", font=("Arial", 12))
            y_start += 20

        second_card_lines = ["Seguro de Vida: Sim", "Seguro veicular: Sim", "Seguro de Casa: Não"]
        y_start = 2 * card_space + card_height + 40

        for line in second_card_lines:
            self.right_frame.create_text(x1 + 10, y_start, text=line, anchor="nw", font=("Arial", 12))
            y_start += 20

    def coordenadas_casa(self, index):
        espaco = (LARGURA_TABULEIRO - LARGURA_CASA) / (COMPRIMENTO_LADO - 1)
        x, y = 0, 0
        if index < COMPRIMENTO_LADO:
            x = index * espaco
            y = 0
        elif index < 2 * COMPRIMENTO_LADO:
            x = LARGURA_TABULEIRO - LARGURA_CASA
            y = (index - COMPRIMENTO_LADO) * espaco
        elif index < 3 * COMPRIMENTO_LADO:
            x = LARGURA_TABULEIRO - LARGURA_CASA - (index - 2 * COMPRIMENTO_LADO) * espaco
            y = ALTURA_TABULEIRO - LARGURA_CASA
        else:
            x = 0
            y = ALTURA_TABULEIRO - LARGURA_CASA - (index - 3 * COMPRIMENTO_LADO) * espaco

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
        style.configure("Custom.TButton", bordercolor="black", borderwidth=4, relief="groove",
                        font=("Arial", 10, "bold"), background="white")
        style.layout("Custom.TButton",
                     [('Button.border', {'sticky': 'nswe', 'border': '1', 'children':
                         [('Button.padding', {'sticky': 'nswe', 'border': '1', 'children':
                             [('Button.label', {'sticky': 'nswe'})]})]})])

        self.btn_girar = ttk.Button(self.frame, text="Girar Dados",
                                    command=lambda: self.girar_dado(self.jogadores[0]), style="Custom.TButton")
        self.btn_girar.place(x=LARGURA_TABULEIRO // 2 - self.btn_girar.winfo_reqwidth() // 2,
                             y=ALTURA_TABULEIRO // 2 + LARGURA_CASA + 60)
    

    def girar_dado(self, jogador):
        passos = randint(1, 6)
        jogador.posicao += passos

        centro_x, centro_y = LARGURA_TABULEIRO // 2, ALTURA_TABULEIRO // 2
        self.canvas.delete("dado")
        self.desenhar_dado(passos)
        self.atualizar_posicao_jogador(jogador)
        # self.update_cash(jogador) FIXME

    def update_cash(self, jogador):
        jogador.dinheiro += 100 
        self.canvas.itemconfigure(self._cash_text, text=f"R$ {jogador.dinheiro}")

class ActorPlayer(DogPlayerInterface):
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Jogo da Vida Simplificado")
        self.game_interface = GameInterface(self.master)

        self.menubar = Menu(self.master)
        self.menubar.option_add('*tearOff', FALSE)
        self.master['menu'] = self.menubar
        
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

        self.menu_file.add_command(label='Iniciar jogo', command=self.start_match)
        self.menu_file.add_command(label='Restaurar estado inicial', command=self.start_game)

        self.game_interface.desenhar_casas()
        self.game_interface.desenhar_jogadores()

        player_name = simpledialog.askstring(title="Player identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)

        self.master.mainloop()

    def start_match(self):
        start_status = self.dog_server_interface.start_match(5)
        message = start_status.get_message()
        messagebox.showinfo(message=message)

    def start_game(self):
        print('start_game')

    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)



ActorPlayer()
#def main():
#    ActorPlayer()
#
#if __name__ == "__main__":
#    main()

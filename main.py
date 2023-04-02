import tkinter as tk
from tkinter import ttk
from random import randint
import math

NUM_JOGADORES = 5
NUM_CASAS = 40
LARGURA_TABULEIRO = 800
ALTURA_TABULEIRO = 800
NUM_CASAS = 40
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

def criar_jogadores():
    cores = ['red', 'blue', 'green', 'yellow', 'purple']
    jogadores = []
    for i in range(NUM_JOGADORES):
        jogador = Jogador(f'Jogador {i + 1}', cores[i], 0, 0)
        jogadores.append(jogador)
    return jogadores

def desenhar_dado(tabuleiro, centro_x, centro_y, numero):
    lado = LARGURA_CASA  # Increase the size of the dice by setting the 'lado' equal to LARGURA_CASA
    meio_lado = lado / 2
    raio = LARGURA_CASA / 8  # Increase the size of the dots
    dist_multiplier = 2  # Increase the distance between the dots

    # Draw the dice
    tabuleiro.create_rectangle(centro_x - meio_lado, centro_y - meio_lado, centro_x + meio_lado, centro_y + meio_lado, fill="white", outline="black")

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
        tabuleiro.create_oval(x - raio, y - raio, x + raio, y + raio, fill="black")

def girar_dado(jogador):
    passos = randint(1, 6)
    jogador.posicao += passos

    return passos

def coordenadas_casa(index):
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

def desenhar_jogador(tabuleiro, x, y, cor):
    raio_jogador = 5
    x_jogador = x + LARGURA_CASA // 2
    y_jogador = y + LARGURA_CASA // 2
    tabuleiro.create_oval(x_jogador - raio_jogador, y_jogador - raio_jogador, x_jogador + raio_jogador, y_jogador + raio_jogador, fill=cor)

def main():
    root = tk.Tk()
    root.title("Jogo da Vida Simplificado")

    frame = tk.Frame(root)
    frame.pack()

    tabuleiro = tk.Canvas(frame, width=LARGURA_TABULEIRO, height=ALTURA_TABULEIRO, bg='white')
    tabuleiro.pack(side="left")

    retangulo_direita = tk.Canvas(frame, width=300, height=ALTURA_TABULEIRO, bg='white')
    retangulo_direita.pack(side="right")

    # Draw three cards vertically centered within the right frame
    card_width = int(0.8 * 300)
    card_height = int(ALTURA_TABULEIRO / 4)
    card_space = int((ALTURA_TABULEIRO - 3 * card_height) / 4)

    x1 = (300 - card_width) // 2
    subtitles = ["Perfil", "Seguros", "Dívidas"]

    for i in range(3):
        y1 = card_space * (i + 1) + card_height * i
        x2 = x1 + card_width
        y2 = y1 + card_height
        retangulo_direita.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
        retangulo_direita.create_text(x1 + 10, y1 + 10, text=subtitles[i], anchor="nw", font=("Arial", 14, "bold"))

    # Add the text to the first card
    first_card_lines = ["Quantidade de filhos: 0", "Status civil: Solteiro", "Ações: Não", "Carreira: Negócios"]
    y_start = card_space + 40

    for line in first_card_lines:
        retangulo_direita.create_text(x1 + 10, y_start, text=line, anchor="nw", font=("Arial", 12))
        y_start += 20

    # Add the text to the second card
    second_card_lines = ["Seguro de Vida: Sim", "Seguro veicular: Sim", "Seguro de Casa: Não"]
    y_start = 2 * card_space + card_height + 40

    for line in second_card_lines:
        retangulo_direita.create_text(x1 + 10, y_start, text=line, anchor="nw", font=("Arial", 12))
        y_start += 20

    for i in range(NUM_CASAS):
        x, y = coordenadas_casa(i)
        cor = CORES[i % len(CORES)]
        if i == 0:
            tabuleiro.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill="#343434", outline="black")
        else:
            tabuleiro.create_rectangle(x, y, x + LARGURA_CASA, y + LARGURA_CASA, fill=cor, outline="black")

    jogadores = criar_jogadores()
    if jogadores is not None:
        for jogador in jogadores:
            x, y = coordenadas_casa(0)
            desenhar_jogador(tabuleiro, x, y, jogador.cor)

    centro_x, centro_y = LARGURA_TABULEIRO // 2, ALTURA_TABULEIRO // 2
    desenhar_dado(tabuleiro, centro_x, centro_y, 5)

    tabuleiro.create_text(LARGURA_TABULEIRO // 2, ALTURA_TABULEIRO // 2 + LARGURA_CASA + 20, text="Jogo da Vida", font=("Futura", 30, "bold italic"), fill="black")
    
    # Create a custom style for the button
    style = ttk.Style()
    style.configure("Custom.TButton", bordercolor="black", borderwidth=4, relief="groove", font=("Arial", 10, "bold"), background="white")
    style.layout("Custom.TButton", [('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [('Button.padding', {'sticky': 'nswe', 'border': '1', 'children': [('Button.label', {'sticky': 'nswe'})]})]})])

    # Move the "Girar Dados" button below the dice and apply the custom style
    btn_girar = ttk.Button(root, text="Girar Dados", command=lambda: girar_dado(jogadores[0]), style="Custom.TButton")
    btn_girar.place(x=LARGURA_TABULEIRO // 2 - btn_girar.winfo_reqwidth() // 2, y=ALTURA_TABULEIRO // 2 + LARGURA_CASA + 60)

    vez = "Vez: jogador 3"
    tabuleiro.create_text(LARGURA_CASA + 160, LARGURA_CASA + 10, text=vez, anchor="ne", font=("Arial", 16, "bold"), fill="black")

    cash = "$1000"
    tabuleiro.create_text(LARGURA_TABULEIRO - LARGURA_CASA - 10, LARGURA_CASA + 10, text=cash, anchor="ne", font=("Arial", 16, "bold"), fill="green")
    root.mainloop()
if __name__ == "__main__":
    main()
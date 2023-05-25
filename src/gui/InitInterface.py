from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
from constants import LARGURA_TABULEIRO

class InitInterface:
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

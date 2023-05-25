from tkinter import *
from tkinter import messagebox
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from gui.GameInterface import GameInterface
from gui.InitInterface import InitInterface

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
        players = start_status.get_players()

        return message, players

    def start_game(self):
        self.player_name = self.init_interface.name_var.get()  # Store the player name

        if not self.player_name.strip() or self.player_name.strip() == 'Enter your name':  # Check if player_name is empty
            messagebox.showwarning("Warning", "Player name is required")  # Show warning messagebox
            return  # Exit the function
        
        conn_message = self.dog_server_interface.initialize(self.player_name, self)
        messagebox.showinfo(message=conn_message)

        if conn_message != 'Conectado a Dog Server':
            return

        message, players = self.start_match()
        if message == 'Jogadores insuficientes':
            self.init_interface.set_waiting_other_players()
            return

        self.render_game_interface(players)
        
    def render_init_interface(self):
        if self.game_interface:
            self.game_interface.frame.destroy()
            self.game_interface = None

        self.player_name = ''
        self.init_interface = InitInterface(self.master)
        self.init_interface.button.configure(command=self.start_game)

    def render_game_interface(self, players):
        if self.init_interface:
            self.init_interface.frame.destroy()
            self.init_interface = None

        self.game_interface = GameInterface(self.master, self.player_name, players, self.dog_server_interface)

    def receive_start(self, start_status):
        message = start_status.get_message()
        players = start_status.get_players()
        messagebox.showinfo(message=message)
        self.render_game_interface(players)

    def receive_move(self, move):
        self.game_interface.handle_move(move)

    def receive_withdrawal_notification(self):
        messagebox.showwarning("Warning", "Some player left, this is the end of the game.")
        self.render_init_interface()

def main():
    root = Tk()
    ActorPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

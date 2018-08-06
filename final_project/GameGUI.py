import tkinter as tk
from tkinter import ttk
import math

"""
Layout:
+---------------------GameGUI---------------------+
| +------------------GameBoard------------------+ |
| | +-PLayerInfo1-+ +--Board--+ +-PLayerInfo1-+ | |
| | |             | |         | |             | | |
| | |             | |         | |             | | |
| | |             | |         | |             | | |
| | +-------------+ +---------+ +-------------+ | |
| +---------------------------------------------+ |
| +------------------Settings-------------------+ |
| | +------Player1------+ +------Player1------+ | |
| | | * Computer        | | * Computer        | | |
| | | * Human name      | | * Human name      | | |
| | +-------------------+ +-------------------+ | |
| | +---PredictSettings-----------------------+ | |
| | | * Show value and remoteness             | | |
| | +-----------------------------------------+ | |
| +---------------------------------------------+ |
+-------------------------------------------------+
"""

IMG_SLOT_TRUE = "Leaf.png"
IMG_SLOT_FALSE = "Water.png"
IMG_BLACK_PIECE = "Frog_0.png"
IMG_WHITE_PIECE = "Frog_1.png"

SLOT_WIDTH = 18
SLOT_HEIGHT = 8

class GameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.game_board = GameBoard(master=self.window)  # TODO: control board_row and board_col
        self.game_board.frame.grid(row=0, column=0)

        self.settings = Settings(master=self.window)
        self.settings.frame.grid(row=1, column=0)

    def run(self):
        self.window.mainloop()


class GameBoard:
    def __init__(self, master, board_row=4, board_col=4):
        # self.master = master
        self.frame = ttk.LabelFrame(master, text="Game Board")

        self.board = Board(self.frame, board_row=board_row, board_col=board_col)
        self.board.frame.grid(row=0, column=1)

        self.players = {}  # TODO: to GUI
        self.players["Player1"] = self.add_player_info(name="Player1", turn=True)  # TODO: fill name automatically
        self.players["Player1"].frame.grid(row=0, column=0)
        self.players["Player2"] = self.add_player_info(name="Player2", turn=False)
        self.players["Player2"].frame.grid(row=0, column=2)

    def add_player_info(self, name, turn):
        return PlayerInfo(master=self.frame, name=name, turn=turn)


class Board:
    def __init__(self, master, board_row, board_col):
        self.frame = ttk.LabelFrame(master)
        self.board_row = board_row
        self.board_col = board_col
        self.slots = {}
        self.pieces = {}
        self.init_board()
        self.init_piece()

    def init_board(self):  # TODO: labels are not given automatically
        for r in range(self.board_row):
            for c in range(self.board_col):
                self.slots[r, c, 0] = tk.Frame(self.frame, height=100, width=100)
                self.slots[r, c, 0].grid(row=r, column=c)
                self.slots[r, c, 0].pack_propagate(False)  # don't shrink

                slot_true = tk.PhotoImage(file=IMG_SLOT_TRUE)
                self.slots[r, c, 1] = tk.Button(self.slots[r, c, 0], state="disabled", bg="white", fg="white", justify="center", bd=0, image=slot_true)
                self.slots[r, c, 1].image = slot_true
                self.slots[r, c, 1].pack(fill="both", expand=True)

    def init_piece(self):
        piece0 = tk.PhotoImage(file=IMG_BLACK_PIECE)
        piece1 = tk.PhotoImage(file=IMG_WHITE_PIECE)
        self.pieces = [piece0, piece1]

        self.slots[0, math.ceil(self.board_col / 2.0) - 1, 1].config(image=self.pieces[0])  # black
        self.slots[self.board_row - 1, math.floor(self.board_col / 2.0), 1].config(image=self.pieces[1])  # white

    def move_piece(self, row, col):
        pass

class PlayerInfo:
    def __init__(self, master, name, turn=False):
        self.frame = ttk.LabelFrame(master, text=name)
        self.name = name

        self.turn = turn
        self.turn_info = ttk.Label(self.frame, text="")
        self.turn_info.grid(row=0, column=0)
        self.check_turn()

        self.remoteness_info = ttk.Label(self.frame, text="")
        self.remoteness_info.grid(row=1, column=0)

    def check_turn(self):  # TODO: two subturns
        if self.turn:
            self.turn_info.config(text="It's %s's turn." % self.name)
        else:
            self.turn_info.config(text="")

    def update_remoteness(self, value, remoteness):
        self.remoteness_info.config(text="%s should %s in %i." % (self.name, value, remoteness))


class Settings:
    def __init__(self, master):
        self.frame = ttk.LabelFrame(master, text="Settings")

        self.player1 = PlayerSettings(self.frame, "Player 1")
        self.player1.frame.grid(row=0, column=0)
        self.player2 = PlayerSettings(self.frame, "Player 2")
        self.player2.frame.grid(row=0, column=1)

        self.prediction = PredictSettings(self.frame)
        self.prediction.predict_button.grid(row=1, column=0)


class PlayerSettings:
    def __init__(self, master, name):
        self.frame = ttk.LabelFrame(master)
        self.name = ttk.Label(self.frame, text=name)
        self.name.grid(row=0, column=0)

        self.type = tk.IntVar()
        self.computer_button = tk.Radiobutton(self.frame, text="Computer", variable=self.type, value=0, command=self.choose)
        self.computer_button.grid(row=1, column=0)
        self.human_button = tk.Radiobutton(self.frame, text="Human", variable=self.type, value=1, command=self.choose)
        self.human_button.grid(row=2, column=0)    # TODO: Add rename Entry

        self.choice = None

    def choose(self):
        self.choice = self.type.get()

class PredictSettings:
    def __init__(self, master):
        self.predict_int = tk.IntVar()
        self.predict_button = tk.Checkbutton(master, text="Show values and remoteness", variable=self.predict_int)
        self.predict_button.deselect()


if __name__ == '__main__':
    game_gui = GameGUI()
    game_gui.game_board.players["Player1"].update_remoteness("WIN", 7)
    game_gui.run()  # TODO: change config when run

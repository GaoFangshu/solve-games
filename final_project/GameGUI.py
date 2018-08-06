import tkinter as tk
from tkinter import ttk, messagebox
import math
from final_project import Env
import argparse

parser = argparse.ArgumentParser(description='Game Player')
parser.add_argument('-g', '--game_name', choices=["Isolation"], default='Isolation', help='the game name, only "Isolation" for now')
parser.add_argument('-r', '--row', type=int, default=4, help='number of rows of gameboard')
parser.add_argument('-c', '--column', type=int, default=4, help='number of columns of gameboard')
parser.add_argument('-d', '--database_name', default=None,  help='filename of the database file')
args = parser.parse_args()

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
IMG_SLOT_VALID = "Leaf_valid.png"
IMG_PIECE_0 = "Frog_0.png"
IMG_PIECE_1 = "Frog_1.png"

class GameGUI:
    def __init__(self, board_row, board_col):
        self.env = Env.Env(game_name=args.game_name, board_row=board_row, board_col=board_col)

        self.window = tk.Tk()
        self.game_board = GameBoard(master=self.window, board_row=board_row, board_col=board_col, env=self.env)
        self.game_board.frame.grid(row=0, column=0)

        self.settings = Settings(master=self.window)
        self.settings.frame.grid(row=1, column=0)


        # self.game = Game.Game(board_row=board_row, board_col=board_row)

    def run(self):
        #self.p1_choice = self.settings.player1.type
        #self.p2_choice = self.settings.player2.type
        self.window.mainloop()

class GameBoard:
    def __init__(self, master, board_row, board_col, env):
        # self.master = master
        self.frame = ttk.LabelFrame(master, text="Game Board")

        self.board = Board(self.frame, board_row=board_row, board_col=board_col, env=env)
        self.board.frame.grid(row=0, column=1)

        self.players = {}  # TODO: to GUI
        self.players["Player1"] = self.add_player_info(name="Player1", turn=True)  # TODO: fill name automatically
        self.players["Player1"].frame.grid(row=0, column=0)
        self.players["Player2"] = self.add_player_info(name="Player2", turn=False)
        self.players["Player2"].frame.grid(row=0, column=2)

    def add_player_info(self, name, turn):
        return PlayerInfo(master=self.frame, name=name, turn=turn)


class Board:
    def __init__(self, master, board_row, board_col, env):
        self.env=env
        self.frame = ttk.LabelFrame(master)
        self.board_row = board_row
        self.board_col = board_col

        self.img_slot_true = tk.PhotoImage(file=IMG_SLOT_TRUE)
        self.img_slot_false = tk.PhotoImage(file=IMG_SLOT_FALSE)
        self.img_piece_0 = tk.PhotoImage(file=IMG_PIECE_0)
        self.img_piece_1 = tk.PhotoImage(file=IMG_PIECE_1)
        self.img_slot_valid = tk.PhotoImage(file=IMG_SLOT_VALID)

        self.dict_img = {0: self.img_slot_false,
                         1: self.img_slot_true,
                         2: self.img_piece_0,
                         3: self.img_piece_1}    # values to images

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

                self.slots[r, c, 1] = tk.Button(self.slots[r, c, 0], state="normal", bg="white", fg="white", justify="center", bd=0, image=self.img_slot_true)
                self.slots[r, c, 1].image = self.img_slot_true
                self.slots[r, c, 1].pack(fill="both", expand=True)

    def show_position(self, p):
        for r in p:
            for c in r:
                self.slots[r, c, 1].image = self.dict_img[c]

    def init_piece(self):
        row_piece0 = 0
        col_piece0 = math.ceil(self.board_col / 2.0) - 1
        row_piece1 = self.board_row - 1
        col_piece1 = math.floor(self.board_col / 2.0)

        self.slots[row_piece0, col_piece0, 1].config(image=self.img_piece_0,
                                                                     state="normal",
                                                                     command=lambda: self.show_valid_slot(row_piece0, col_piece0, piece=0))  # for player 1
        self.slots[row_piece1, col_piece1, 1].config(image=self.img_piece_1, state="normal",
                                                                     command=lambda: self.show_valid_slot(row_piece1, col_piece1, piece=1))  # for player 2

    def show_valid_slot(self, row, col, piece):
        if self.env.turn[0] == piece:
            current_position = self.env.curr_position
            valid_slots = self.env.game.gen_valid_index(row=row, col=col, p=current_position)
            for s in valid_slots:
                self.slots[s[0], s[1], 1].config(image=self.img_slot_valid, state="normal")
            # TODO: add next step (move)


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
    game_gui = GameGUI(board_row=args.row, board_col=args.column)
    game_gui.game_board.players["Player1"].update_remoteness("WIN", 7)
    game_gui.run()  # TODO: change config when run

import tkinter as tk
from tkinter import ttk

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
| +------------------Settings_------ ------------+ |
| | +------Player1------+ +------Player1------+ | |
| | | * Computer        | | * Computer        | | |
| | | * Human name      | | * Human name      | | |
| | +-------------------+ +-------------------+ | |
| | +---Prediction----------------------------+ | |
| | | * Show value and remoteness             | | |
| | +-----------------------------------------+ | |
| +---------------------------------------------+ |
+-------------------------------------------------+
"""

class GameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.game_board = GameBoard(master=self.window)    # TODO: control board_row and board_col
        self.game_board.frame.grid(row=0, column=0)

    def run(self):
        self.window.mainloop()

class GameBoard:
    def __init__(self, master, board_row=4, board_col=4):
        # self.master = master
        self.frame = ttk.LabelFrame(master, text="Game Board")

        self.board = Board(self.frame, board_row=board_row, board_col=board_col)
        self.board.frame.grid(row=0, column=1)

        self.players = {}    # TODO: to GUI
        self.players["Player1"] = self.add_player_info(name="Player1", turn=True)    # TODO: fill name automatically
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
        self.init_board()

    def init_board(self):    # TODO: labels are not given automatically
        for r in range(self.board_row):
            for c in range(self.board_col):
                slot = tk.Button(self.frame, state="disabled", bg="Grey", fg="white", justify="center", width=20, height=8, bd=1)
                slot.grid(row=r, column=c) #, sticky="N"
"""
    def row_helper(self):
        for row in range(1, 9):
            for column in range(1, 9):
                if row % 2 == 0:
                    bg = "Black"
                    if column % 2 == 0:
                        bg = "White"
                else:
                    bg = "White"
                    if column % 2 == 0:
                        bg = "Black"
                b1 = Button(self.labelframe, bg=bg, width=20, height=6, bd=8, relief=RAISED)
                b1.grid(row=row, column=column, sticky="N")
                b1.bind("<Button 1>", lambda e=row, i=row, k=column: self.movement(i, k))
"""

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


    def check_turn(self):    # TODO: two subturns
        if self.turn:
            self.turn_info.config(text="It's %s's turn." % self.name)
        else:
            self.turn_info.config(text="")

    def update_remoteness(self, value, remoteness):
        self.remoteness_info.config(text="%s should %s in %i." % (self.name, value, remoteness))


class Settings:
    def __init__(self, master ):
        pass

class PlayerSettings:
    def __init__(self):


class ValueSettings:

if __name__ == '__main__':
    game_gui = GameGUI()
    game_gui.game_board.players["Player1"].update_remoteness("WIN", 7)
    game_gui.run()    # TODO: change config when run

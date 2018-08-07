import tkinter as tk
from tkinter import ttk, messagebox
import math
from final_project import Env
import argparse

parser = argparse.ArgumentParser(description='Game Player')
parser.add_argument('-g', '--game_name', choices=["Isolation"], default='Isolation',
                    help='the game name, only "Isolation" for now')
parser.add_argument('-r', '--row', type=int, default=4, help='number of rows of gameboard')
parser.add_argument('-c', '--column', type=int, default=4, help='number of columns of gameboard')
parser.add_argument('-d', '--database_name', default=None, help='filename of the database file')
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

IMG_SLOT_TRUE = "img/Floor.png"
IMG_SLOT_FALSE = "img/Fire.png"
IMG_PIECE_0 = "img/FiremanRed.png"
IMG_PIECE_1 = "img/FiremanBlue.png"
IMG_MOVE_L = "img/ArrowL.png"
IMG_MOVE_R = "img/ArrowR.png"
IMG_MOVE_U = "img/ArrowU.png"
IMG_MOVE_D = "img/ArrowD.png"
IMG_MOVE_LU = "img/ArrowLU.png"
IMG_MOVE_LD = "img/ArrowLD.png"
IMG_MOVE_RU = "img/ArrowRU.png"
IMG_MOVE_RD = "img/ArrowRD.png"


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
        # self.p1_choice = self.settings.player1.type
        # self.p2_choice = self.settings.player2.type
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
        self.env = env
        self.frame = ttk.LabelFrame(master)
        self.board_row = board_row
        self.board_col = board_col

        [self.img_slot_true, self.img_slot_false, self.img_piece_0, self.img_piece_1, self.img_move_L, self.img_move_R,
         self.img_move_U, self.img_move_D, self.img_move_LU, self.img_move_LD, self.img_move_RU, self.img_move_RD] = [
            tk.PhotoImage(file=img) for img in
            [IMG_SLOT_TRUE, IMG_SLOT_FALSE, IMG_PIECE_0, IMG_PIECE_1, IMG_MOVE_L, IMG_MOVE_R, IMG_MOVE_U, IMG_MOVE_D,
             IMG_MOVE_LU, IMG_MOVE_LD, IMG_MOVE_RU, IMG_MOVE_RD]]

        self.dict_img = {0: self.img_slot_false,
                         1: self.img_slot_true,
                         2: self.img_piece_0,
                         3: self.img_piece_1}  # values to images

        self.slots = {}
        self.pieces = {}
        self.init_board()
        self.show_position(p=self.env.curr_position)

    def init_board(self):  # TODO: labels are not given automatically
        for r in range(self.board_row):
            for c in range(self.board_col):
                # 0 for Frames, 1 for Buttons
                self.slots[r, c, 0] = tk.Frame(self.frame, height=100, width=100)
                self.slots[r, c, 0].grid(row=r, column=c)
                self.slots[r, c, 0].pack_propagate(False)  # don't shrink

                self.slots[r, c, 1] = tk.Button(self.slots[r, c, 0], state="normal", bg="white", fg="white",
                                                justify="center", bd=1, image=self.img_slot_true)
                self.slots[r, c, 1].image = self.img_slot_true
                self.slots[r, c, 1].pack(fill="both", expand=True)

    def show_position(self, p):
        row = 0
        for r in p:
            col = 0
            for c in r:
                self.slots[row, col, 1].config(image=self.dict_img[c], command=lambda: None)
                col += 1
            row += 1

        row_piece0, col_piece0 = self.env.game.get_piece_index(piece=2, p=self.env.curr_position)
        row_piece1, col_piece1 = self.env.game.get_piece_index(piece=3, p=self.env.curr_position)

        if self.env.turn[0] == 0:  # player 1
            self.activate_slot(row_piece0, col_piece0)
        elif self.env.turn[0] == 1:  # player 2
            self.activate_slot(row_piece1, col_piece1)

    def activate_slot(self, row, col):
        if self.env.turn[1] == 0:  # activate slots to move
            valid_slots = self.env.game.gen_valid_index(row=row, col=col, p=self.env.curr_position)
            print(valid_slots)
            print(row, col)
            for s in valid_slots:
                print(s)
                self.slots[s[0], s[1], 1].config(command=lambda s=s: self.step(s[0], s[1]))
                if s[0] == row:
                    if s[1] + 1 == col:  # left
                        self.slots[s[0], s[1], 1].config(image=self.img_move_L)
                    elif s[1] - 1 == col:  # right
                        self.slots[s[0], s[1], 1].config(image=self.img_move_R)
                elif s[0] + 1 == row:
                    if s[1] + 1 == col:  # left up
                        self.slots[s[0], s[1], 1].config(image=self.img_move_LU)
                    elif s[1] - 1 == col:  # right up
                        self.slots[s[0], s[1], 1].config(image=self.img_move_RU)
                    elif s[1] == col:  # up
                        self.slots[s[0], s[1], 1].config(image=self.img_move_U)
                elif s[0] - 1 == row:
                    if s[1] + 1 == col:  # left down
                        self.slots[s[0], s[1], 1].config(image=self.img_move_LD)
                    elif s[1] - 1 == col:  # right down
                        self.slots[s[0], s[1], 1].config(image=self.img_move_RD)
                    elif s[1] == col:  # down
                        self.slots[s[0], s[1], 1].config(image=self.img_move_D)
        elif self.env.turn[1] == 1:  # activate slots to delete
            for r in range(self.board_row):
                for c in range(self.board_col):
                    if self.env.curr_position[r][c] == 1:
                        self.slots[r, c, 1].bind("Enter",
                                                 lambda r=r, c=c: self.slots[r, c, 1].config(image=self.img_slot_false))
                        self.slots[r, c, 1].config(command=lambda r=r, c=c: self.step(r, c))

    def step(self, row, col):  # do move or do delete
        print(self.env.curr_position)
        self.env.game.do_move(p=self.env.curr_position, m=[row, col], turn=self.env.turn)
        self.next_turn()
        print(row, col)
        print(self.env.curr_position)
        self.show_position(p=self.env.curr_position)
        # check winner
        if self.env.game.primitive(p=self.env.curr_position) == 2:
            messagebox.showinfo("Game Over", "Player 2 Wins!")
        elif self.env.game.primitive(p=self.env.curr_position) == 3:
            messagebox.showinfo("Game Over", "Player 1 Wins!")

    def next_turn(self):
        if self.env.turn[0] == 0 and self.env.turn[1] == 0:
            self.env.turn[1] = 1
        elif self.env.turn[0] == 0 and self.env.turn[1] == 1:
            self.env.turn[0] = 1
            self.env.turn[1] = 0
        elif self.env.turn[0] == 1 and self.env.turn[1] == 0:
            self.env.turn[1] = 1
        elif self.env.turn[0] == 1 and self.env.turn[1] == 1:
            self.env.turn[0] = 0
            self.env.turn[1] = 0


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
        self.computer_button = tk.Radiobutton(self.frame, text="Computer", variable=self.type, value=0,
                                              command=self.choose)
        self.computer_button.grid(row=1, column=0)
        self.human_button = tk.Radiobutton(self.frame, text="Human", variable=self.type, value=1, command=self.choose)
        self.human_button.grid(row=2, column=0)  # TODO: Add rename Entry

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

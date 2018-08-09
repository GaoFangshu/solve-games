import tkinter as tk
from tkinter import ttk, messagebox
import math
from final_project import Env
import argparse

parser = argparse.ArgumentParser(description='Game Player')
parser.add_argument('-g', '--game_name', choices=["Isolation"], default='Isolation',
                    help='the game name, only "Isolation" for now')
parser.add_argument('-r', '--row', type=int, default=2, help='number of rows of gameboard')
parser.add_argument('-c', '--column', type=int, default=2, help='number of columns of gameboard')
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
IMG_PIECE_0 = "img/Player1.png"
IMG_PIECE_1 = "img/Player2.png"
IMG_MOVE_L = "img/ArrowL.png"
IMG_MOVE_R = "img/ArrowR.png"
IMG_MOVE_U = "img/ArrowU.png"
IMG_MOVE_D = "img/ArrowD.png"
IMG_MOVE_LU = "img/ArrowLU.png"
IMG_MOVE_LD = "img/ArrowLD.png"
IMG_MOVE_RU = "img/ArrowRU.png"
IMG_MOVE_RD = "img/ArrowRD.png"
IMG_1_WIN = "img/Player1Win.png"
IMG_2_WIN = "img/Player2Win.png"
IMG_Ash = "img/Ash.png"
IMG_MINI_P1 = "img/MiniP1.png"
IMG_MINI_P2 = "img/MiniP2.png"


class GameGUI:
    def __init__(self, board_row, board_col):
        self.env = Env.Env(board_row=board_row, board_col=board_col)

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
        self.board_row = board_row
        self.board_col = board_col
        self.env = env

        self.board = Board(self.frame, board_row=self.board_row, board_col=self.board_col, env=self.env)
        self.board.frame.grid(row=0, column=0)

        self.players = {}  # TODO: to GUI
        self.player_info = self.add_player_info(name="Info", turn=True)  # TODO: fill name automatically
        self.player_info.frame.grid(row=1, column=0)

    def add_player_info(self, name, turn):
        return PlayerInfo(master=self.frame, name=name, turn=turn)

    '''
    def init_board(self):
        if self.board:
            self.board.frame.grid_forget()
        else:
            self.board = Board(self.frame, board_row=self.board_row, board_col=self.board_col, env=self.env)
            self.board.frame.grid(row=0, column=1)
    '''


class Board:
    def __init__(self, master, board_row, board_col, env):
        self.env = env
        self.frame = tk.LabelFrame(master, borderwidth=0, highlightthickness=0)
        self.board_row = board_row
        self.board_col = board_col

        [self.img_slot_true, self.img_slot_false, self.img_piece_0, self.img_piece_1, self.img_move_L, self.img_move_R,
         self.img_move_U, self.img_move_D, self.img_move_LU, self.img_move_LD, self.img_move_RU, self.img_move_RD,
         self.img_1_win, self.img_2_win] = [
            tk.PhotoImage(file=img) for img in
            [IMG_SLOT_TRUE, IMG_SLOT_FALSE, IMG_PIECE_0, IMG_PIECE_1, IMG_MOVE_L, IMG_MOVE_R, IMG_MOVE_U, IMG_MOVE_D,
             IMG_MOVE_LU, IMG_MOVE_LD, IMG_MOVE_RU, IMG_MOVE_RD, IMG_1_WIN, IMG_2_WIN]]

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
            self.game_over(msg="Player 2 Wins!", img=self.img_2_win)
        elif self.env.game.primitive(p=self.env.curr_position) == 3:
            self.game_over(msg="Player 1 Wins!", img=self.img_1_win)

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

    def game_over(self, msg, img):
        top = tk.Toplevel(self.frame)
        top.title = "Game Over"
        frame = tk.LabelFrame(top)
        frame.place(anchor='n')
        tk.Label(frame, image=img).grid()
        tk.Label(frame, text=msg).grid()
        b = tk.Button(top, text="Try again", command=lambda top=top: self.restart(top))
        b.place(anchor='s')

    def restart(self, top):
        top.destroy()
        self.env.restart()
        self.init_board()
        self.show_position(p=self.env.curr_position)


class PlayerInfo:
    def __init__(self, master, name, turn=False):
        self.frame = ttk.LabelFrame(master, text="Information")
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

        self.players = [0, 0]  # [player1, player2], 0 for computer, 1 for human
        self.names = ["Computer 1", "Computer 2"]

        self.player_frame = tk.LabelFrame(self.frame, text="Players")
        self.player_frame.grid(row=0, column=0)
        self.player1 = PlayerSettings(master=self.player_frame, img=IMG_MINI_P1)  # TODO: center
        self.player1.frame.grid(row=0, column=0)
        self.player2 = PlayerSettings(master=self.player_frame, img=IMG_MINI_P2)  # TODO: center
        self.player2.frame.grid(row=0, column=1)

        self.player_button = tk.Button(self.player_frame, command=self.change_player, text="ok")
        self.player_button.grid(row=1, column=0, columnspan=2)  # TODO: set width

        self.prediction = PredictSettings(self.frame)
        self.prediction.predict_button.grid(row=1, column=0)

    def change_player(self):
        i = 0
        for player_setting in [self.player1, self.player2]:
            if player_setting.type.get() == 0:  # computer
                self.players[i] = 0
                self.names[i] = "Computer " + str(i)
            elif player_setting.type.get() == 1:
                self.players[i] = 1
                if player_setting.name.get():
                    self.names[i] = player_setting.name.get()
                else:
                    self.names[i] = "Human " + str(i)
            i += 1
        print(self.players, self.names)


class PlayerSettings:
    def __init__(self, master, img):
        self.frame = tk.Frame(master, borderwidth=0, highlightthickness=0)
        self.title = tk.Frame(self.frame, borderwidth=0, highlightthickness=0)
        self.title.grid(row=0, column=0, rowspan=2, sticky='n')
        self.img_player = tk.PhotoImage(file=img)
        tk.Label(self.title, image=self.img_player).grid()

        self.type = tk.IntVar()
        self.computer_button = tk.Radiobutton(self.frame, text="Computer", variable=self.type, value=0,
                                              command=self.choose)
        self.computer_button.grid(row=0, column=1, sticky='w')
        self.human_button = tk.Radiobutton(self.frame, text="Human", variable=self.type, value=1, command=self.choose)
        self.human_button.grid(row=1, column=1, sticky='w')  # TODO: Set name

        self.name = tk.StringVar()
        self.name_entry = tk.Entry(self.frame, textvariable=self.name)  # TODO: state='disabled'
        self.name_entry.grid(row=1, column=2, sticky='w')
        tk.Label(self.frame, text="   ").grid(row=1, column=3)

    def choose(self):
        self.choice = self.type.get()


class PredictSettings:
    def __init__(self, master):
        self.predict_int = tk.IntVar()
        self.predict_button = tk.Checkbutton(master, text="Show values and remoteness", variable=self.predict_int)
        self.predict_button.deselect()
        self.predict_button.grid(sticky='w')


if __name__ == '__main__':
    game_gui = GameGUI(board_row=args.row, board_col=args.column)
    game_gui.game_board.player_info.update_remoteness("WIN", 7)
    game_gui.run()  # TODO: change config when run

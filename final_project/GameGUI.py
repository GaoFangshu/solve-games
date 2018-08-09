import tkinter as tk
from tkinter import ttk, messagebox, font
import math
import Env
from copy import deepcopy
from time import sleep

IMG_SLOT_TRUE = "img/Floor.png"
IMG_SLOT_FALSE = "img/Fire.png"
IMG_SLOT_RED = "img/RedFloor.png"
IMG_SLOT_GREEN = "img/GreenFloor.png"
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

IMG_MOVE_L_B = "img/BlueArrowL.png"
IMG_MOVE_R_B = "img/BlueArrowR.png"
IMG_MOVE_U_B = "img/BlueArrowU.png"
IMG_MOVE_D_B = "img/BlueArrowD.png"
IMG_MOVE_LU_B = "img/BlueArrowLU.png"
IMG_MOVE_LD_B = "img/BlueArrowLD.png"
IMG_MOVE_RU_B = "img/BlueArrowRU.png"
IMG_MOVE_RD_B = "img/BlueArrowRD.png"

IMG_MOVE_L_R = "img/RedArrowL.png"
IMG_MOVE_R_R = "img/RedArrowR.png"
IMG_MOVE_U_R = "img/RedArrowU.png"
IMG_MOVE_D_R = "img/RedArrowD.png"
IMG_MOVE_LU_R = "img/RedArrowLU.png"
IMG_MOVE_LD_R = "img/RedArrowLD.png"
IMG_MOVE_RU_R = "img/RedArrowRU.png"
IMG_MOVE_RD_R = "img/RedArrowRD.png"

IMG_MOVE_L_G = "img/GreenArrowL.png"
IMG_MOVE_R_G = "img/GreenArrowR.png"
IMG_MOVE_U_G = "img/GreenArrowU.png"
IMG_MOVE_D_G = "img/GreenArrowD.png"
IMG_MOVE_LU_G = "img/GreenArrowLU.png"
IMG_MOVE_LD_G = "img/GreenArrowLD.png"
IMG_MOVE_RU_G = "img/GreenArrowRU.png"
IMG_MOVE_RD_G = "img/GreenArrowRD.png"

IMG_1_WIN = "img/Player1Win.png"
IMG_2_WIN = "img/Player2Win.png"
IMG_Ash = "img/Ash.png"
IMG_MINI_P1 = "img/MiniP1.png"
IMG_MINI_P2 = "img/MiniP2.png"


class GameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.frame = ttk.LabelFrame(self.window, text="Settings")
        self.frame.grid(row=0, column=0)
        self.players = [0, 0]  # [player1, player2], 0 for human, 1 for computer
        self.names = ["Human 1", "Human 2"]

        self.size_frame = tk.LabelFrame(self.frame, borderwidth=0, highlightthickness=0)
        self.size_frame.grid(row=0, column=0, sticky='w', columnspan=2)  # TODO: set width
        self.size_setting = SizeSettings(master=self.size_frame)

        self.player_frame = tk.LabelFrame(self.frame, borderwidth=0, highlightthickness=0)
        self.player_frame.grid(row=1, column=0)
        self.player1 = PlayerSettings(master=self.player_frame, img=IMG_MINI_P1)  # TODO: center
        self.player1.frame.grid(row=0, column=0)
        self.player2 = PlayerSettings(master=self.player_frame, img=IMG_MINI_P2)  # TODO: center
        self.player2.frame.grid(row=0, column=1)

        self.predict_frame = tk.LabelFrame(self.frame, borderwidth=0, highlightthickness=0)
        self.predict_frame.grid(row=2, column=0, sticky='w')  # TODO: set width
        self.predict_setting = PredictSettings(self.predict_frame)
        self.predict_setting.predict_button.grid(row=0, column=0, sticky='w')

        self.player_button = tk.Button(self.frame, command=self.start, text="Fight!")
        self.player_button.grid(row=3, column=0)  # TODO: set width

        self.board_row = None
        self.board_col = None
        self.env = None
        self.players = [0, 0]  # [player1, player2], 0 for human, 1 for computer
        self.names = ["Human 1", "Human 2"]
        self.game_board = None

        self.window.mainloop()

    def start(self):
        # init environment
        self.board_row = int(self.size_setting.row.get())
        self.board_col = int(self.size_setting.row.get())
        self.env = Env.Env(board_row=self.board_row, board_col=self.board_col)

        # init players
        i = 0
        for player_setting in [self.player1, self.player2]:
            if player_setting.type.get() == 0:  # human
                self.players[i] = 0
                if player_setting.name.get():
                    self.names[i] = player_setting.name.get()
                else:
                    self.names[i] = "Human " + str(i + 1)
            elif player_setting.type.get() == 1:  # computer
                self.players[i] = 1
                self.names[i] = "Computer " + str(i + 1)
            i += 1
        self.env.players = self.players
        self.env.turn_to_player = {0:self.names[0], 1:self.names[1]}
        print(self.players, self.names)

        # init prediction
        self.env.prediction = self.predict_setting.predict_int.get()

        # init game_board
        self.game_board = None
        self.game_board = GameBoard(master=self.window, board_row=self.board_row, board_col=self.board_col, env=self.env)
        self.game_board.frame.grid(row=1, column=0)

class SizeSettings:
    def __init__(self, master):
        tk.Label(master, text="Board size: ").grid(row=0, column=0, sticky='w')

        self.row = tk.StringVar()
        self.row_entry = tk.Entry(master, textvariable=self.row, width=3)
        self.row_entry.grid(row=0, column=1, sticky='w')

        tk.Label(master, text="*").grid(row=0, column=2)

        self.col = tk.StringVar()
        self.col_entry = tk.Entry(master, textvariable=self.col, width=3)
        self.col_entry.grid(row=0, column=3, sticky='w')


class PlayerSettings:
    def __init__(self, master, img):
        self.frame = tk.Frame(master, borderwidth=0, highlightthickness=0)
        self.title = tk.Frame(self.frame, borderwidth=0, highlightthickness=0)
        self.title.grid(row=0, column=0, rowspan=2, sticky='n')
        self.img_player = tk.PhotoImage(file=img)
        tk.Label(self.title, image=self.img_player).grid()

        self.type = tk.IntVar()
        self.computer_button = tk.Radiobutton(self.frame, text="Human", variable=self.type, value=0,
                                              command=self.choose)
        self.computer_button.grid(row=0, column=1, sticky='w')
        self.human_button = tk.Radiobutton(self.frame, text="Computer", variable=self.type, value=1, command=self.choose)
        self.human_button.grid(row=1, column=1, sticky='w')  # TODO: Set name

        self.name = tk.StringVar()
        self.name_entry = tk.Entry(self.frame, textvariable=self.name)  # TODO: state='disabled'
        self.name_entry.grid(row=0, column=2, sticky='w')
        tk.Label(self.frame, text="   ").grid(row=1, column=3)

    def choose(self):
        self.choice = self.type.get()


class PredictSettings:
    def __init__(self, master):
        self.predict_int = tk.IntVar()
        self.predict_button = tk.Checkbutton(master, text="Show values and remoteness", variable=self.predict_int)
        self.predict_button.deselect()
        self.predict_button.grid(sticky='w')


class GameBoard:
    def __init__(self, master, board_row, board_col, env):
        # self.master = master
        self.frame = ttk.LabelFrame(master, text="Game Board")
        self.board_row = board_row
        self.board_col = board_col
        self.env = env

        self.player_info = PlayerInfo(master=self.frame)
        self.player_info.frame.grid(row=1, column=0)

        self.board = Board(self.frame, board_row=self.board_row, board_col=self.board_col, env=self.env, player_info=self.player_info)
        self.board.frame.grid(row=0, column=0)
        self.board.show_position(p=self.env.curr_position)
        self.board.show_next_position()


class Board:
    def __init__(self, master, board_row, board_col, env, player_info):
        self.env = env
        self.player_info = player_info

        self.frame = tk.LabelFrame(master, borderwidth=0, highlightthickness=0)
        self.board_row = board_row
        self.board_col = board_col

        [self.img_slot_true, self.img_slot_false, self.img_slot_red, self.img_slot_green,
         self.img_piece_0, self.img_piece_1, self.img_1_win, self.img_2_win,

         self.img_move_L, self.img_move_R, self.img_move_U, self.img_move_D, self.img_move_LU, self.img_move_LD,
         self.img_move_RU, self.img_move_RD,

         self.img_move_L_B, self.img_move_R_B, self.img_move_U_B, self.img_move_D_B, self.img_move_LU_B,
         self.img_move_LD_B, self.img_move_RU_B, self.img_move_RD_B,

         self.img_move_L_R, self.img_move_R_R, self.img_move_U_R, self.img_move_D_R, self.img_move_LU_R,
         self.img_move_LD_R, self.img_move_RU_R, self.img_move_RD_R,

         self.img_move_L_G, self.img_move_R_G, self.img_move_U_G, self.img_move_D_G, self.img_move_LU_G,
         self.img_move_LD_G, self.img_move_RU_G, self.img_move_RD_G,

         ] = [
            tk.PhotoImage(file=img) for img in
            [IMG_SLOT_TRUE, IMG_SLOT_FALSE, IMG_SLOT_RED, IMG_SLOT_GREEN,
             IMG_PIECE_0, IMG_PIECE_1, IMG_1_WIN, IMG_2_WIN,

             IMG_MOVE_L, IMG_MOVE_R, IMG_MOVE_U, IMG_MOVE_D, IMG_MOVE_LU, IMG_MOVE_LD, IMG_MOVE_RU, IMG_MOVE_RD,

             IMG_MOVE_L_B, IMG_MOVE_R_B, IMG_MOVE_U_B, IMG_MOVE_D_B, IMG_MOVE_LU_B, IMG_MOVE_LD_B, IMG_MOVE_RU_B,
             IMG_MOVE_RD_B,

             IMG_MOVE_L_R, IMG_MOVE_R_R, IMG_MOVE_U_R, IMG_MOVE_D_R, IMG_MOVE_LU_R, IMG_MOVE_LD_R, IMG_MOVE_RU_R,
             IMG_MOVE_RD_R,

             IMG_MOVE_L_G, IMG_MOVE_R_G, IMG_MOVE_U_G, IMG_MOVE_D_G, IMG_MOVE_LU_G, IMG_MOVE_LD_G, IMG_MOVE_RU_G,
             IMG_MOVE_RD_G
             ]]

        self.value_to_img = {0: self.img_slot_false,
                             1: self.img_slot_true,
                             2: self.img_piece_0,
                             3: self.img_piece_1}  # values to images

        self.color_to_img = {"Red": [self.img_move_L_R, self.img_move_R_R, self.img_move_U_R, self.img_move_D_R,
                                     self.img_move_LU_R, self.img_move_LD_R, self.img_move_RU_R, self.img_move_RD_R],
                             "Green": [self.img_move_L_G, self.img_move_R_G, self.img_move_U_G, self.img_move_D_G,
                                       self.img_move_LU_G, self.img_move_LD_G, self.img_move_RU_G, self.img_move_RD_G]}

        self.slots = {}
        self.pieces = {}
        self.init_board()

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

                self.slots[row, col, 1].config(image=self.value_to_img[c], compound=tk.CENTER)
                self.slots[row, col, 1].config(command = lambda: None)
                col += 1
            row += 1

    def show_next_position(self):
        row_piece0, col_piece0 = self.env.game.get_piece_index(piece=2, p=self.env.curr_position)
        row_piece1, col_piece1 = self.env.game.get_piece_index(piece=3, p=self.env.curr_position)

        if self.env.turn[0] == 0:  # player 1
            self.activate_slot(row_piece0, col_piece0)
        elif self.env.turn[0] == 1:  # player 2
            self.activate_slot(row_piece1, col_piece1)

    def activate_slot(self, row, col):
        FONT = font.Font(family='Helvetica', size=24, weight='bold')
        if self.env.turn[1] == 0:  # activate slots to move
            valid_slots = self.env.game.gen_valid_move_index(row=row, col=col, p=self.env.curr_position)

            if self.env.prediction:
                for r in range(self.board_row):
                    for c in range(self.board_col):
                        self.slots[r, c, 1].config(text="", font=FONT)
                self.env.predict(curr_p=self.env.curr_position, turn=self.env.turn, valid_moves=valid_slots)
                for s in valid_slots:  # {slot: value, remoteness}
                    self.slots[s[0], s[1], 1].config(command=lambda s=s: self.step(s[0], s[1]))  # TODO: image disappear
                    value, remoteness = self.env.predict_info["move"][str(s)]
                    self.slots[s[0], s[1], 1].config(text=remoteness, font=FONT)
                    if value == "WIN":  # lead to WIN position, bad choice
                        img_move = self.color_to_img["Red"]
                    elif value == "LOSE":  # lead to LOSE position, good choice
                        img_move = self.color_to_img["Green"]
                    if s[0] == row:
                        if s[1] + 1 == col:  # left
                            self.slots[s[0], s[1], 1].config(image=img_move[0])
                        elif s[1] - 1 == col:  # right
                            self.slots[s[0], s[1], 1].config(image=img_move[1])
                    elif s[0] + 1 == row:
                        if s[1] + 1 == col:  # left up
                            self.slots[s[0], s[1], 1].config(image=img_move[4])
                        elif s[1] - 1 == col:  # right up
                            self.slots[s[0], s[1], 1].config(image=img_move[6])
                        elif s[1] == col:  # up
                            self.slots[s[0], s[1], 1].config(image=img_move[2])
                    elif s[0] - 1 == row:
                        if s[1] + 1 == col:  # left down
                            self.slots[s[0], s[1], 1].config(image=img_move[5])
                        elif s[1] - 1 == col:  # right down
                            self.slots[s[0], s[1], 1].config(image=img_move[7])
                        elif s[1] == col:  # down
                            self.slots[s[0], s[1], 1].config(image=img_move[3])
                    # TODO: add remoteness
            else:
                value, remoteness = self.env.database.lookup(p=self.env.curr_position)
                self.player_info.update_remoteness(name=self.env.turn_to_player[self.env.turn[0]], value=value, remoteness=remoteness)
                for s in valid_slots:
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
            if self.env.prediction:
                deletes_info = self.env.predict_info["delete"][str(self.env.last_move)]
                deletes_info_zip = list(zip(*deletes_info))  # [([d_row, d_col], value, remoteness), ...]
                delete_list = [str(info[0]) for info in deletes_info_zip]

            for r in range(self.board_row):
                for c in range(self.board_col):
                    self.slots[r, c, 1].config(text="", font=FONT)
                    if self.env.curr_position[r][c] == 1:
                        if self.env.prediction:
                            value = deletes_info[1][delete_list.index(str([r, c]))]
                            remoteness = deletes_info[2][delete_list.index(str([r, c]))]
                            self.slots[r, c, 1].config(text=remoteness, font=FONT)
                            if value == "WIN":  # lead to WIN position, bad choice
                                self.slots[r, c, 1].config(image=self.img_slot_red)
                                self.slots[r, c, 1].bind("Enter",
                                                         lambda r=r, c=c: self.slots[r, c, 1].config(
                                                             image=self.img_slot_red))
                            elif value == "LOSE":  # lead to LOSE position, good choice
                                self.slots[r, c, 1].config(image=self.img_slot_green)
                                self.slots[r, c, 1].bind("Enter",
                                                         lambda r=r, c=c: self.slots[r, c, 1].config(
                                                             image=self.img_slot_green))
                        else:
                            self.slots[r, c, 1].bind("Enter",
                                                     lambda r=r, c=c: self.slots[r, c, 1].config(image=self.img_slot_false))
                        self.slots[r, c, 1].config(command=lambda r=r, c=c: self.step(r, c))

    def step(self, row, col):  # do move or do delete
        self.env.last_move = [row, col]
        self.env.curr_position = self.env.game.do_move(p=self.env.curr_position, m=[row, col], turn=self.env.turn)
        self.env.turn = self.env.next_turn(self.env.turn)
        self.show_position(p=self.env.curr_position)
        self.show_next_position()
        self.check_winner()

        if self.env.players[self.env.turn[0]] == 1:  # if it is computer in this turn
            curr_p = deepcopy(self.env.curr_position)
            final_position, final_value, final_remoteness = self.env.gen_best_position(curr_p=curr_p, turn=self.env.turn)
            self.env.curr_position = final_position
            self.env.turn = self.env.next_turn(self.env.turn)
            self.env.turn = self.env.next_turn(self.env.turn)
            self.show_position(p=self.env.curr_position)
            self.show_next_position()
            self.check_winner()

    def check_winner(self):
        name = self.env.turn_to_player[self.env.turn[0]]
        if self.env.game.primitive(p=self.env.curr_position) == 2:
            self.player_info.game_over(msg="%s Wins!" % name, img=self.img_2_win)
        elif self.env.game.primitive(p=self.env.curr_position) == 3:
            self.player_info.game_over(msg="%s Wins!" % name, img=self.img_1_win)

    def restart(self, top):
        top.destroy()
        self.env.restart()
        self.init_board()
        self.show_position(p=self.env.curr_position)
        self.show_next_position()


class PlayerInfo:
    def __init__(self, master):
        self.frame = ttk.LabelFrame(master, text="Information")

        self.remoteness_info = ttk.Label(self.frame, text="")
        self.remoteness_info.grid(row=0, column=0)

    def update_remoteness(self, name, value, remoteness):
        self.remoteness_info.config(text="%s should %s in %i." % (name, value, remoteness))

    def game_over(self, msg, img):
        self.remoteness_info.config(text="Game Over")
        ttk.Label(self.frame, image=img).grid(row=1, column=0)
        ttk.Label(self.frame, text=msg).grid(row=2, column=0)


if __name__ == '__main__':
    game_gui = GameGUI()

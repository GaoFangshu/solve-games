import math
from copy import deepcopy

class Game:
    def __init__(self, board_row, board_col):
        self.board_row = board_row
        self.board_col = board_col

        # position: 0 for no slot, 1 for have slot, 2 for piece of player 1, 3 for piece of player 2
        self.init_position = [[1 for i in range(self.board_col)] for j in range(self.board_row)]
        self.init_position[0][math.ceil(self.board_col / 2.0) - 1] = 2  # player 1
        self.init_position[self.board_row - 1][math.floor(self.board_col / 2.0)] = 3  # player 2

        self.dict_turn = {0: 2, 1: 3}  # 2 for player 1, 3 for player 2

    def do_move(self, p, m, turn):
        # m = [row, col] chosen
        p_copy = deepcopy(p)
        piece_row, piece_col = self.get_piece_index(piece=self.dict_turn[turn[0]], p=p_copy)
        # TODO: is it safe?
        if turn[1] == 0:  # move piece
            if m in self.gen_valid_move_index(row=piece_row, col=piece_col, p=p_copy):
                p_copy[piece_row][piece_col] = 1
                p_copy[m[0]][m[1]] = self.dict_turn[turn[0]]
        elif turn[1] == 1:  # delete slot
            p_copy[m[0]][m[1]] = 0
        return p_copy

    def gen_move(self, p, turn):  # TODO: split gen_delete?
        # turn is in [0, 0] player 1 to move
        #            [0, 1] player 1 to delete one slot
        #            [1, 0] player 2 to move
        #            [1, 1] player 2 to delete one slot
        if turn[1] == 0:
            piece_row, piece_col = self.get_piece_index(piece=self.dict_turn[turn[0]], p=p)
            return self.gen_valid_move_index(row=piece_row, col=piece_col, p=p)
        elif turn[1] == 1:
            return self.gen_valid_delete_index(p=p)

    def primitive(self, p, turn):
        is_primitive, valid0, valid1 = self.is_primitive(p)
        if is_primitive:
            if (len(valid0) == 0) and (len(valid1) == 0):
                if turn[0] == 0:
                    print("player 1 LOSE")
                    return 2
                elif turn[0] == 1:
                    print("player 2 LOSE")
                    return 3
            elif len(valid0) == 0:
                print("player 1 LOSE")
                return 2
            elif len(valid1) == 0:
                print("player 2 LOSE")
                return 3
        else:
            print("This position is not primitive.")

    def is_primitive(self, p):
        piece_row0, piece_col0 = self.get_piece_index(piece=2, p=p)
        piece_row1, piece_col1 = self.get_piece_index(piece=3, p=p)
        valid0 = self.gen_valid_move_index(row=piece_row0, col=piece_col0, p=p)
        valid1 = self.gen_valid_move_index(row=piece_row1, col=piece_col1, p=p)
        return len(valid0) == 0 or len(valid1) == 0, valid0, valid1

    def print_current_position(self, p):
        print("\nCurrent position: %i" % p)

    def print_possible_move(self, p, turn):
        move_list = self.gen_move(p=p, turn=turn)
        print("your possible moves are", end=" ")
        print(move_list)

    def get_piece_index(self, piece, p):
        # piece=2 for player 1, piece=3 for player 2
        row_piece = [row for row in p if piece in row][0]
        return p.index(row_piece), row_piece.index(piece)

    def gen_valid_move_index(self, row, col, p):
        valid_index = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if 0 <= row + r <= self.board_row - 1 and 0 <= col + c <= self.board_col - 1 and p[row + r][
                            col + c] == 1:
                    valid_index.append([row + r, col + c])
        return valid_index

    def gen_valid_delete_index(self, p):
        valid_index = []
        for r in range(self.board_row):
            for c in range(self.board_col):
                if p[r][c] == 1:
                    valid_index.append([r, c])
        return valid_index


if __name__ == '__main__':
    # You can change the parameters in the following
    BOARD_ROW = 4
    BOARD_COL = 4

    game = Game(board_row=BOARD_ROW, board_col=BOARD_COL)
    print(game.init_position)
    game.print_possible_move(p=game.init_position, turn=[0, 0])
    game.print_possible_move(p=game.init_position, turn=[1, 0])

    from copy import deepcopy

    print(game.do_move(p=deepcopy(game.init_position), m=[0, 1], turn=[0, 0]))
    print(game.do_move(p=deepcopy(game.init_position), m=[0, 0], turn=[0, 0]))
    print(game.do_move(p=deepcopy(game.init_position), m=[0, 1], turn=[0, 1]))

    game.is_primitive(p=game.init_position)
    game.primitive(p=game.init_position)

    position = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 3, 0, 0]]
    game.primitive(p=position)

    position = [[1, 1, 1, 1], [2, 0, 0, 1], [0, 0, 0, 1], [3, 1, 1, 1]]
    print(game.gen_move(p=position, turn=[1,1]))
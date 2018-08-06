import math

# You can change the parameters in the following
BOARD_ROW = 4
BOARD_COL = 5
START_PLAYER = 0

class GAME:
    def __init__(self, board_row=BOARD_ROW, board_col=BOARD_COL, start_player=START_PLAYER):
        self.board_row = board_row
        self.board_col = board_col

        # position: 0 for no slot, 1 for have slot, 2 for piece of player 1, 3 for piece of player 2
        self.init_position = [[1 for i in range(self.board_col)] for j in range(self.board_row)]
        self.init_position[0][math.ceil(self.board_col / 2.0) - 1] = 2  # player 1
        self.init_position[self.board_row - 1][math.floor(self.board_col / 2.0)] = 3  # player 2

        self.start_player = start_player

        self.dict_turn = {0: 2, 1: 3}  # 2 for player 1, 3 for player 2

    def do_move(self, p, m, turn):
        # m = [row, col] chosen
        piece_row, piece_col = self.get_piece_index(piece=self.dict_turn[turn[0]], p=p)

        if m in self.gen_valid_index(row=piece_row, col=piece_col, p=p):
            if turn[1] == 0:    # move piece
                p[piece_row][piece_col] = 1
                p[m[0]][m[1]] = self.dict_turn[turn[0]]
            elif turn[1] == 1:    # remove slot
                p[m[0]][m[1]] = 0
            return p
        else:
            print("The move is invalid.")

    def gen_move(self, p, turn):
        # turn is in [0, 0] player 1 to move
        #            [0, 1] player 1 to remove one slot
        #            [1, 0] player 2 to move
        #            [1, 1] player 2 to remove one slot
        piece_row, piece_col = self.get_piece_index(piece=self.dict_turn[turn[0]], p=p)
        return self.gen_valid_index(row=piece_row, col=piece_col, p=p)

    def primitive(self, p):
        if self.is_primitive(p):
            return "LOSE"
        else:
            print("This position is not primitive.")

    def is_primitive(self, p, turn):
        return len(self.gen_move(p, turn)) == 0

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

    def gen_valid_index(self, row, col, p):
        valid_index = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if 0 <= row + r <= self.board_row - 1 and 0 <= col + c <= self.board_col - 1 and p[row + r][col + c] == 1:
                    valid_index.append([row + r, col + c])
        return valid_index


if __name__ == '__main__':
    game = GAME()
    print(game.init_position)
    game.print_possible_move(p=game.init_position, turn=[0, 0])
    game.print_possible_move(p=game.init_position, turn=[1, 0])

    from copy import deepcopy
    print(game.do_move(p=deepcopy(game.init_position), m=[0, 1], turn=[0, 0]))
    print(game.do_move(p=deepcopy(game.init_position), m=[0, 0], turn=[0, 0]))
    print(game.do_move(p=deepcopy(game.init_position), m=[0, 1], turn=[0, 1]))
'''
TODO: fill the game discription and the rule.
Game:
    pass

Rule:
    pass
'''
import copy

class OddOrEven:
    class Position:
        def __init__(self, num=(0, 0), turn=0):
            self.num = list(num)
            self.turn = turn
        # use hash as the key of the dict
        def __hash__(self):
            return int(self.turn * 1000000 + self.num[0] * 1000 + self.num[1])

        def __getitem__(self, item):
            return self.num[item]

        # Very necessary!!!
        # https://blog.csdn.net/lnotime/article/details/81192207
        def __eq__(self, other):
            return self.__hash__() == other.__hash__()

    def __init__(self, init_position=(0, 0), n=15, max_move=3, start_player=0):
        self.init_position = self.Position(list(init_position), start_player)
        self.n = n
        self.max_move = max_move
        self.start_player = start_player
        self.n_player = 2

    def do_move(self, position, m):
        new_position = copy.deepcopy(position)
        new_position.num[position.turn] += m
        new_position.turn ^= 1
        return new_position

    def gen_move(self, position):
        return range(1, min(self.max_move, self.n - sum(position.num))+1)

    def primitive(self, position):
        if self.is_primitive(position):
            if position.num[position.turn] % 2 == 0:
                return "WIN"
            else:
                return "LOSE"
        else:
            print("This position is not primitive.")

    def is_primitive(self, position):
        return self.n == sum(position.num)

    def print_current_position(self, curr_position):
        print("\nCurrent position: (%i, %i)" % (curr_position[0], curr_position[1]))
        # print("turn is " + str(curr_position.turn))

    def print_possible_move(self, curr_position):
        move_list = self.gen_move(curr_position)
        print("your possible moves are", end=" ")
        print(move_list)

'''
One example
What's your name: lijiawei
The players are:
lijiawei computer

Current position: (0, 0)
it's lijiawei's turn.
At current position, lijiawei will WIN in 8.
Please give an available move: 3

Current position: (3, 0)
it's computer's turn.
At current position, computer will LOSE in 7.
Then computer moves 1.

Current position: (3, 1)
it's lijiawei's turn.
At current position, lijiawei will WIN in 6.
Please give an available move: 2

Current position: (5, 1)
it's computer's turn.
At current position, computer will WIN in 6.
Then computer moves 1.

Current position: (5, 2)
it's lijiawei's turn.
At current position, lijiawei will LOSE in 5.
Please give an available move: 1

Current position: (6, 2)
it's computer's turn.
At current position, computer will WIN in 4.
Then computer moves 3.

Current position: (6, 5)
it's lijiawei's turn.
At current position, lijiawei will LOSE in 3.
Please give an available move: 1

Current position: (7, 5)
it's computer's turn.
At current position, computer will WIN in 1.
Then computer moves 3.

Current position: (7, 8)
At current position, computer WINs.
Game over

'''
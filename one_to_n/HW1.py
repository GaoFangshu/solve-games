# -*- coding: utf-8 -*-

"""
Python 3.5.2

Game:
      One to N

Rule:
      There are N+1 slots (from 0 to N), and a piece is in slot 0. Each player can move the piece 1 to K slots ahead,
    the player who reaches the slot N is winner.
"""


class OneToN:
    def __init__(self, init_position=0, n_position=10, max_move=2):
        self.curr_position = init_position
        self.n_position = n_position
        self.max_move = max_move

    def do_move(self, m):
        self.curr_position += m

    def gen_move(self, p):
        return range(1, min(self.max_move + 1, self.n_position - p + 1))

    def primitive(self, p):
        if self.is_primitive(p):
            return "LOSE"
        else:
            print("This position is not primitive.")

    def is_primitive(self, p):
        return p == self.n_position


class Solver:
    def __init__(self):
        pass

    def solve(self, p, game):
        if game.is_primitive(p):
            return p, game.primitive(p)
        else:
            children = [p + m for m in game.gen_move(p)]  # positions of p's children
            values = [self.solve(child, game)[1] for child in children]
            if all(value == "WIN" for value in values):  # all children are WIN
                return p, "LOSE",
            elif "LOSE" in values:  # there exists at least 1 LOSE
                return p, "WIN"

if __name__ == '__main__':
    """
    An example of one-to-ten game, N=10, K=2:
        
    Current position: 0
    At current position, you will WIN. (If each player moves perfectly.)
    >>> Please give an available move: 1
    
    Current position: 1
    At current position, you will LOSE. (If each player moves perfectly.)
    >>> Please give an available move: two
    >>> Please give an available move: 
    >>> Please give an available move: 1
    
    Current position: 2
    At current position, you will WIN. (If each player moves perfectly.)
    >>> Please give an available move: 2
    
    Current position: 4
    At current position, you will LOSE. (If each player moves perfectly.)
    >>> Please give an available move: 1
    
    Current position: 5
    At current position, you will WIN. (If each player moves perfectly.)
    >>> Please give an available move: 2
    
    Current position: 7
    At current position, you will LOSE. (If each player moves perfectly.)
    >>> Please give an available move: 1
    
    Current position: 8
    At current position, you will WIN. (If each player moves perfectly.)
    >>> Please give an available move: 2
    
    Current position: 10
    At current position, you LOSE.
    Game over
    """

    game = OneToN(init_position=0, n_position=10, max_move=2)

    solver = Solver()

    for i in range(game.n_position + 1): print(solver.solve(i, game))    # show the value of each position

    while not game.is_primitive(game.curr_position):
        print("\nCurrent position: %i" % game.curr_position)
        print("At current position, you will %s. (If each player moves perfectly.)" %
              solver.solve(game.curr_position, game)[1])
        while True:
            try:
                m = int(input('Please give an available move: '))
            except:
                m = 0
            if m in game.gen_move(game.curr_position):
                break
        game.do_move(m)

    print("\nCurrent position: %i" % game.curr_position)
    print("At current position, you %s." % game.primitive(game.curr_position))
    print("Game over")

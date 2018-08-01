# -*- coding: utf-8 -*-

"""
It's really difficult to calculate the number of positions with 4-connected.
So I only care about the gameboard satisfied gravity, i.e. no pieces hang in the air.
There are 7 columns, each column's height can be 0-6,
so there are 7^7 = 823543 different valid "outlines" of the gameboard, if we don't consider the color the pieces.
For each type of outline, we can color them, if a outline has x pieces, then there's at most has C(x, x/2) different ways to color it.
So the following code will enumerate all 7^7 outlines, and sum all the possible positions.

This code can run in 5s, and the final result is 70728639995483, about 15.6 times the exact number.


fac=[]
# initialize the factorial to speed up the calculation of combinatorial number
def init_fac():
    fac.append(1)
    for i in range(1, 43):
        fac.append(fac[i-1]*i)

def C(n, m):
    return fac[n]//(fac[m]*fac[n-m])


init_fac()
cnt = 0
# mask is a number in base 7, represent an possible outline
for mask in range(7 ** 7):
    pieces_num = 0
    tmp = mask
    while tmp > 0:
        pieces_num += tmp % 7
        tmp //= 7
    cnt += C(pieces_num, pieces_num//2)
print("The upper bound is " + str(cnt))

"""

"""
Python 3.5.2

Game:
      One to N (with players and database)

Rule:
      There are N+1 slots (from 0 to N), and a piece is in slot 0. Each player can move the piece 1 to K slots ahead,
    the player who reaches the slot N is winner.
"""

import bisect


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
            return p, game.primitive(p), 0
        else:
            children = [p + m for m in game.gen_move(p)]  # positions of p's children
            child_info = [self.solve(child, game) for child in children]
            values = [child[1] for child in child_info]
            remoteness = [child[2] for child in child_info]
            if all(value == "WIN" for value in values):  # all children are WIN
                return p, "LOSE", 1 + max(remoteness)
            elif "LOSE" in values:  # there exists at least 1 LOSE
                remoteness_lose = [child[2] for child in child_info if child[1] == "LOSE"]
                return p, "WIN", 1 + min(remoteness_lose)


class Database:
    def __init__(self, game, solver):
        self.data = []
        for i in range(game.n_position + 1):
            self.add_data(p=i, game=game, solver=solver)
        self.data.sort()

    def add_data(self, p, game, solver):
        position, value, remoteness = solver.solve(p, game)
        self.data.append((position, value, remoteness))


class Player:
    def __init__(self, is_human, database):
        self.is_human = is_human
        if not is_human:
            self.goal_position = [data[0] for data in database.data if data[1] == "LOSE"]
            self.position = [data[0] for data in database.data]  # position list
            self.remoteness = [data[2] for data in database.data]  # remoteness list

    def do_player_move(self, main_env):
        position, value, remoteness = main_env.database.data[main_env.game.curr_position]
        print("At current position, %s will %s in %i." % (main_env.players[main_env.turn][0], value, remoteness))
        if self.is_human:
            while True:
                try:
                    m = int(input('Please give an available move: '))
                except:
                    m = 0
                if m in main_env.game.gen_move(main_env.game.curr_position):
                    break
        else:
            m = main_env.players[main_env.turn][1].gen_best_move(main_env.game.curr_position)
            print("Then computer moves %i." % m)
        main_env.game.do_move(m)

    def gen_best_move(self, p):
        if p in self.goal_position:
            return 1  # TODO: gen_slowest_move(self, p, main_env)
        else:
            return self.goal_position[bisect.bisect(self.goal_position, p)] - p


class MainEnv:
    def __init__(self, game_name):
        self.game = None
        self.players = []
        self.n_player = 0
        self.turn = 0
        self.database = None
        self.create_game(game_name)

    def create_game(self, game_name):
        if game_name == "OneToN":
            self.game = OneToN(init_position=0, n_position=10, max_move=2)
            self.database = Database(game=self.game, solver=Solver())
        else:
            print("Please start a game.")

    def add_player(self, is_human):
        if is_human:
            name = input('What\'s your name: ')
        else:
            name = "computer"
        self.players.append([name, Player(is_human=is_human, database=self.database)])

    def start(self):
        self.n_player = len(self.players)


if __name__ == '__main__':
    """
    Two examples of one-to-ten game, N=10, K=2:

    Example 1 (Human vs. Computer):
    
        >>> What's your name: Fangshu
        The players are: 
        Fangshu
        computer
        
        Current position: 0, and it's Fangshu's turn.
        At current position, Fangshu will WIN in 7.
        >>> Please give an available move: 1
        
        Current position: 1, and it's computer's turn.
        At current position, computer will LOSE in 6.
        Then computer moves 1.
        
        Current position: 2, and it's Fangshu's turn.
        At current position, Fangshu will WIN in 5.
        >>> Please give an available move: 1
        
        Current position: 3, and it's computer's turn.
        At current position, computer will WIN in 5.
        Then computer moves 1.
        
        Current position: 4, and it's Fangshu's turn.
        At current position, Fangshu will LOSE in 4.
        >>> Please give an available move: 2
        
        Current position: 6, and it's computer's turn.
        At current position, computer will WIN in 3.
        Then computer moves 1.
        
        Current position: 7, and it's Fangshu's turn.
        At current position, Fangshu will LOSE in 2.
        >>> Please give an available move: 2
        
        Current position: 9, and it's computer's turn.
        At current position, computer will WIN in 1.
        Then computer moves 1.
        
        Current position: 10
        At current position, computer WINs.
        Game over

    Example 2 (Human vs. Human):
    
        >>> What's your name: Fangshu
        >>> What's your name: Jiawei
        The players are: 
        Fangshu
        Jiawei
        
        Current position: 0, and it's Fangshu's turn.
        At current position, Fangshu will WIN in 7.
        >>> Please give an available move: 1
        
        Current position: 1, and it's Jiawei's turn.
        At current position, Jiawei will LOSE in 6.
        >>> Please give an available move: 1
        
        Current position: 2, and it's Fangshu's turn.
        At current position, Fangshu will WIN in 5.
        >>> Please give an available move: 2
        
        Current position: 4, and it's Jiawei's turn.
        At current position, Jiawei will LOSE in 4.
        >>> Please give an available move: 1
        
        Current position: 5, and it's Fangshu's turn.
        At current position, Fangshu will WIN in 3.
        >>> Please give an available move: 1
        
        Current position: 6, and it's Jiawei's turn.
        At current position, Jiawei will WIN in 3.
        >>> Please give an available move: 1
        
        Current position: 7, and it's Fangshu's turn.
        At current position, Fangshu will LOSE in 2.
        >>> Please give an available move: 2
        
        Current position: 9, and it's Jiawei's turn.
        At current position, Jiawei will WIN in 1.
        >>> Please give an available move: 1
        
        Current position: 10
        At current position, Jiawei WINs.
        Game over
    """


    def start(main_env):
        main_env.start()
        print("The players are: ")
        for i in range(len(main_env.players)):
            print(main_env.players[i][0])
        while not main_env.game.is_primitive(main_env.game.curr_position):
            if main_env.turn < main_env.n_player:
                print("\nCurrent position: %i, and it's %s's turn." % (
                    main_env.game.curr_position, main_env.players[main_env.turn][0]))
                main_env.players[main_env.turn][1].do_player_move(main_env=main_env)
                if not main_env.game.is_primitive(main_env.game.curr_position):
                    main_env.turn += 1
            else:
                main_env.turn = 0

        print("\nCurrent position: %i" % main_env.game.curr_position)
        print("At current position, %s WINs." % main_env.players[main_env.turn][0])
        print("Game over\n")


    # Start a game with one human and one computer (human first).
    main_env = MainEnv(game_name="OneToN")
    main_env.add_player(is_human=True)  # Add player
    main_env.add_player(is_human=False)  # Add computer
    start(main_env=main_env)

    # Start another game with two humans.
    main_env = MainEnv(game_name="OneToN")
    main_env.add_player(is_human=True)  # Add player 1
    main_env.add_player(is_human=True)  # Add player 2
    start(main_env=main_env)

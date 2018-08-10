'''
Game:
      One to N (with players and database)

Rule:
      There are N+1 slots (from 0 to N), and a piece is in slot 0. Each player can move the piece 1 to K slots ahead,
    the player who reaches the slot N is winner.


This file contain the basic rule of the game, and static information.
Dynamic information of the game are kept in Player.py
'''
# You can change the parameters in the following
INIT_POSITION = 0
N_POSITION = 10
MAX_MOVE = 2
START_PLAYER = 0

class OneToN:
    def __init__(self, init_position=INIT_POSITION, n_position=N_POSITION, max_move=MAX_MOVE, start_player=START_PLAYER):
        self.init_position = init_position
        self.n_position = n_position
        self.max_move = max_move
        self.start_player = start_player

    def do_move(self, curr_position, m):
        return curr_position + m

    def gen_move(self, p):
        return range(1, min(self.max_move + 1, self.n_position - p + 1))

    def primitive(self, p):
        if self.is_primitive(p):
            return "LOSE"
        else:
            print("This position is not primitive.")

    def is_primitive(self, p):
        return p == self.n_position

    def print_current_position(self, curr_position):
        print("\nCurrent position: %i" % curr_position)

    def print_possible_move(self, curr_position):
        move_list = self.gen_move(curr_position)
        print("your possible moves are", end=" ")
        print(move_list)


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
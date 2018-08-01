# -*- coding: utf-8 -*-

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
    def __init__(self, init_positon=0, n_position=10, max_move=2):
        self.curr_positon = init_positon
        self.n_position = n_position
        self.max_move = max_move
        self.goal_position = range(n_position % (max_move + 1), n_position + 1, max_move + 1)

    def solve(self, p):
        if p in self.goal_position:
            return "LOSE"
        else:
            return "WIN"

    def do_move(self, m):
        self.curr_positon += m

    def gen_best_move(self, p):
        if p in self.goal_position:
            return min(self.gen_move(p))
        else:
            return self.goal_position[bisect.bisect(self.goal_position, p)] - p

    def gen_move(self, p):
        return range(1, min(self.max_move + 1, self.n_position - p + 1))

    def primitive(self, p):
        if self.is_primitive(p):
            return "LOSE"
        else:
            print("This position is not primitive.")

    def is_primitive(self, p):
        return p == self.n_position


class Database:
    def __init__(self, game):
        self.data = {}
        for p in range(game.n_position, -1, -1):    # 10 to 0
            if game.is_primitive(p):
                last_lose = 0
                last_win = None
                self.add_position(position = p, value=game.primitive(p), remoteness=0)
            else:
                value = game.solve(p)
                if value == "LOSE":
                    remoteness = 1 + last_win    # 1 + max(all_win) in the future
                    last_lose = remoteness
                elif value == "WIN":
                    remoteness = 1 + last_lose    # 1 + min(all_lose) in the future
                    last_win = remoteness
                else:
                    pass    # for tie and draw in the future
                self.add_position(position=p, value=value, remoteness=remoteness)

    def add_position(self, position, value, remoteness):
        self.data[position] = (value, remoteness)


class Player:
    def __init__(self, is_human):
        self.is_human = is_human

    def do_player_move(self, main_game):
        value, remoteness = main_game.database.data[main_game.game.curr_positon]
        print("At current position, %s will %s in %i." % (main_game.players[main_game.turn][0], value, remoteness))
        if self.is_human:
            while True:
                try:
                    m = int(input('Please give an available move: '))
                except:
                    m = 0
                if m in main_game.game.gen_move(main_game.game.curr_positon):
                    break
        else:
            m = main_game.game.gen_best_move(main_game.game.curr_positon)
            print("Then computer moves %i." % m)
        main_game.game.do_move(m)


class MainGame:
    def __init__(self, game_name):
        self.game = None
        self.players = []
        self.n_player = 0
        self.turn = 0
        self.database = None
        self.create_game(game_name)

    def create_game(self, game_name):
        if game_name == "OneToN":
            self.game = OneToN(init_positon=0, n_position=10, max_move=2)
            self.database = Database(self.game)
        else:
            print("Please start a game.")

    def add_player(self, is_human):
        if is_human:
            name = input('What\'s your name: ')
        else:
            name = "computer"
        self.players.append([name, Player(is_human=is_human)])

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

    def start(main_game):
        main_game.start()
        print("The players are: ")
        for i in range(len(main_game.players)):
            print(main_game.players[i][0])
        while not main_game.game.is_primitive(main_game.game.curr_positon):
            if main_game.turn < main_game.n_player:
                print("\nCurrent position: %i, and it's %s's turn." % (main_game.game.curr_positon, main_game.players[main_game.turn][0]))
                main_game.players[main_game.turn][1].do_player_move(main_game=main_game)
                if not main_game.game.is_primitive(main_game.game.curr_positon):
                    main_game.turn += 1
            else:
                main_game.turn = 0

        print("\nCurrent position: %i" % main_game.game.curr_positon)
        print("At current position, %s WINs." % main_game.players[main_game.turn][0])
        print("Game over\n")


    # Start a game with one human and one computer (human first).
    main_game = MainGame(game_name="OneToN")
    main_game.add_player(is_human=True)    # Add player
    main_game.add_player(is_human=False)    # Add computer
    start(main_game=main_game)

    # Start another game with two humans.
    main_game = MainGame(game_name="OneToN")
    main_game.add_player(is_human=True)    # Add player 1
    main_game.add_player(is_human=True)    # Add player 2
    start(main_game=main_game)
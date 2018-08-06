# -*- coding: utf-8 -*-

"""
Python 3.5.2

Only support 2 player game now
"""

import bisect
import OneToN
import OddOrEven
import Solver
import argparse

parser = argparse.ArgumentParser(description='Game Player')
parser.add_argument('-g', '--game_name', choices=["OneToN", "OddOrEven"], required=True,
                    help='the game name, "OneToN" or "OddOrEven"')
parser.add_argument('-d', '--database_name', default=None,
                    help='filename of the database file')
parser.add_argument('-m', '--mode', default="pvc", choices=["pvp", "pvc"], help="game mode: 'pvp' or 'pvc'")
args = parser.parse_args()

# data_dict a dict save the value and the remoteness of position,
# key is position, val is also a dict with key="value" or "remoteness"
class Database:
    def __init__(self, game, solver):
        self.data_dict = {}
        if args.database_name is None:
            solver.solve(game.init_position, game, data_dict=self.data_dict)
            # for p in self.data_dict.keys():
               # game.print_current_position(p)
        else:
            # TODO: use database file
            print("Can not use database file not! Add this later")
            exit(-1)

    def solve(self, position):
        return self.data_dict[position]


class Player:
    def __init__(self, name, is_human):
        self.name = name
        self.is_human = is_human

    def do_player_move(self, main_env):
        position = main_env.curr_position
        result = main_env.database.solve(position)
        value = result["value"]
        remoteness = result["remoteness"]
        # TODO: add --hint, if --hint, then print this
        print("At current position, %s will %s in %i." % (self.name, value, remoteness))
        if self.is_human:
            while True:
                try:
                    m = int(input('Please give an available move: '))
                except:
                    m = 0
                if m in main_env.game.gen_move(main_env.curr_position):
                    break
                else:
                    main_env.game.print_possible_move(main_env.curr_position)
        else:
            m = self.gen_best_move(main_env)
            print("Then computer moves %i." % m)
        main_env.curr_position = main_env.game.do_move(main_env.curr_position, m)

    def gen_best_move(self, main_env):
        p = main_env.curr_position
        database = main_env.database
        tie_move = None
        max_remote = 0
        max_remote_move = None
        for m in main_env.game.gen_move(p):
            new_p = main_env.game.do_move(p, m)
            result= database.solve(new_p)
            if result["value"] == "LOSE":
                return m
            elif result["value"] == "TIE":
                tie_move = m
            elif result["value"] == "WIN":
                if max_remote < result["remoteness"]:
                    max_remote = result["remoteness"]
                    max_remote_move = m
        if tie_move is not None:
            return tie_move
        else:
            return max_remote_move


# Keep the dynamic information of the game, like curr_position, turn...
class MainEnv:
    def __init__(self, game_name):
        self.game = None
        self.players = []
        self.n_player = 0
        self.database = None
        self.turn = 0

        # Change: following code executes the function of previous "create_game" function.
        if game_name == "OneToN":
            self.game = OneToN.OneToN()
        elif game_name == "OddOrEven":
            self.game = OddOrEven.OddOrEven()
        # I move curr_position to MainEnv class, because it is dynamic
        self.curr_position = self.game.init_position
        self.database = Database(game=self.game, solver=Solver.Solver())

    def add_player(self, is_human):
        if is_human:
            name = input('What\'s your name: ')
        else:
            name = "computer"
        self.players.append(Player(name = name, is_human=is_human))

    def play(self):
        self.n_player = len(self.players)
        print("The players are: ")
        for i in range(len(self.players)):
            print(self.players[i].name, end=" ")
        print("")
        game = self.game  # for shorten the code
        while not game.is_primitive(self.curr_position):

            game.print_current_position(self.curr_position)
            print("it's %s's turn." % self.players[self.turn].name)

            self.players[self.turn].do_player_move(env=self)
            if not game.is_primitive(self.curr_position):
                self.turn ^= 1
            else:
                break


        game.print_current_position(self.curr_position)
        print("At current position, %s WINs." % self.players[self.turn].name)
        print("Game over\n")


if __name__ == '__main__':

    main_env = MainEnv(game_name=args.game_name)
    # Start a game with one human and one computer (human first).
    if args.mode == "pvc":
        main_env.add_player(is_human=True)  # Add player
        main_env.add_player(is_human=False)  # Add computer
    elif args.mode == "pvp":
        main_env.add_player(is_human=True)  # Add player
        main_env.add_player(is_human=True)  # Add computer

    main_env.play()

'''
    # Start another game with two humans.
    main_env = MainEnv(game_name="OneToN")
    main_env.add_player(is_human=True)  # Add player 1
    main_env.add_player(is_human=True)  # Add player 2
    start(main_env=main_env)
'''
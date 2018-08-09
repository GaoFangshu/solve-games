from final_project import Game, Database
from copy import deepcopy


# Env holds game and dynamic variables (analysis, database later). GameGUI just interacts with Env.
class Env:
    def __init__(self, board_row, board_col):
        self.board_row = board_row
        self.board_col = board_col
        self.game = None
        self.turn = None
        self.players = None
        self.database = None
        self.curr_position = None

        self.restart()

    def restart(self):
        self.turn = [0, 0]
        self.players = []
        self.database = None
        self.game = Game.Game(board_row=self.board_row, board_col=self.board_col)  # TODO: handle start_player
        self.curr_position = self.game.init_position
        self.database = Database.Database(row=self.board_row, col=self.board_col)

    def add_player(self, is_human):    # TODO: human name
            if is_human:
                name = "human"
            else:
                name = "computer"
            self.players.append(Player(name = name, is_human=is_human))

    def gen_best_move(self, turn):
        current_value, current_remoteness = database.lookup(position)
        position_list = []
        value_list = []
        remoteness_list = []
        valid_moves = self.game.gen_move(self.curr_position, turn)
        for move in valid_moves:
            position = game.do_move(p=deepcopy(game.curr_position), m=move, turn=turn))
            value, remoteness = database.lookup(position)
            position_list.append(position)
            value_list.append(value)
            remoteness_list.append(remoteness)

        if current_value == "LOSE":
                return m
        elif current_value == "WIN":
                if max_remote < result["remoteness"]:
                    max_remote = result["remoteness"]
                    max_remote_move = m
        if tie_move is not None:
            return tie_move
        else:
            return max_remote_move

class Player:
    def __init__(self, name, is_human):
        self.name = name
        self.is_human = is_human

    def do_player_move(self, env):
        position = env.curr_position
        result = env.database.solve(position)
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
                if m in env.game.gen_move(env.curr_position):
                    break
                else:
                    env.game.print_possible_move(env.curr_position)
        else:
            m = self.gen_best_move(env)
            print("Then computer moves %i." % m)
        env.curr_position = env.game.do_move(env.curr_position, m)

    def gen_best_move(self, env):
        pass


if __name__ == '__main__':

    main_env = Env(game_name='Isolation')
    '''
    # Start a game with one human and one computer (human first).
    if args.mode == "pvc":
        main_env.add_player(is_human=True)  # Add player
        main_env.add_player(is_human=False)  # Add computer
    elif args.mode == "pvp":
        main_env.add_player(is_human=True)  # Add player
        main_env.add_player(is_human=True)  # Add computer
    '''
    main_env.play()
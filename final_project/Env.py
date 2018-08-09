import Game, Database
from copy import deepcopy


# Env holds game and dynamic variables (analysis, database later). GameGUI just interacts with Env.
class Env:
    def __init__(self, board_row, board_col):
        self.board_row = board_row
        self.board_col = board_col
        self.game = None
        self.turn = None
        self.players = None
        self.turn_to_player = {}
        self.database = None
        self.curr_position = None
        # predict_info:
        #   {"move": {"[move_row, move_col]": [value, remoteness], ...},
        #    "delete": {"[move_row, move_col]": [{"[delete_row, delete_col]": [value, remoteness], ...}], ...}
        #   }
        self.predict_info = None
        self.prediction = False

        self.last_move = None

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

    def predict(self, curr_p, turn, valid_moves):
        info = {}
        self.predict_info = {"move":{}, "delete":{}}
        #valid_moves = self.game.gen_move(curr_p, turn)
        for move in valid_moves:
            position = self.game.do_move(p=curr_p, m=move, turn=turn)
            turn_next = self.next_turn(turn)
            valid_deletes = self.game.gen_move(position, turn_next)
            value_list = []
            remoteness_list = []
            for delete in valid_deletes:
                final_position = self.game.do_move(p=position, m=delete, turn=turn_next)
                value, remoteness = self.database.lookup(final_position)
                value_list.append(value)
                remoteness_list.append(remoteness + 1)
            info[str(move)] = [valid_deletes, value_list, remoteness_list]

        # get "move" step prediction
        for move in info:
            valid_deletes, value_list, remoteness_list = info[move]
            if "LOSE" in value_list:  # this move has LOSE position for opponent, this move is WIN for me
                # choose LOSE smallest remoteness
                index_lose = [i for i, value in enumerate(value_list) if value == "LOSE"]
                min_remoteness = max(remoteness_list)
                for index in index_lose:
                    if min_remoteness >= remoteness_list[index]:
                        min_remoteness = remoteness_list[index]
                self.predict_info["move"][move] = ["LOSE", min_remoteness]

            else:  # this move leads to all WIN, this move is LOSE for me
                # choose WIN largest remoteness
                index_max = remoteness_list.index(max(remoteness_list))
                self.predict_info["move"][move] = ["WIN", remoteness_list[index_max]]

        # get "delete" step prediction
        self.predict_info["delete"] = info

        print(self.predict_info)

    def gen_best_position(self, curr_p, turn):  # return position(list), value("WIN" or "LOSE"), remoteness(int)
        current_value, current_remoteness = self.database.lookup(curr_p)
        position_list = []
        value_list = []
        remoteness_list = []
        valid_moves = self.game.gen_move(curr_p, turn)
        for move in valid_moves:
            position = self.game.do_move(p=curr_p, m=move, turn=turn)
            turn_next = self.next_turn(turn)
            valid_deletes = self.game.gen_move(position, turn_next)
            for delete in valid_deletes:
                final_position = self.game.do_move(p=position, m=delete, turn=turn_next)
                value, remoteness = self.database.lookup(final_position)
                position_list.append(final_position)
                value_list.append(value)
                remoteness_list.append(remoteness)

        if current_value == "LOSE":
            index_max = remoteness_list.index(max(remoteness_list))
            return position_list[index_max], value_list[index_max], remoteness_list[index_max]
        elif current_value == "WIN":
            index_lose = [i for i, value in enumerate(value_list) if value == "LOSE"]
            min_remoteness = max(remoteness_list)
            for index in index_lose:
                if min_remoteness >= remoteness_list[index]:
                    min_position = position_list[index]
                    min_value = value_list[index]
                    min_remoteness = remoteness_list[index]
            return min_position, min_value, min_remoteness

    def next_turn(self, turn):
        next_turn = deepcopy(turn)
        if turn[0] == 0 and turn[1] == 0:
            next_turn[1] = 1
        elif turn[0] == 0 and turn[1] == 1:
            next_turn[0] = 1
            next_turn[1] = 0
        elif turn[0] == 1 and turn[1] == 0:
            next_turn[1] = 1
        elif turn[0] == 1 and turn[1] == 1:
            next_turn[0] = 0
            next_turn[1] = 0
        return next_turn

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


if __name__ == '__main__':
    main_env = Env()

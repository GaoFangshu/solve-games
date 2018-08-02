
# TODO: handle the "TIE" situation
class Solver:
    def __init__(self):
        pass

    # Change: change the form of the return value.
    def solve(self, p, game, data_dict):
        # game.print_current_position(p)
        # if p[0]==3 and p[1]==0 and p.turn == 1:
            # print("12333333333333333333333333")
        if p in data_dict:
            return data_dict[p]
        elif game.is_primitive(p):
            data_dict[p] = {"value": game.primitive(p), "remoteness": 0}
            return data_dict[p]
        else:
            children = [game.do_move(p, m) for m in game.gen_move(p)]  # positions of p's children
            child_info = [self.solve(child, game, data_dict) for child in children]
            values = [child["value"] for child in child_info]
            remoteness = [child["remoteness"] for child in child_info]

            if all(value == "WIN" for value in values):  # all children are WIN
                data_dict[p] = {"value": "LOSE", "remoteness": 1 + max(remoteness)}
                return data_dict[p]
            elif "LOSE" in values:  # there exists at least 1 LOSE
                remoteness_lose = [child["remoteness"] for child in child_info if child["value"] == "LOSE"]
                data_dict[p] = {"value": "WIN", "remoteness": 1 + min(remoteness_lose)}
                return data_dict[p]

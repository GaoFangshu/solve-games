OneToN.py and OddOrEven.py are two games, keep their static information(rule)
If you want to change the parameters for the game, you can change them in their game file at the start of the code.

Solver.py is a solver can be use for all game.
If we don't have an external database file, then the player will call Solver.solve(start_position),
and get all the {position : value/remoteness} pairs, and store them in runtime database(a dict array).
Then If we need the information of the position, we only need to search the database, and don't need to call solver any more

Player.py is the player for the all the game, keep the dynamic information of the game, like current position...

We haven't support external database file yet, so don't use -d.

usage: Player.py [-h] -g {OneToN,OddOrEven} [-d DATABASE_NAME] [-m {pvp,pvc}]
eg: python3 Player.py -g OddOrEven -m "pvc"
OneToN.py and OddOrEven.py are two games, keep their static information(rule)
Solver.py is a solver can be use for all game
Player.py is the player for the all the game, keep the dynamic information of the game.

If you want to change the parameters for the game, you should change them in their game file.
We haven't support database function yet.

usage: Player.py [-h] -g {OneToN,OddOrEven} [-d DATABASE_NAME] [-m {pvp,pvc}]
eg: python3 Player.py -g OddOrEven -m "pvc"
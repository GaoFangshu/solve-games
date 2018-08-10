# solve-games :heavy_check_mark:
Solve games in computaional game theory class.

![](./final_project/img/Player1Win.png) If you only play Human vs. Human [Isolation](https://en.wikipedia.org/wiki/Isolation_(board_game)) game, python files are enough. (just run `python GameGUI.py` in terminal)

![](./final_project/img/Player2Win.png) If you want to play with computer or need prediction, run C++ first to get database, and compile the `reader.cpp` to get a `reader.exe` file. Put the `reader.exe` and the database file in the **same folder** with the GameGUI.py.

Remark: The  `reader.cpp` use a `_fseeki64` function, which is only support in VS. If you use other compiler, you should change it to `fseek` function, but it will only support gameboard smaller than 5*5

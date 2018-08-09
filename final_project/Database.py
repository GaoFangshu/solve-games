import os

value_dict = {0:"WIN", 1:"LOSE"}

class Database:
    def __init__(self, row, col):
        # connect to file
        # self.filename blabla
        self.row = row
        self.col = col
        self.n = row * col

    def hash(self, p):
        '''
        hash position to hash value
            for example, a gameboard like this: '.' is valid grid, 'x' is deleted grid, 0 is player0, 1 is player1
            0 . . .
            . . . x
            . x . .
            . . . 1
            position = [[2, 1, 1, 1], [1, 1, 1, 0], [1, 0, 1, 1], [1, 1, 1, 3]]
            then hash values can be calculate as:
            (2^7 + 2^9) + (2^16 * 0) + (2^16*16 * 15) = 3860
        '''
        i = 0
        hash_value = 0
        for r in p:
            for c in r:
                if c == 0:
                    hash_value += 2 ** i
                elif c == 2:
                    hash_value += 2 ** self.n * i
                elif c == 3:
                    hash_value += 2 ** self.n * self.n * i
                i += 1

        return hash_value

    def get_info(self, ret):
        '''
        the highest bit means win/lose (win is 0, lose is 1), other 7 bits is the remoteness
            for example: (10001110)_2 means: LOSE and 14 remoteness.
        '''
        msg = "{0:b}".format(ret).zfill(8)
        value = int(msg[-8])  # 0 for win, 1 for lose
        remoteness = int(msg[-7:], 2)
        return value_dict[value], remoteness

    def lookup(self, p):
        hash_value = self.hash(p)
        ret = os.system("reader.exe database_%s_%s.db %s" % (str(self.row), str(self.col), str(hash_value)))
        return self.get_info(ret)

if __name__ == '__main__':
    position1 = [[2, 1, 1, 1], [1, 1, 0, 1], [1, 1, 1, 1], [1, 1, 3, 1]]  # player 2 to move and delete
    position2 = [[2, 1, 1, 1], [0, 1, 0, 1], [1, 3, 1, 1], [1, 1, 1, 1]]  # player 1 to move and delete
    database = Database(row=4, col=4)
    print(database.lookup(position1))
    print(database.lookup(position2))

    position3 = [[1, 1, 2, 1], [1, 1, 1, 1], [1, 1, 0, 1], [1, 1, 3, 1]]
    print(database.lookup(position3))
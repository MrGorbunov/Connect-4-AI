from enum import IntEnum


class CGame(IntEnum):
    EMPTY = 0  # No chip
    RED = 1  # Red chip
    YELLOW = 2  # Yellow chip

    COLUMN = 6  # Spaces in a x_pos
    ROW = 7  # Spaces in a y_pos


class Board():
    def __init__(self):
        self.boardState = [[0] * CGame.ROW for y_pos in range(0, CGame.COLUMN)]
        self.turn = 0

    def changeTurn(self):
        self.turn = self.turn + 1

    def isCompTurn(self):
        return self.turn % 2 == 0

    def editBoard(self, moveNumber):
        for y_pos in range(0, CGame.COLUMN):  # checks for each y_pos in a x_pos for empty space
            if self.boardState[y_pos][moveNumber] == 0:  # if the spot you want to place in is not occupied
                if self.isCompTurn():  # if it is player 1's turn
                    self.boardState[y_pos][moveNumber] = 1
                else:  # if it is player 2's turn
                    self.boardState[y_pos][moveNumber] = 2
                break

    def horizontalWin(self):
        isWin = False
        for y_pos in range(0, CGame.COLUMN):
            for x_pos in range(0, CGame.ROW):
                if x_pos + 3 < CGame.ROW:
                    if self.boardState[y_pos][x_pos] == self.boardState[y_pos][x_pos + 1] == self.boardState[y_pos][x_pos + 2] == \
                            self.boardState[y_pos][x_pos + 3] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def verticalWin(self):
        isWin = False
        for y_pos in range(0, CGame.COLUMN):
            for x_pos in range(0, CGame.ROW):
                if y_pos + 3 < CGame.COLUMN:
                    if self.boardState[y_pos][x_pos] == self.boardState[y_pos + 1][x_pos] == self.boardState[y_pos + 2][x_pos] == \
                            self.boardState[y_pos + 3][x_pos] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def diagonalRightWin(self):
        isWin = False
        for y_pos in range(0, CGame.COLUMN):
            for x_pos in range(0, CGame.ROW):
                if y_pos + 3 < CGame.COLUMN and x_pos + 3 < CGame.ROW:
                    if self.boardState[y_pos][x_pos] == self.boardState[y_pos + 1][x_pos + 1] == self.boardState[y_pos + 2][x_pos + 2] == \
                            self.boardState[y_pos + 3][x_pos + 3] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def diagonalLeftWin(self):
        isWin = False
        for y_pos in range(0, CGame.COLUMN):
            for x_pos in range(0, CGame.ROW):
                if x_pos - 3 >= 0 and y_pos + 3 < CGame.COLUMN:
                    if self.boardState[y_pos][x_pos] == self.boardState[y_pos + 1][x_pos - 1] == self.boardState[y_pos + 2][x_pos - 2] == \
                            self.boardState[y_pos + 3][x_pos - 3] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def isWinner(self):
        win = False
        if self.horizontalWin() or self.verticalWin() or self.diagonalRightWin() or self.diagonalLeftWin():
            win = True
        return win

    def printBoard(self):
        for y_pos in range(0, CGame.COLUMN):
            print(self.boardState[CGame.COLUMN - y_pos - 1])
        print(" 1  2  3  4  5  6  7")

from enum import IntEnum


class CGame(IntEnum):
    EMPTY = 0  # No chip
    RED = 1  # Red chip
    YELLOW = 2  # Yellow chip

    COLUMN = 6  # Spaces in a column
    ROW = 7  # Spaces in a row


class Board():
    def __init__(self):
        self.boardState = [[0] * 7] * 6
        self.turn = 0

    def changeTurn(self):
        self.turn = self.turn + 1

    def isCompTurn(self):
        return self.turn % 2 == 0

    def editBoard(self, moveNumber):
        for i in range(0, CGame.COLUMN):  # checks for each COLUMN in a ROW for empty space
            if self.boardState[i][moveNumber] == CGame.EMPTY:  # if the spot you want to place in is not occupied
                if self.isCompTurn():  # if it is player 1's turn
                    self.boardState[i][moveNumber] = CGame.RED
                else:  # if it is player 2's turn
                    self.boardState[i][moveNumber] = CGame.YELLOW
                break

    def horizontalWin(self):
        isWin = False
        for i in range(0, CGame.COLUMN):
            for j in range(0, CGame.ROW):
                if j + 3 < CGame.ROW:
                    if self.boardState[i][j] == self.boardState[i][j + 1] == self.boardState[i][j + 2] == \
                            self.boardState[i][j + 3] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def verticalWin(self):
        isWin = False
        for i in range(0, CGame.COLUMN):
            for j in range(0, CGame.ROW):
                if i + 3 < CGame.COLUMN:
                    if self.boardState[i][j] == self.boardState[i + 1][j] == self.boardState[i + 2][j] == \
                            self.boardState[i + 3][j] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def diagonalRightWin(self):
        isWin = False
        for i in range(0, CGame.COLUMN):
            for j in range(0, CGame.ROW):
                if i + 3 < CGame.COLUMN and j + 3 <CGame.ROW:
                    if self.boardState[i][j] == self.boardState[i + 1][j + 1] == self.boardState[i + 2][j + 2] == \
                            self.boardState[i + 3][j + 3] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def diagonalLeftWin(self):
        isWin = False
        for i in range(0, CGame.COLUMN):
            for j in range(0, CGame.ROW):
                if j - 3 >= 0 and i + 3 < CGame.COLUMN:
                    if self.boardState[i][j] == self.boardState[i + 1][j - 1] == self.boardState[i + 2][j - 2] == \
                            self.boardState[i + 3][j - 3] != CGame.EMPTY:
                        isWin = True
                        return isWin
        return isWin

    def isWinner(self):
        win = False
        if self.horizontalWin() or self.verticalWin() or self.diagonalRightWin() or self.diagonalLeftWin():
            win = True
        return win

    def printBoard(self):
        for column in range(0, CGame.COLUMN):
            print(self.boardState[column])
        print(" 1  2  3  4  5  6  7")

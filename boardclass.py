class Board():
    n = 0
    r = 1
    y = 2

    def __init__(self):
        self.row5 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row4 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row3 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row2 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row1 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row0 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation

        self.boardState = [self.row0, self.row1, self.row2, self.row3, self.row4, self.row5]

        self.turn = 0

    def changeTurn(self):
        self.turn = self.turn + 1

    def isCompTurn(self):
        return self.turn % 2 == 0

    def editBoard(self, moveNumber):
        for i in range(0, len(self.boardState)):  # checks for each row in a column for empty space
            if self.boardState[i][moveNumber] == self.n:  # if the spot you want to place in is not occupied
                if self.isCompTurn():  # if it is player 1's turn
                    self.boardState[i][moveNumber] = self.r
                else:  # if it is player 2's turn
                    self.boardState[i][moveNumber] = self.y
                break

    def horizontalWin(self):
        isWin = False
        for i in range(0, len(self.boardState)):
            for j in range(0, len(self.row0)):
                if j + 3 < len(self.row0):
                    if self.boardState[i][j] == self.boardState[i][j + 1] == self.boardState[i][j + 2] == self.boardState[i][j + 3] != self.n:
                        isWin = True
                        return isWin
        return isWin

    def verticalWin(self):
        isWin = False
        for i in range(0, len(self.boardState)):
            for j in range(0, len(self.row0)):
                if i + 3 < len(self.boardState):
                    if self.boardState[i][j] == self.boardState[i + 1][j] == self.boardState[i + 2][j] == self.boardState[i + 3][j] != self.n:
                        isWin = True
                        return isWin
        return isWin

    def diagonalRightWin(self):
        isWin = False
        for i in range(0, len(self.boardState)):
            for j in range(0, len(self.row0)):
                if i + 3 < len(self.boardState) and j + 3 < len(self.row0):
                    if self.boardState[i][j] == self.boardState[i + 1][j + 1] == self.boardState[i + 2][j + 2] == self.boardState[i + 3][j + 3] != self.n:
                        isWin = True
                        return isWin
        return isWin

    def diagonalLeftWin(self):
        isWin = False
        for i in range(0, len(self.boardState)):
            for j in range(0, len(self.row0)):
                if j - 3 >= 0 and i + 3 < len(self.boardState):
                    if self.boardState[i][j] == self.boardState[i + 1][j - 1] == self.boardState[i + 2][j - 2] == self.boardState[i + 3][j - 3] != self.n:
                        isWin = True
                        return isWin
        return isWin

    def isWinner(self):
        win = False
        if self.horizontalWin() or self.verticalWin() or self.diagonalRightWin() or self.diagonalLeftWin():
            win = True
        return win

    def printBoard(self):
        print(self.row5)
        print(self.row4)
        print(self.row3)
        print(self.row2)
        print(self.row1)
        print(self.row0)
        print(" 1  2  3  4  5  6  7")

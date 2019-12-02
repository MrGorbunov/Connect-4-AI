import random

n = 0  # no chip
r = 1  # red chip
y = 2  # yellow chip
count = 0
winner = n

row5 = [n, n, n, n, n, n, n]  # empty board creation
row4 = [n, n, n, n, n, n, n]
row3 = [n, n, n, n, n, n, n]
row2 = [n, n, n, n, n, n, n]
row1 = [n, n, n, n, n, n, n]
row0 = [n, n, n, n, n, n, n]

board = [row0, row1, row2, row3, row4, row5]


def main():
    global count
    while not isWinner():
        printBoard()
        playerTurn()
        count = count + 1
    if count % 2 == r:
        winner = r
        print("Winner P1!")
    else:
        winner = y
        print("Winner P2!")


def playerTurn():
    if count % 2 == 0:
        print("Select your column to place in")
        move = eval(input())
        editBoard(move-1)
    else:
        editBoard(computerDecision() - 1)

def computerDecision():
    move = random.randint(1, 7)
    print("Computer Move: " + str(move))
    return move

def editBoard(moveNumber):
    for i in range(0, len(board)):  # checks for each row in a column for empty space
        if board[i][moveNumber] == n:  # if the spot you want to place in is not occupied
            if count % 2 == 0:  # if it is player 1's turn
                board[i][moveNumber] = r
            else:  # if it is player 2's turn
                board[i][moveNumber] = y
            break


def horizontalWin():
    isWin = False
    for i in range(0, len(board)):
        for j in range(0, len(row1)):
            if j + 3 < len(row1):
                if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] != n:
                    isWin = True
                    return isWin
    return isWin


def verticalWin():
    isWin = False
    for i in range(0, len(board)):
        for j in range(0, len(row1)):
            if i + 3 < len(board):
                if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] != n:
                    isWin = True
                    return isWin
    return isWin


def diagonalRightWin():
    isWin = False
    for i in range(0, len(board)):
        for j in range(0, len(row1)):
            if i + 3 < len(board) and j + 3 < len(row1):
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] != n:
                    isWin = True
                    return isWin
    return isWin


def diagonalLeftWin():
    isWin = False
    for i in range(0, len(board)):
        for j in range(0, len(row1)):
            if j - 3 >= 0 and i + 3 < len(board):
                if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] != n:
                    isWin = True
                    return isWin
    return isWin


def isWinner():
    win = False
    if horizontalWin() or verticalWin() or diagonalRightWin() or diagonalLeftWin():
        win = True
    return win


def printBoard():
    print(row5)
    print(row4)
    print(row3)
    print(row2)
    print(row1)
    print(row0)
    print(" 1  2  3  4  5  6  7")

main()

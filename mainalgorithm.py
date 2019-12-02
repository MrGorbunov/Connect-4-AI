from board import Board
import random

currentBoard = Board()


def playerTurn():
    if currentBoard.isCompTurn():
        print("Select your column to place in")
        move = eval(input())
        currentBoard.editBoard(move - 1)
    else:
        currentBoard.editBoard(computerDecision() - 1)  # will create comp decision method


def computerDecision():
    move = random.randint(1, 7)
    print("Computer Move: " + str(move))
    return move


while not currentBoard.isWinner():
    currentBoard.printBoard()
    playerTurn()
    currentBoard.changeTurn()

#In the search, boards are duplicated all around
import copy



def static_eval(board):
    '''Returns the value of the board, + = 1 and - = 2'''
    #Length 2 = +4
    #Length 3 = +9
    #Length 4 = +1000

    board_eval = 0

    for con in board.connections:
        multiplier = 1
        if con[0] == 2:
            multiplier = -1

        length = len(con) - 1

        if length == 2:
            board_eval += multiplier * 4
        elif length == 3:
            board_eval += multiplier * 9
        elif length == 4:
            board_eval += multiplier * 1000
    
    return board_eval



def get_best_move(board, depth):
    '''Will recursively find the best move via min max. Depth 1 = one layer, not one round'''
    if depth == 0:
        return 0
    depth -= 1


    minimize = False
    if not board.isCompTurn():
            minimize = True

    best_move = None 
    best_value = None


    for i in range(0, 7):
        alt_board = copy.deepcopy(board)

        if alt_board.handle_turn(i) == False:
            #invalid move
            continue

        if minimize:
            valuation = max_outcome(alt_board, depth)
            
            if valuation < best_value or best_value == None:
                best_value = valuation
                best_move = i

        else:
            valuation = max_outcome(alt_board, depth)

            if valuation > best_value or best_value == None:
                best_value = valuation
                best_move = i


    return best_move





#
# There are two almost identical functions to avoid if/elses
# These functions are called thousands of times so minor optimizations add up

def min_outcome(board, depth):
    '''Will return the minimum possible outcome given depth, not what moves made it'''
    if depth == 0:
        return static_eval(board)
    depth -= 1

    #handle first move
    alt_board = copy.deepcopy(board)
    alt_board.handle_turn(0)
    min_value = max_outcome(alt_board, depth)
    
    #handle rest of moves
    for i in range(1, 7):
        alt_board = copy.deepcopy(board)
        alt_board.handle_turn(i)
        value = max_outcome(alt_board, depth)

        if value < min_value:
            min_value = value
    return min_value


def max_outcome(board, depth):
    '''Will return the maximum possible outcome given depth, not what moves made it'''
    if depth == 0:
        return static_eval(board)
    depth -= 1

    #handle first move
    alt_board = copy.deepcopy(board)
    alt_board.handle_turn(0)
    max_value = min_outcome(alt_board, depth)

    #handle rest
    for i in range(1, 7):
        alt_board = copy.deepcopy(board)
        alt_board.handle_turn(i)
        value = min_outcome(alt_board, depth)

        if value > max_value:
            max_value = value

    return max_value





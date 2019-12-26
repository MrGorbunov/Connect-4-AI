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



def get_best_move(board, depth, debug = False):
    '''Will recursively find the best move via min max. Depth 1 = one layer, not one round'''
    if depth == 0:
        return 0
    depth -= 1

    if debug:
        print "Minmaxing for the best move"
        print "depth: {0}, cur_eval: {1}, minimizing: {2}".format(depth, static_eval(board), board.is_comp_turn())

    minimize = False
    if not board.is_comp_turn():
            minimize = True

    best_move = None 
    best_value = None


    for i in range(0, 7):
        alt_board = copy.deepcopy(board)

        if alt_board.handle_turn(i) == False:
            #invalid move
            continue

        if minimize:
            #minimze the maxima
            valuation = max_outcome(alt_board, depth, best_value)
            
            if valuation < best_value or best_value == None:
                best_value = valuation
                best_move = i
            
        else:
            #maximize the minima
            valuation = min_outcome(alt_board, depth, best_value)

            if valuation > best_value or best_value == None:
                best_value = valuation
                best_move = i
    
    print "best_move: {0}, projected eval: {1}".format(best_move, best_value)
    return best_move






#
# There are two almost identical functions to avoid if/elses
# These functions are called thousands of times so minor optimizations add up


#for reference, here are some benchmarks for depth 7 searches
#w/ pruning: 43s
#w/o pruning: 2:43 = 163s


#cur_min & max are used for alpha-beta pruning
def min_outcome(board, depth, cur_max):
    '''Will return the minimum possible outcome given depth, not what moves made it'''
    if depth == 0:
        return static_eval(board)
    depth -= 1

    #handle first move
    alt_board = copy.deepcopy(board)
    alt_board.handle_turn(0)
    min_value = max_outcome(alt_board, depth, None)

    if min_value <= cur_max:
        return min_value
    
    #handle rest of moves
    for i in range(1, 7):
        alt_board = copy.deepcopy(board)
        alt_board.handle_turn(i)
        value = max_outcome(alt_board, depth, min_value)

        #pruning
        if value <= cur_max:
            return value

        if value < min_value:
            min_value = value
    
    return min_value


def max_outcome(board, depth, cur_min):
    '''Will return the maximum possible outcome given depth, not what moves made it'''
    if depth == 0:
        return static_eval(board)
    depth -= 1

    #handle first move
    alt_board = copy.deepcopy(board)
    alt_board.handle_turn(0)
    max_value = min_outcome(alt_board, depth, None)
    
    if max_value >= cur_min and cur_min != None:
        return max_value

    #handle rest
    for i in range(1, 7):
        alt_board = copy.deepcopy(board)
        alt_board.handle_turn(i)
        value = min_outcome(alt_board, depth, max_value)

        #pruning
        if value >= cur_min and cur_min != None:
            return value

        if value > max_value:
            max_value = value

    return max_value





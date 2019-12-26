from boardclass import *
from algorithm import *


def __main__():
#   alpha_beta_pruning()
    always_takes_win()
    guaranteed_wins()
    

def alpha_beta_pruning():
    '''Runs ambiguous cases to provide different values during evaluation,
    to see true pruning in action, you must configure algorithm.py to print info'''
    b = Board()
    
    b.handle_turn(4)
    b.handle_turn(5)
    
    b.handle_turn(6)
    b.handle_turn(6)
    
    b.handle_turn(5)
    b.handle_turn(3)

    b.handle_turn(2)

    b.print_board()

    print "2 to move, optimizing for min value"
    print ""
    print ""

    #Board state
    #
    #
    #          X O
    #    X O X O X
    #0 1 2 3 4 5 6
    # O to move

    move = get_best_move(b, 6)

    print ""
    print str(move) + " is considered best"



def guaranteed_wins():
    '''Tests for _ 1 1 1 _ situation'''
    b = Board()

    for move in range(2,4):
        b.handle_turn(0)
        b.handle_turn(move)

    #now setup to be
    #
    #1
    #1 _ 2 2 _ _ _

    b.handle_turn(0)
    b.handle_turn(0)

    b.handle_turn(0)
    b.handle_turn(get_best_move(b, 4)) 

    #now
    #1
    #2
    #1
    #1
    #1 _ 2 2 2 _ _ => 1 to move

    b.handle_turn(get_best_move(b, 3))
    b.handle_turn(get_best_move(b, 2))
    b.handle_turn(get_best_move(b, 1))
    #should now be a winner

    if b.is_winner() == False: 
        b.print_board()
        print "Failed to win 100% win situation"
    else:
        print "Correctly looked two turns ahead"
    



def always_takes_win():
    '''Tests if the AI will take the winning move (distance 1)'''
    b = Board()
    
    b.handle_turn(0)
    b.handle_turn(1)
    
    b.handle_turn(0)
    b.handle_turn(1)

    b.handle_turn(0)
    b.handle_turn(1)
  
    #Current state:
    #
    #1 2
    #1 2
    #1 2
    #0 1 2 3 4 5 6

    #going into 0 would be an insta win
    best_move = get_best_move(b, 1)

    if best_move != 0:
        b.print_board()
        print "{0} considered best move, should be 0".format(best_move)
    else:
        print "Correctly picked win. Move {0} is move 0".format(best_move)

    #now test the other way
    b = Board()
   
    b.handle_turn(5)
   
    b.handle_turn(0)
    b.handle_turn(1)
    
    b.handle_turn(0)
    b.handle_turn(1)

    b.handle_turn(0)
    b.handle_turn(1)
  
    #Current state:
    #
    #1 2
    #1 2
    #1 2
    #0 1 2 3 4 5 6

    #going into 0 would be an insta win
    best_move = get_best_move(b, 1)

    if best_move != 0:
        b.print_board()
        print "{0} considered best move, should be 0".format(best_move)
    else:
        print "Correctly picked win. Move {0} is move 0".format(best_move)



__main__()

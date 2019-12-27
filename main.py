'''
Connect 4 AI
'''


from boardclass import Board
from algorithm import get_best_move
from gui import *


#---------------------------------- Game Logic Globals -----------------------------
#used to act based on current situation
GAME_STATE = {
	"PLAYER_MOVE": 0,
	"AI_MOVE": 1,
	"ANIMATION": 2
}

ANIM_STATE = {
        "NONE": 0,
        "FALLING": 1,
        "CHOOSE": 2
}


#we import a dictionary for key presses from animation (it uses pygame enums)

#current state
game_state = GAME_STATE['PLAYER_MOVE']
anim_state = ANIM_STATE['NONE']
preview_move = 0

AGAINST_BOT = True
BOT_DEPTH = 6



board = Board()
#start with player
if board.is_comp_turn():
	board.change_turn()





#--------------------------------- Game Logic Commands --------------------------------	
def reset_turn():
    '''Resets the turn after animation is finished'''
    global game_state, anim_state
    #check for win
    if board.is_winner():
        global running
        draw_winning_connection(board)
        running = False

    switch_color()

    if board.is_comp_turn() and AGAINST_BOT:
        game_state = GAME_STATE['AI_MOVE']
        draw_new_preview(preview_move, board, draw_ghost = False)
    else:
        game_state = GAME_STATE['PLAYER_MOVE']
        draw_new_preview(preview_move, board)

    anim_state = ANIM_STATE['NONE']
    


def handle_move_logic():
    '''Updates the Board instance (board) and cur_images'''
    global preview_move, game_state, anim_state
    
    #check for valid move
    if board.empty_slots_in_col(preview_move) <= 0:
        return

    #animation
    game_state = GAME_STATE['ANIMATION']
    anim_state = ANIM_STATE['FALLING']
    set_falling_animation_parameters(board)
   
    #state
    preview_move %= 7
    board.handle_turn(preview_move)



def make_ai_turn():
    '''Calls on the algorithm to make a move, then sets animations into progress'''
    global preview_move, game_state, anim_state

    best_move = get_best_move(board, BOT_DEPTH)
   
    #animation
    game_state = GAME_STATE['ANIMATION']
    anim_state = ANIM_STATE['CHOOSE']
    set_choose_animation_parameters(best_move)
    
    #state
    preview_move = best_move





#------------------------------------- Main Loop ---------------------------------------
#this way the preivew move is there at the start
draw_new_preview(preview_move, board)


#main game loop
running = True
while running:
	#------------------ check events -----------
	for event in get_events():
		if event.type == EVENT_TYPE['QUIT']:
			running = False
			break
		
		
		#doesn't listen to input, but still allows for closing the window
		if game_state == GAME_STATE['ANIMATION']:
			break
	
                if game_state == GAME_STATE['AI_MOVE']:
                        break

		
		#something pressed
		if event.type == EVENT_TYPE['KEYDOWN']:
			if event.key == INPUT_TYPE['LEFT']:
                                preview_move -= 1
				draw_new_preview(preview_move, board)
				
			elif event.key == INPUT_TYPE['RIGHT']:
                                preview_move += 1
				draw_new_preview(preview_move, board)

			elif event.key == INPUT_TYPE['SELECT']:
				handle_move_logic()
				break
	


        #------------- GAME STATE ---------------
        if game_state == GAME_STATE['AI_MOVE']:
                #AI has yet to make up its mind
                make_ai_turn()


	#update based on game_state
	if game_state == GAME_STATE['ANIMATION']:
                if anim_state == ANIM_STATE['FALLING']:
                    #animations return True when they're done
                    if handle_falling_animation():
                        reset_turn()

                elif anim_state == ANIM_STATE['CHOOSE']:
                    if handle_choose_animation():
                        #this sets it up for the falling animation
                        handle_move_logic()

        game_tick()	


#this way there's a delay and you can admire the victory
game_tick()
asd = input()

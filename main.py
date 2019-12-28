'''
Connect 4 AI
'''


from boardclass import Board
from algorithm import get_best_move
from display import *


#---------------------------------- Game Logic Globals -----------------------------
#used to act based on current situation
GAME_STATE = {
	"PLAYER_MOVE": 0,
	"AI_MOVE": 1,
	"ANIMATION": 2,
        "END_SCREEN": 3
}

ANIM_STATE = {
        "NONE": 0,
        "FALLING": 1,
        "CHOOSE": 2,
        "GUI_DROPIN": 3,
        "SCREEN_RESET": 4
}

GUI_STATE = {
        "RESTART": 0,
        "QUIT": 1
}


#because pygame enums are referenced, EVENT_TYPE and INPUT_TYPE are imported

#current state
game_state = GAME_STATE['ANIMATION']
preview_move = 0
AGAINST_BOT = True
BOT_DEPTH = 6

anim_state = ANIM_STATE['SCREEN_RESET']

gui_state = GUI_STATE['RESTART']


board = Board()
#start with player
if board.is_comp_turn():
	board.change_turn()





#--------------------------------- Game Logic Commands --------------------------------	
def reset_game():
    '''Resets the game, including the board and drawing a blank screen'''
    global game_state, preview_move, anim_state, board

    game_state = GAME_STATE['PLAYER_MOVE']
    preview_move = 0
    anim_state = ANIM_STATE['NONE']

    board = Board()
    #start with player
    if board.is_comp_turn():
            board.change_turn()

    draw_blank_game()
    set_piece_color(board)
    draw_new_preview(preview_move, board)

    print "game reset"




def reset_turn():
    '''Resets the turn after animation is finished'''
    global game_state, anim_state
    #check for win
    if board.is_winner():
        draw_winning_connection(board)

        if board.get_winning_connection()[0] == 2:
            play_victory_sound()
        else:
            play_gameover_sound()


        game_state = GAME_STATE['END_SCREEN']
        return

    elif board.is_tie():
        play_gameover_sound()
        game_state = GAME_STATE['END_SCREEN']
        return

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





#----------------------------------- End Game Screen -----------------------------------
def handle_button_action():
    '''Does action depending on GUI_STATE'''
    global gui_state, game_state, running

    if gui_state == GUI_STATE['RESTART']:
        game_state = GAME_STATE['ANIMATION']
        anim_state = ANIM_STATE['SCREEN_RESET']
    else:
        running = False



def handle_button_press():
    '''Draws what is necessary with the new button press'''
    draw_pressed_button(gui_state)






#------------------------------------- Main Loop ---------------------------------------
#this way the preivew move is there at the start
draw_new_preview(preview_move, board)
running = True

def game_loop():
    '''The main game_loop'''
    #main game loop
    global preview_move, board, running

    reset_game()

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
            elif game_state == GAME_STATE['ANIMATION']:
                    if anim_state == ANIM_STATE['FALLING']:
                        #animations return True when they're done
                        if handle_falling_animation():
                            reset_turn()

                    elif anim_state == ANIM_STATE['CHOOSE']:
                        if handle_choose_animation():
                            #this sets it up for the falling animation
                            handle_move_logic()
           

            elif game_state == GAME_STATE['END_SCREEN']:
                return

            game_tick()	




def gui_loop():
    '''Handles the GUI pop up'''
    global running, board, gui_state

    #if the player x-ed out of the game
    if not running:
        return
    
    button_primed = False
    
    #assumed that coming in, the game just finished
    #still need to draw up GUI
    game_state = GAME_STATE['ANIMATION']
    anim_state = ANIM_STATE['GUI_DROPIN']
    set_dropin_animation_parameters(board)

    while running:
        #------------------ check events -----------
        for event in get_events():
                if event.type == EVENT_TYPE['QUIT']:
                        running = False
                        break
                
                elif event.type == EVENT_TYPE['KEYDOWN'] and not button_primed:
                        if event.key == INPUT_TYPE['LEFT']:
                            gui_state -= 1
                            gui_state %= 2
                            draw_endscreen(gui_state)

                        elif event.key == INPUT_TYPE['RIGHT']:
                            gui_state += 1
                            gui_state %= 2
                            draw_endscreen(gui_state)

                        elif event.key == INPUT_TYPE['SELECT']:
                            handle_button_press()
                            button_primed = True

                elif event.type == EVENT_TYPE['KEYUP'] and button_primed:
                        if event.key == INPUT_TYPE['SELECT']:
                            handle_button_action()
                            return



        #------------- GAME STATE ---------------
        #update based on game_state
        if game_state == GAME_STATE['ANIMATION']:
                if anim_state == ANIM_STATE['GUI_DROPIN']:
                    #animations return True when they're done
                    if handle_dropin_animation():
                        game_state = GAME_STATE['END_SCREEN']
                        anim_state = ANIM_STATE['NONE']

        elif game_state == GAME_STATE['END_SCREEN']:
            pass
       
        game_tick()




def __main__():
    '''Puts the game loop together with the actual gui display'''
    while running:
        game_loop()

        if running:
            gui_loop()



__main__()

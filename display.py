import pygame
from pygame import mixer

mixer.pre_init(44100, -16, 1, 512)
pygame.init()

#window info
SCALE_FACTOR = 6
SCREEN_WIDTH = 160 * SCALE_FACTOR // 1 #//1 = floor function
SCREEN_HEIGHT = 120 * SCALE_FACTOR // 1
pygame.display.set_caption("Connect 4 AI")
ICON = pygame.image.load("img/piece/red_piece.png")
pygame.display.set_icon(ICON)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()




#------------------------------ SFX / MUSIC ----------------------
#currently no music
hit_sound = mixer.Sound("snd/hit.wav")
quiet_hit_sound = mixer.Sound("snd/hit_quiet.wav")
victory_sound = mixer.Sound("snd/victory.wav")
game_over_sound = mixer.Sound("snd/game_over.wav")




#----------------------------- GAME IMAGES --------------------------------
#these come from the image, representing the x,y of the top left of the gameboard
BOARD_X = 22 * SCALE_FACTOR
BOARD_Y = 21 * SCALE_FACTOR
CHIP_SIZE = 16 * SCALE_FACTOR
#distance (px) between the top of the board and the preview piece
PREVIEW_PADDING = -3 * SCALE_FACTOR


#load images
BG_IMG    = pygame.image.load("img/wall.png")
BOARD_IMG = pygame.image.load("img/gameboard.png")

PLAYER_GHOST_IMG = pygame.image.load("img/piece/ghost_red_piece.png")
PLAYER_PIECE_IMG = pygame.image.load("img/piece/red_piece.png")
AI_PIECE_IMG     = pygame.image.load("img/piece/yel_piece.png")
AI_GHOST_IMG     = pygame.image.load("img/piece/ghost_yel_piece.png")

CROSS_HORIZ = pygame.image.load("img/cross/cross_horiz.png")
CROSS_VERT  = pygame.image.load("img/cross/cross_vert.png") 
CROSS_NW    = pygame.image.load("img/cross/cross_diag_nw.png")
CROSS_NE    = pygame.image.load("img/cross/cross_diag_ne.png") 

#scaling the images up
BG_IMG    = pygame.transform.scale(BG_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
BOARD_IMG = pygame.transform.scale(BOARD_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
#image size of 16x16 assumed for the pieces
PLAYER_PIECE_IMG = pygame.transform.scale(PLAYER_PIECE_IMG, (CHIP_SIZE, CHIP_SIZE)) 
PLAYER_GHOST_IMG = pygame.transform.scale(PLAYER_GHOST_IMG, (CHIP_SIZE, CHIP_SIZE))
AI_PIECE_IMG     = pygame.transform.scale(AI_PIECE_IMG,  (CHIP_SIZE, CHIP_SIZE))
AI_GHOST_IMG     = pygame.transform.scale(AI_GHOST_IMG, (CHIP_SIZE, CHIP_SIZE))

CROSS_HORIZ = pygame.transform.scale(CROSS_HORIZ, (CHIP_SIZE, CHIP_SIZE))
CROSS_VERT  = pygame.transform.scale(CROSS_VERT, (CHIP_SIZE, CHIP_SIZE))
CROSS_NW    = pygame.transform.scale(CROSS_NW, (CHIP_SIZE, CHIP_SIZE))
CROSS_NE    = pygame.transform.scale(CROSS_NE, (CHIP_SIZE, CHIP_SIZE))




#--------------------------- GUI Images -----------------------
#These magic numbers come right from the files
BUTTON_SIZE = (36 * SCALE_FACTOR, 34 * SCALE_FACTOR)
BUT_RESTART_POS = (29 * SCALE_FACTOR, 49 * SCALE_FACTOR)
BUT_QUIT_POS = (89 * SCALE_FACTOR , 49 * SCALE_FACTOR)

#load up these bad bois
RESTART_DESELECT_IMG = pygame.image.load("img/gui/restart_deselected.png")
RESTART_SELECT_IMG   = pygame.image.load("img/gui/restart_selected.png")
RESTART_PRESS_IMG    = pygame.image.load("img/gui/restart_pushed.png")
QUIT_DESELECT_IMG    = pygame.image.load("img/gui/quit_deselected.png")
QUIT_SELECT_IMG      = pygame.image.load("img/gui/quit_selected.png")
QUIT_PRESS_IMG       = pygame.image.load("img/gui/quit_pushed.png")

#scale these bad bois up
RESTART_DESELECT_IMG = pygame.transform.scale(RESTART_DESELECT_IMG, BUTTON_SIZE)
RESTART_SELECT_IMG   = pygame.transform.scale(RESTART_SELECT_IMG, BUTTON_SIZE)
RESTART_PRESS_IMG    = pygame.transform.scale(RESTART_PRESS_IMG, BUTTON_SIZE)
QUIT_DESELECT_IMG    = pygame.transform.scale(QUIT_DESELECT_IMG, BUTTON_SIZE)
QUIT_SELECT_IMG      = pygame.transform.scale(QUIT_SELECT_IMG, BUTTON_SIZE)
QUIT_PRESS_IMG       = pygame.transform.scale(QUIT_PRESS_IMG, BUTTON_SIZE)






#--------------------------- Globals ------------------------------
FPS = 60

#used by main.py, which does not import pygame
EVENT_TYPE = {
        "QUIT": pygame.QUIT,
        "KEYDOWN": pygame.KEYDOWN,
        "KEYUP": pygame.KEYUP
}

INPUT_TYPE = {
	"LEFT": pygame.K_LEFT,
	"RIGHT": pygame.K_RIGHT,
	"SELECT": pygame.K_DOWN
}










#--------------------- Flow Control / Coupling with main.py -----------
def game_tick():
    '''Updates the display, and adds a moment of delay'''
    pygame.display.update()
    clock.tick(FPS)

def get_events():
    '''Returns all current pygame events'''
    return pygame.event.get()



#------------------------ Basic Audio Hits
def play_victory_sound():
    '''Literally just plays the victory sound effect'''
    victory_sound.play()

def play_gameover_sound():
    '''Plays the game over sound'''
    game_over_sound.play()



#--------------------------- Basic Drawing Functions ---------------------------------
def draw_blank_game():
    '''Will cover the entire screen with a blank game'''
    screen.blit(BG_IMG, (0,0))
    screen.blit(BOARD_IMG, (0,0))


#all x,y are in pixel space
def draw_piece_over(pos, img, img_area = (CHIP_SIZE, CHIP_SIZE)):
    '''Draws img at pos without clearing it. Assumes img is CHIP_SIZE x CHIP_SIZE'''
    global screen

    board_area = pos + img_area
    screen.blit(img, pos)


def draw_piece(pos, chip):
	'''Draws a piece on the board. pos is a (px_x, px_y) Visually overwrites any piece that was in the location. Assumes chip is an image of CHIP_SIZE x CHIP_SIZE dimensiom'''
	global screen
	
	# the area that the chip takes up on the board, (x, y, width, height)
	board_area = pos + (CHIP_SIZE, CHIP_SIZE)

	#the piece gets sandwhiched between the bg and board
	screen.blit(BG_IMG, pos, board_area)
	screen.blit(chip, pos) #no area specified because we're drawing the entire image
	screen.blit(BOARD_IMG, pos, board_area)


def clear_piece(pos, area = (CHIP_SIZE, CHIP_SIZE)):
	'''Clears a piece on the board, but only visually. pos is a (px_x, px_y)'''
	global screen
	board_area = pos + area
	
	screen.blit(BG_IMG, pos, board_area)
	screen.blit(BOARD_IMG, pos, board_area)


#utility draw functions
def get_px_cords(x, y, y_px_offset = 0):
	'''Returns a (px_x, px_y) pair representing the top left of the square (x,y) on the board. (0,0) is top left'''
	return (BOARD_X + x*CHIP_SIZE,
                BOARD_Y + y*CHIP_SIZE + y_px_offset)


def get_board_cords(px_x, px_y):
	'''Converts pixel cords to game board cords. Will return negatives'''
        #// 1 is a floor operator (integer division)
	return ((px_x - BOARD_X) / CHIP_SIZE // 1, 
			(px_y - BOARD_Y) / CHIP_SIZE // 1)




#-------------------- Game-Related Drawing Commands -----------------------
preview_move = 0

cur_piece_img = PLAYER_PIECE_IMG
cur_ghost_img = PLAYER_GHOST_IMG


def set_piece_color(board):
    '''Sets the current color to match that of the board'''
    global cur_piece_img, cur_ghost_img

    player_turn = not board.is_comp_turn()

    if player_turn and cur_piece_img != PLAYER_PIECE_IMG:
        switch_color()
    elif not player_turn and cur_piece_img == PLAYER_PIECE_IMG:
        switch_color()


def switch_color():
        '''Swaps the current image to be the other image'''
        global cur_piece_img, cur_ghost_img
        if cur_piece_img == PLAYER_PIECE_IMG:
            cur_piece_img = AI_PIECE_IMG
            cur_ghost_img = AI_GHOST_IMG
        else:
            cur_piece_img = PLAYER_PIECE_IMG
            cur_ghost_img = PLAYER_GHOST_IMG


def draw_new_preview(new_preview_move, board, draw_ghost = True):
	'''Will update visuals to match the new state. new_preview_move is automatically clamped (%= 7)'''
	global PREVIEW_PADDING, preview_move

	#clamping for 0-6
	new_preview_move %= 7
	
	#clear the current ghost and preview piece
	ghost_height = board.empty_slots_in_col(preview_move) - 1
        if ghost_height > -1:
            clear_piece(get_px_cords(preview_move, ghost_height))
	clear_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING))
	
	#draw new preview piece
	preview_move = new_preview_move
	draw_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING), cur_piece_img)

        if draw_ghost:
            #this check needs to happen again because it's a new column
            ghost_height = board.empty_slots_in_col(preview_move) - 1	
            if ghost_height > -1:   
                 draw_piece(get_px_cords(preview_move, ghost_height), cur_ghost_img)


def draw_winning_connection(board):
    '''Draws the winning connection onto the display'''
    if not board.is_winner():
        return

    winner = board.get_winning_connection()
    #discard info about who won
    winner = winner[1:]
    win_dir = [winner[0][0] - winner[1][0], winner[0][1] - winner[1][1]]

    cross_img = CROSS_NW
    #con_dir could be the negative version of a dir, hence the or
    if win_dir == [0, 1] or win_dir == [0, -1]:
        cross_img = CROSS_VERT
    elif win_dir == [1, 0] or win_dir == [-1, 0]:
        cross_img = CROSS_HORIZ
    elif win_dir == [1, 1] or win_dir == [-1, -1]:
        cross_img = CROSS_NE

    #actually draw the bad bois
    for cord in winner:
        cur_cord = get_px_cords(cord[0], 5 - cord[1]) 
        draw_piece_over(cur_cord, cross_img) 


def draw_square_of_pieces(board, pos, width, height):
    '''Draws pieces on the board in a square of size size, touching empty places too. pos is in board space.'''
    cords = []

    for col in range(width):
        x = pos[0] + col
        for row in range(height):
            y = pos[1] + row

            cords += [[x, y]]

    #now actually draw those bad bois
    for cord in cords:
        piece = 0

        if cord[0] < 0 or cord[0] >= len(board.board_state[0]):
            piece = 3
        elif cord[1] < 0 or cord[1] >= len(board.board_state):
            piece = 3
        else:
            piece = board.board_state[5 - cord[1]][cord[0]]

        if piece == 0 or piece == 3:
            clear_piece(get_px_cords(cord[0], cord[1]))
            continue

        cur_piece = PLAYER_PIECE_IMG
        if piece == 1:
            cur_piece = AI_PIECE_IMG

        draw_piece(get_px_cords(cord[0], cord[1]), cur_piece)




#------------------------- GUI Drawing Commands --------------------------
def draw_endscreen(new_selection, y_pos = BUT_RESTART_POS[1]):
    '''Draws/updates the endscreen gui to match the new selection'''
    new_selection %= 2
    
    #making the selected image different 
    res_img = RESTART_DESELECT_IMG
    quit_img = QUIT_DESELECT_IMG

    if new_selection == 0:
        res_img = RESTART_SELECT_IMG
    elif new_selection == 1:
        quit_img = QUIT_SELECT_IMG
   

    #now lets draw these mfs
    res_pos = (BUT_RESTART_POS[0], y_pos)
    quit_pos = (BUT_QUIT_POS[0], y_pos)
    draw_piece_over(res_pos, res_img, BUTTON_SIZE)
    draw_piece_over(quit_pos, quit_img, BUTTON_SIZE)


def draw_pressed_button(button): 
    '''Pushes down a button. 0 = Restart, 1 = Quit''' 
    butt_img = RESTART_PRESS_IMG
    img_pos = BUT_RESTART_POS
    if button == 1:
        butt_img = QUIT_PRESS_IMG 
        img_pos = BUT_QUIT_POS

    draw_piece_over(img_pos, butt_img, BUTTON_SIZE)














#-------------------------------------------------------------------------
#                                Animations
#-------------------------------------------------------------------------

#--------------------------------- GUI Drop-In Animation ----------------------------
#exactly the same as the falling animation, just diff num bounces, image, and the board behind needs to be redrawn a lot
#gravity is a lil bigger because there's usually more lag with this
DROP_GRAVITY = 22 * SCALE_FACTOR
DROP_NUM_BOUNCES = 3
DROP_BOUNCE_COEF = -0.4
dropin_anim = {
	"y_pos": 0,
	"y_dest": BUT_RESTART_POS[1],
	"y_vel": -35 * SCALE_FACTOR,
	"Y_ACCEL": DROP_GRAVITY * (1.0 / FPS),
	"bounce": 0,
        "board": None
}



def set_dropin_animation_parameters(board):
        '''Sets up the animation for GUI pieces to drop in'''
	global dropin_anim
        
        #always start the same
	dropin_anim['y_pos'] = -BUTTON_SIZE[1] - 10
        dropin_anim['y_dest'] = BUT_RESTART_POS[1]
        #the negative adds some delay before it shows itself
	dropin_anim['y_vel'] = -5 * SCALE_FACTOR
        dropin_anim['bounce'] = 0
        dropin_anim['board'] = board


def handle_dropin_animation():
	'''Will draw and update values relating to a falling piece'''
	global dropin_anim
        finished = False
	
        dropin_anim['y_vel'] += dropin_anim['Y_ACCEL']
	dropin_anim['y_pos'] += int(dropin_anim['y_vel'])
	
	#check if it has reached the target y yet
	if dropin_anim['y_dest'] <= dropin_anim['y_pos']:
		#this way it isn't below the line
		dropin_anim['y_pos'] = dropin_anim['y_dest']

                #sound playing
                if dropin_anim['bounce'] == 0:
                    hit_sound.play()
                else:
                    quiet_hit_sound.play()

		#bouncing behaviour
		if dropin_anim['bounce'] + 1 >= DROP_NUM_BOUNCES:
			finish_dropin_animation()
                        finished = True
		

                dropin_anim['bounce'] += 1
                #reverse dir and lose some speed
                dropin_anim['y_vel'] *= DROP_BOUNCE_COEF


        #redraw the pieces and the winning connection, then the GUI
        res_pos = get_board_cords(BUT_RESTART_POS[0], dropin_anim['y_pos'])
        quit_pos = get_board_cords(BUT_QUIT_POS[0], dropin_anim['y_pos'])

        res_pos = (res_pos[0], res_pos[1] - 1)
        quit_pos = (quit_pos[0], quit_pos[1] - 1)

        draw_square_of_pieces(dropin_anim['board'], res_pos, 3, 4)
        draw_square_of_pieces(dropin_anim['board'], quit_pos, 3, 4)
        draw_winning_connection(dropin_anim['board'])

        draw_endscreen(0, dropin_anim['y_pos'])
        return finished
		


def finish_dropin_animation():
	'''Wraps up the falling animation, redrawing what's necessary'''
        pass




#--------------------------------- AI Choosing Animation ---------------------
#Moves the preview piece back and forth so it looks like a choice is being made
FRAMES_PER_MOVE = 15 #so it's not instant side to side
choose_anim = {
        "dest": 0,
        "dir": 1,
        "frame": 0
}


def set_choose_animation_parameters(destination):
    '''Sets all parameters relating to the choosing animation'''
    global choose_anim

    choose_anim['dest'] = destination
    
    choose_anim['dir'] = 1
    if destination - preview_move < 0:
        choose_anim['dir'] = -1
    elif destination - preview_move == 0:
        choose_anim['dir'] = 0
    
    choose_anim['frame'] = 0


def handle_choose_animation():
    '''Moves one frame forward in the choosing animation'''
    global choose_anim
    choose_anim['frame'] += 1

    if choose_anim['frame'] >= FRAMES_PER_MOVE:
        global preview_move
        choose_anim['frame'] = 0
        
        if preview_move == choose_anim['dest']:
            finish_choose_animation()
            return True
        
        #this will look very similar to draw_new_preview(..)
        clear_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING))
        preview_move += choose_anim['dir']
        preview_move %= 7
        draw_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING), cur_piece_img)
       

    return False



def finish_choose_animation():
    '''Resets choose_anim parameters for next time'''
    #all params (A/O now) are set with set_choose_animation()
    #so none need to be reset
    pass





#--------------------------------- Falling Animation ----------------------------
GRAVITY = 20 * SCALE_FACTOR
NUM_BOUNCES = 2
BOUNCE_COEF = -0.3
fall_anim = {
	"pos": (0, 0),
	"dest": (0, 0),
	"y_vel": 0,
	"Y_ACCEL": GRAVITY * (1.0 / FPS),
	"bounce": 0,
	"img": PLAYER_PIECE_IMG,
}



def set_falling_animation_parameters(board):
	global fall_anim

        #with each call, it will switch
        fall_anim['img'] = cur_piece_img
	fall_anim['pos'] = get_px_cords(preview_move, -1, PREVIEW_PADDING)
	fall_anim['y_vel'] = 0
	
	#set to just be the bottom of the board
	fall_anim['dest'] = get_px_cords(preview_move, board.empty_slots_in_col(preview_move) - 1)

        fall_anim['bounce'] = 0



def handle_falling_animation():
	'''Will draw and update values relating to a falling piece'''
	global fall_anim
        finished = False
	
	clear_piece(tuple(fall_anim['pos']))
	fall_anim['pos'] = list(fall_anim['pos'])
	
        fall_anim['y_vel'] += fall_anim['Y_ACCEL']
	fall_anim['pos'][1] += fall_anim['y_vel']
	
	#check if it has reached the target y yet
	if fall_anim['dest'][1] <= fall_anim['pos'][1]:
		#this way it isn't below the line
		fall_anim['pos'][1] = fall_anim['dest'][1]

                #sound playing
                if fall_anim['bounce'] == 0:
                    hit_sound.play()
                else:
                    quiet_hit_sound.play()

		#bouncing behaviour
		if fall_anim['bounce'] + 1 >= NUM_BOUNCES:
			finish_falling_animation()
                        finished = True
		

                fall_anim['bounce'] += 1
                #reverse dir and lose some speed
                fall_anim['y_vel'] *= BOUNCE_COEF


        #redraw
        fall_anim['pos'] = tuple(fall_anim['pos'])
        draw_piece(fall_anim['pos'], fall_anim['img'])

        return finished
		


def finish_falling_animation():
	'''Wraps up the falling animation, redrawing what's necessary'''
        #reset for next time	
	fall_anim['bounce'] = 0































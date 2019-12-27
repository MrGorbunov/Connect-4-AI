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
RESTART_IN_IMG  = pygame.image.load("img/gui/restart_in.png")
RESTART_OUT_IMG = pygame.image.load("img/gui/restart_out.png")
QUIT_IN_IMG     = pygame.image.load("img/gui/quit_in.png")
QUIT_OUT_IMG    = pygame.image.load("img/gui/quit_out.png")

#scale these bad bois up
RESTART_IN_IMG  = pygame.transform.scale(RESTART_IN_IMG, BUTTON_SIZE)
RESTART_OUT_IMG = pygame.transform.scale(RESTART_OUT_IMG, BUTTON_SIZE)
QUIT_IN_IMG     = pygame.transform.scale(QUIT_IN_IMG, BUTTON_SIZE)
QUIT_OUT_IMG    = pygame.transform.scale(QUIT_OUT_IMG, BUTTON_SIZE)






#--------------------------- Globals ------------------------------
#draw BG => then later it just gets overwritten in specific places
screen.blit(BG_IMG, (0,0))
screen.blit(BOARD_IMG, (0,0))

FPS = 60

#used by main.py, which does not import pygame
EVENT_TYPE = {
        "QUIT": pygame.QUIT,
        "KEYDOWN": pygame.KEYDOWN
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



#--------------------------- Basic Drawing Functions ---------------------------------
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


def clear_piece(pos):
	'''Clears a piece on the board, but only visually. pos is a (px_x, px_y)'''
	global screen
	board_area = pos + (CHIP_SIZE, CHIP_SIZE)
	
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
    #first, get the winning connection
    winner = board.get_winning_connection()

    #determine direction, then image
    con_dir = [winner[1][0] - winner[2][0], winner[1][1] - winner[2][1]]
    cross_img = CROSS_NW

    #con_dir could be the negative version of a dir, hence the or
    if con_dir == [0, 1] or con_dir == [0, -1]:
        cross_img = CROSS_VERT
    elif con_dir == [1, 0] or con_dir == [-1, 0]:
        cross_img = CROSS_HORIZ
    elif con_dir == [1, 1] or con_dir == [-1, -1]:
        cross_img = CROSS_NE
    else:
        cross_img = CROSS_NW

    #actually draw the bad bois
    winner = winner[1:]
    for cord in winner:
        cur_cord = get_px_cords(cord[0], 5 - cord[1]) 
        draw_piece_over(cur_cord, cross_img) 




#------------------------- GUI Drawing Commands --------------------------
def draw_endscreen(new_selection):
    '''Draws/updates the endscreen gui to match the new selection'''
    new_selection %= 2
    
    #making the selected image different 
    res_img = RESTART_OUT_IMG
    quit_img = QUIT_OUT_IMG

    if new_selection == 0:
        res_img = RESTART_IN_IMG
    elif new_selection == 1:
        quit_img = QUIT_IN_IMG
   

    #now lets draw these mfs
    draw_piece_over(BUT_RESTART_POS, res_img, BUTTON_SIZE)
    draw_piece_over(BUT_QUIT_POS, quit_img, BUTTON_SIZE)

















#-------------------------------------------------------------------------
#                                Animations
#-------------------------------------------------------------------------



#--------------------------------- GUI Drop-In Animation  ---------------------
SPEED = FPS // 2 #frames for whole animation
#path is fast drop
#over shoot by a little
#come back to rest
dropin_anim = {
        "over_shoot": 5 * SCALE_FACTOR,
        "cur_pos": 0
}


def set_dropin_animation_parameters(destination):
    '''Sets all parameters relating to the gui dropin animation'''
    pass

def handle_dropin_animation():
    '''Moves one frame forward in the gui dropin animation'''
    return False



def finish_dropin_animation():
    '''Resets gui dropin parameters for next time'''
    #all params (A/O now) are set with set_choose_animation()
    #so none need to be reset
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



def handle_falling_animation():
	'''Will draw and update values relating to a falling piece'''
	global fall_anim
	
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

                        #redraw
                        fall_anim['pos'] = tuple(fall_anim['pos'])
                        draw_piece(fall_anim['pos'], fall_anim['img'])

                        return True 
		

                fall_anim['bounce'] += 1
                #reverse dir and lose some speed
                fall_anim['y_vel'] *= BOUNCE_COEF


        #redraw
        fall_anim['pos'] = tuple(fall_anim['pos'])
        draw_piece(fall_anim['pos'], fall_anim['img'])

        return False
		


def finish_falling_animation():
	'''Wraps up the falling animation, redrawing what's necessary'''
        #reset for next time	
	fall_anim['bounce'] = 0































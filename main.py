'''
Connect 4 AI

Controls sounds and the GUI display, made in pygame

Michael Gorbunov
11/29/19 - 
'''

'''
TODO
-Create classes for data chunks
-Require almost 0 parameters with most functions
-Adapt to work with Dennis' gamestate
-Add input from buttons
-Split multiple files

-SFX
'''

from enum import IntEnum
import pygame

pygame.init()


#window info
SCALE_FACTOR = 6
SCREEN_WIDTH = 160 * SCALE_FACTOR // 1 #//1 = floor function
SCREEN_HEIGHT = 120 * SCALE_FACTOR // 1
pygame.display.set_caption("Connect 4 AI")
ICON = pygame.image.load("img/red_piece.png")
pygame.display.set_icon(ICON)

#global pygame stuff
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


#loading all images
BG_IMG    = pygame.image.load("img/wall.png")
BOARD_IMG = pygame.image.load("img/gameboard.png")
RED_CHIP  = pygame.image.load("img/red_piece.png")
RED_GHOST = pygame.image.load("img/ghost_red_piece.png")
YEL_CHIP  = pygame.image.load("img/yel_piece.png")
YEL_GHOST = pygame.image.load("img/ghost_yel_piece.png")

#these come from the image, representing the x,y of the top left
BOARD_X = 22 * SCALE_FACTOR
BOARD_Y = 21 * SCALE_FACTOR
CHIP_SIZE = 16 * SCALE_FACTOR

#scaling the images up
BG_IMG    = pygame.transform.scale(BG_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
BOARD_IMG = pygame.transform.scale(BOARD_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
#image size of 16x16 assumed
RED_CHIP  = pygame.transform.scale(RED_CHIP,  (CHIP_SIZE, CHIP_SIZE)) 
RED_GHOST = pygame.transform.scale(RED_GHOST, (CHIP_SIZE, CHIP_SIZE))
YEL_CHIP  = pygame.transform.scale(YEL_CHIP,  (CHIP_SIZE, CHIP_SIZE))
YEL_GHOST = pygame.transform.scale(YEL_GHOST, (CHIP_SIZE, CHIP_SIZE))

#draw BG
screen.blit(BG_IMG, (0,0))
screen.blit(BOARD_IMG, (0,0))







#-------------------------------------- Game Setup -----------------------------
#used to act based on current situation
class GameState(IntEnum):
	PLAYER_MOVE = 0
	AI_MOVE = 1
	ANIMATION = 2

#this way we're always dealing with ints but its readable as text
class BoardPiece(IntEnum):
	EMPTY = 0
	RED = 1
	YELLOW = 2

#stores what input comes from what keys
class InputType:
	LEFT   = pygame.K_LEFT
	RIGHT  = pygame.K_RIGHT
	SELECT = pygame.K_DOWN
	HOME   = pygame.K_SPACE

game_state = GameState.PLAYER_MOVE

preview_move = 0 #which row the current move is planned to be in

player_turn  = True

PLAYER_PIECE = BoardPiece.RED
PLAYER_CHIP  = RED_CHIP
PLAYER_GHOST = RED_GHOST

AI_PIECE = BoardPiece.YELLOW
AI_CHIP = YEL_CHIP
AI_GHOST = YEL_GHOST


#distance (in px) between top of board and preview piece. positive is up
PREVIEW_PADDING = -3 * SCALE_FACTOR

FPS = 60

#these track the piece that has just been dropped so as to animate it
anim_piece_pos = (0, 0)
anim_piece_y_vel = 0
anim_piece_img = RED_CHIP
anim_piece_destination = (0, 0)
bounces = 0
GRAVITY = 20 * SCALE_FACTOR
ACCEL_Y = GRAVITY * (1.0 / FPS)


#setup the board
board = () #board[0][0] = top left, [6][5] = bot right
for col in range(8):
	cur_row = ()
	for row in range(7):
		cur_row += (BoardPiece.EMPTY,)
	board += (cur_row,)








#--------------------------- Basic Drawing Functions ---------------------------------
#all x,y are in pixel space
def draw_piece(pos, chip):
	'''Draws a piece on the board. pos is a (px_x, px_y) Visually overwrites any piece that was in the location. Assumes chip is an image of CHIP_SIZE x CHIP_SIZE dimensiom'''
	global board, screen
	
	pos
	# the area that the chip takes up on the board, (x, y, width, height)
	board_area = pos + (CHIP_SIZE, CHIP_SIZE)

	#the piece gets sandwhiched between the bg and board
	screen.blit(BG_IMG, pos, board_area)
	screen.blit(chip, pos) #no area specified because we're drawing the entire image
	screen.blit(BOARD_IMG, pos, board_area)


def clear_piece(pos):
	'''Clears a piece on the board, but only visually. pos is a (px_x, px_y)'''
	global board, screen

	board_area = pos + (CHIP_SIZE, CHIP_SIZE)
	
	screen.blit(BG_IMG, pos, board_area)
	screen.blit(BOARD_IMG, pos, board_area)




#utility draw functions
def get_px_cords(x, y, y_px_offset = 0):
	'''Returns a (px_x, px_y) pair representing the top left of the square (x,y) on the board. (0,0) is top left'''
	return (BOARD_X + x*CHIP_SIZE, BOARD_Y + y*CHIP_SIZE + y_px_offset)


def get_board_cords(px_x, px_y):
	'''Converts pixel cords to game board cords. Will return negatives'''
	return ((px_x - BOARD_X) / CHIP_SIZE // 1, 
			(px_y - BOARD_Y) / CHIP_SIZE // 1)








#----------------------------- Coupled Drawing Commands ----------------------------------
def handle_move_preview_input(chip, ghost, goingLeft):
	'''Will adjust preview_move and update visuals to match the new state. pos is a (px_x, px_y)'''
	global preview_move, PREVIEW_PADDING

	#clear the current ghost and preview piece
	clear_piece(get_px_cords(preview_move, 5))
	clear_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING))
	
	if goingLeft:
		preview_move -= 1
	else:
		preview_move += 1
	#keeps in range 0-6
	preview_move %= 7
	
	#preview piece, is above the board
	draw_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING), chip)
	draw_piece(get_px_cords(preview_move, 5), ghost)


def handle_falling_animation():
	'''Will draw and update values relating to a falling piece'''
	global anim_piece_pos, anim_piece_y_vel, anim_piece_img, anim_piece_destination
	global ACCEL_Y, bounces
	
	#clear where the piece might've been last frame
	clear_piece(anim_piece_pos)
	
	#compute physics
	anim_piece_pos = list(anim_piece_pos)
	
	anim_piece_y_vel += ACCEL_Y
	anim_piece_pos[1] += anim_piece_y_vel
	
	#check if it has reached the target y yet
	if anim_piece_destination[1] <= anim_piece_pos[1]:
		anim_piece_pos[1] = anim_piece_destination[1]
	
		#this makes it bounce twice
		if bounces > 1:
			global game_state
			game_state = GameState.PLAYER_MOVE
			bounces = 0
		else:
			bounces += 1
			#reverse dir and lose some speed
			anim_piece_y_vel *= -0.4
		
	#redraw
	anim_piece_pos = tuple(anim_piece_pos)
	draw_piece(anim_piece_pos, anim_piece_img)
	


def set_falling_animation_parameters():
	'''Sets all parameters relating to a falling animation. Assumes this is being called when a piece is at the top (just after preview piece)'''
	global anim_piece_pos, anim_piece_y_vel, anim_piece_img, anim_piece_destination
	global game_state
	
	game_state = GameState.ANIMATION
	
	if player_turn:
		anim_piece_img = PLAYER_CHIP
	else:
		anim_piece_img = AI_CHIP
	
	anim_piece_pos = get_px_cords(preview_move, -1, PREVIEW_PADDING)
	anim_piece_y_vel = 0
	
	#set to just be the bottom of the board
	anim_piece_destination = get_px_cords(preview_move, 5)
	
	








#------------------------------------- Main Loop ---------------------------------------

#draw the important stuff just once, then the screen gets selectively updated
screen.blit(BG_IMG, (0,0))
screen.blit(BOARD_IMG, (0,0))
pygame.display.update()


#main game loop
running = True
while running:
	#check events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			break
		
		
		#doesn't listen to input, but still allows for closing the window
		if game_state == GameState.ANIMATION:
			break
		
		
		#something pressed
		if event.type == pygame.KEYDOWN:
			if event.key == InputType.LEFT:
				handle_move_preview_input(PLAYER_CHIP, PLAYER_GHOST, goingLeft=True)
				
			elif event.key == InputType.RIGHT:
				handle_move_preview_input(PLAYER_CHIP, PLAYER_GHOST, goingLeft=False)

			elif event.key == InputType.SELECT:
				#choosing to drop a piece
				set_falling_animation_parameters()
				break
				
			elif event.key == InputType.HOME:
				print("home")
	
	
	#update based on game_state
	if game_state == GameState.ANIMATION:
		handle_falling_animation()
	
	pygame.display.update()
	clock.tick(FPS)



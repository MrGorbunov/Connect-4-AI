'''
Connect 4 AI

Controls sounds and the GUI display, made in pygame

Michael Gorbunov
11/29/19 - 
'''


from enum import IntEnum
from boardclass import Board
import pygame




#-------------------------------------- PyGame / Image Globals -----------------------------
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

#these come from the image, representing the x,y of the top left of the gameboard
BOARD_X = 22 * SCALE_FACTOR
BOARD_Y = 21 * SCALE_FACTOR
CHIP_SIZE = 16 * SCALE_FACTOR
#distance (px) between the top of the board and the preview piece
PREVIEW_PADDING = -3 * SCALE_FACTOR

PLAYER_GHOST_IMG = pygame.image.load("img/ghost_red_piece.png")
PLAYER_PIECE_IMG = pygame.image.load("img/red_piece.png")
AI_PIECE_IMG     = pygame.image.load("img/yel_piece.png")
AI_GHOST_IMG     = pygame.image.load("img/ghost_yel_piece.png")


#scaling the images up
BG_IMG    = pygame.transform.scale(BG_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
BOARD_IMG = pygame.transform.scale(BOARD_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))
#image size of 16x16 assumed for the pieces
PLAYER_PIECE_IMG = pygame.transform.scale(PLAYER_PIECE_IMG,  (CHIP_SIZE, CHIP_SIZE)) 
PLAYER_GHOST_IMG = pygame.transform.scale(PLAYER_GHOST_IMG, (CHIP_SIZE, CHIP_SIZE))
AI_PIECE_IMG     = pygame.transform.scale(AI_PIECE_IMG,  (CHIP_SIZE, CHIP_SIZE))
AI_GHOST_IMG     = pygame.transform.scale(AI_GHOST_IMG, (CHIP_SIZE, CHIP_SIZE))

#draw BG => then later it just gets overwritten in specific places
screen.blit(BG_IMG, (0,0))
screen.blit(BOARD_IMG, (0,0))








#-------------------------------------- Animation & Game Globals -----------------------------
#used to act based on current situation
GAME_STATE = {
	"PLAYER_MOVE": 0,
	"AI_MOVE": 1,
	"ANIMATION": 2
}

#stores what input type comes from what keys
INPUT_TYPE = {
	"LEFT": pygame.K_LEFT,
	"RIGHT": pygame.K_RIGHT,
	"SELECT": pygame.K_DOWN
}

game_state = GAME_STATE['PLAYER_MOVE']
preview_move = 0 #which row the current move is planned to be in


#these track the piece that has just been dropped so as to animate it
GRAVITY = 20 * SCALE_FACTOR
FPS = 60

#amount of times it should bounce
fall_anim = {
	"pos": (0, 0),
	"dest": (0, 0),
	"y_vel": 0,
	"Y_ACCEL": GRAVITY * (1.0 / FPS),
	"bounce": 0,
	"img": PLAYER_PIECE_IMG,
}
NUM_BOUNCES = 2
BOUNCE_COEF = -0.3


#setup the board
board = Board()

#Ideally these wouldn't be here
cur_piece_img = PLAYER_PIECE_IMG
cur_ghost_img = PLAYER_GHOST_IMG

#start with player
if board.isCompTurn():
	board.changeTurn()




#--------------------------- Basic Drawing Functions ---------------------------------
#all x,y are in pixel space
def draw_piece(pos, chip):
	'''Draws a piece on the board. pos is a (px_x, px_y) Visually overwrites any piece that was in the location. Assumes chip is an image of CHIP_SIZE x CHIP_SIZE dimensiom'''
	global board, screen
	
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
def handle_move_preview_input(new_preview_move):
	'''Will update visuals to match the new state. pos is a (px_x, px_y). new_preview_move is automatically clamped (%= 7)'''
	global PREVIEW_PADDING, preview_move

	#clamping for 0-6
	new_preview_move %= 7
	
	#clear the current ghost and preview piece
	ghost_height = board.empty_slots_in_col(preview_move) - 1
	clear_piece(get_px_cords(preview_move, ghost_height))
	clear_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING))
	
	#adjusting move
	preview_move = new_preview_move
	
	#preview piece, is above the board
	draw_piece(get_px_cords(preview_move, -1, PREVIEW_PADDING), cur_piece_img)
	#this check needs to happen again because it's a new column
	ghost_height = board.empty_slots_in_col(preview_move) - 1	
	draw_piece(get_px_cords(preview_move, ghost_height), cur_ghost_img)


def handle_falling_animation():
	'''Will draw and update values relating to a falling piece'''
	global fall_anim
	
	#clear where the piece might've been last frame
	clear_piece(fall_anim['pos'])
	
	#compute physics
	fall_anim['pos'] = list(fall_anim['pos'])
	
	fall_anim['y_vel'] += fall_anim['Y_ACCEL']
	fall_anim['pos'][1] += fall_anim['y_vel']
	
	#check if it has reached the target y yet
	if fall_anim['dest'][1] <= fall_anim['pos'][1]:
		#this way it isn't below the line
		fall_anim['pos'][1] = fall_anim['dest'][1]
	
		#bouncing behaviour
		if fall_anim['bounce'] + 1 >= NUM_BOUNCES:
			finish_fall_animation()
		else:
			fall_anim['bounce'] += 1
			#reverse dir and lose some speed
			fall_anim['y_vel'] *= BOUNCE_COEF
		
	#redraw
	fall_anim['pos'] = tuple(fall_anim['pos'])
	draw_piece(fall_anim['pos'], fall_anim['img'])


def finish_fall_animation():
	'''Wrap the falling animation, changing game_state and redrawing what's necessary'''
	global game_state
	
	game_state = GAME_STATE['PLAYER_MOVE']
	fall_anim['bounce'] = 0
	handle_move_preview_input(preview_move)

	#win check
	if board.isWinner():
		global running
		running = False
	
		for i in range(5):
			print("We have a winner!!!")

def set_falling_animation_parameters():
	'''Sets all parameters relating to a falling animation. Assumes this is being called when a piece is at the top (just after preview piece)'''
	global fall_anim, game_state
	global AI_PIECE_IMG, PLAYER_PIECE_IMG
	
	game_state = GAME_STATE['ANIMATION']
	
	#set current piece
	if board.isCompTurn():
		fall_anim['img'] = AI_PIECE_IMG
	else:
		fall_anim['img'] = PLAYER_PIECE_IMG
	
	fall_anim['pos'] = get_px_cords(preview_move, -1, PREVIEW_PADDING)
	fall_anim['y_vel'] = 0
	
	#set to just be the bottom of the board
	fall_anim['dest'] = get_px_cords(preview_move, board.empty_slots_in_col(preview_move) - 1)
	






#--------------------------------- Game Logic Commands --------------------------------	
def handle_move_logic():
	'''Updates the Board instance (board) and cur_images'''
	global cur_piece_img, cur_ghost_img
	board.editBoard(preview_move)
	board.changeTurn()
	
	if board.isCompTurn():
		cur_piece_img = AI_PIECE_IMG
		cur_ghost_img = AI_GHOST_IMG
	else:
		cur_piece_img = PLAYER_PIECE_IMG
		cur_ghost_img = PLAYER_GHOST_IMG
	








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
		if game_state == GAME_STATE['ANIMATION']:
			break
		
		
		#something pressed
		if event.type == pygame.KEYDOWN:
			if event.key == INPUT_TYPE['LEFT']:
				#clamping the new move is handled by the function
				handle_move_preview_input(preview_move - 1)
				
			elif event.key == INPUT_TYPE['RIGHT']:
				handle_move_preview_input(preview_move + 1)

			elif event.key == INPUT_TYPE['SELECT']:
				#choosing to drop a piece
				set_falling_animation_parameters()
				handle_move_logic()
				#so that anything else doesn't muck things up
				break
	
	
	#update based on game_state
	if game_state == GAME_STATE['ANIMATION']:
		handle_falling_animation()
	
	pygame.display.update()
	clock.tick(FPS)


#this way there's a delay and you can admire the victory
asd = input()

'''
Connect 4 AI

Controls sounds and the GUI display, made in pygame

Michael Gorbunov
11/29/19 - 
'''

'''
TODO
-Make functional
-Get into / onto github
-Adapt to work with Dennis' gamestate
-Add input from buttons
-Work with multiple files

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
icon = pygame.image.load("img/red_piece.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(icon)


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


#game logic
#this way we're always dealing with ints but its readable
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

player_move_preview = 0 #which row the current move is under
player_turn  = True
PLAYER_PIECE = BoardPiece.RED
PLAYER_CHIP  = RED_CHIP
PLAYER_GHOST = RED_GHOST

#setup the board
board = () #board[0][0] = top left, [6][5] = bot right
for col in range(8):
	cur_row = ()
	for row in range(7):
		cur_row += (BoardPiece.EMPTY,)
	board += (cur_row,)







#drawing functions
#all x,y are on the gameboard, not in pixels
def draw_piece(x, y, chip):
	'''Draws a piece on the board. Visually overwrites any piece that was in the location. ghosts can be used'''
	global board, screen

	start_cord = (BOARD_X + x*CHIP_SIZE, BOARD_Y + y*CHIP_SIZE)
	# the area that the chip takes up on the board, (x, y, width, height)
	board_area = start_cord + (CHIP_SIZE, CHIP_SIZE)
	
	#the piece gets sandwhiched between the bg and board
	screen.blit(BG_IMG, start_cord, board_area)
	screen.blit(chip, start_cord) #no area specified because we're drawing the entire image
	screen.blit(BOARD_IMG, start_cord, board_area)

def clear_drawn_piece(x, y):
	'''Clears a piece on the board, but only visually'''
	global board, screen

	start_cord = (BOARD_X + x*CHIP_SIZE, BOARD_Y + y*CHIP_SIZE)
	board_area = start_cord + (CHIP_SIZE, CHIP_SIZE)
	
	screen.blit(BG_IMG, start_cord, board_area)
	screen.blit(BOARD_IMG, start_cord, board_area)
	
def draw_preview_piece(chip):
	'''Draws a preview piece above the board in the col of player_mov. Automatically clears the whole preview-piece area'''
	global board, screen, player_move_preview
	
	start_y = BOARD_Y - CHIP_SIZE - (3) * SCALE_FACTOR #3 = padding amount

	#chip
	chip_start_cord = (BOARD_X + player_move_preview*CHIP_SIZE, start_y) #5 = padding
	
	#preview area
	preview_start_cord = (BOARD_X, start_y)
	preview_area = (BOARD_X, start_y, 7*CHIP_SIZE, CHIP_SIZE)
	
	screen.blit(BG_IMG, preview_start_cord, preview_area)
	screen.blit(chip, chip_start_cord)
	#this lines needs to be toggled on if the padding amoutn is less than 3
	# screen.blit(BOARD_IMG, preview_start_cord, preview_area)
	pass

def handle_move_preview_input(chip, ghost, goingLeft):
	'''Will adjust player_move_preview and update visuals to match the new state'''
	global player_move_preview
	
	#clear the current ghost
	clear_drawn_piece(player_move_preview, 5)
	
	if goingLeft:
		player_move_preview -= 1
		if player_move_preview < 0:
			player_move_preview = 6
	else:
		player_move_preview += 1
		if player_move_preview > 6:
			player_move_preview = 0
	
	draw_preview_piece(chip)
	draw_piece(player_move_preview, 5, ghost)

	
#draw the important stuff just once, and then the screen gets selectively updated
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
		
		#something pressed
		if event.type == pygame.KEYDOWN:
			if event.key == InputType.LEFT:
				handle_move_preview_input(PLAYER_CHIP, PLAYER_GHOST, True)
				pygame.display.update()
				
			elif event.key == InputType.RIGHT:
				handle_move_preview_input(PLAYER_CHIP, PLAYER_GHOST, False)
				pygame.display.update()

			elif event.key == InputType.SELECT:
				print("select")
			elif event.key == InputType.HOME:
				print("home")
		
	#draw call
	# running = False



# draw_piece(0, 5, RED_CHIP)
# draw_piece(1, 5, YEL_CHIP)
# draw_piece(0, 4, RED_CHIP)
# draw_piece(2, 5, YEL_CHIP)
# draw_piece(3, 5, RED_CHIP)
# pygame.display.update()
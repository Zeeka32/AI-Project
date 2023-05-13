import pygame
from utilities import *

ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

# settings and variables
width = COLUMNS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
game_over = False
turn = 0
size = (width, height)

def print_board(board):
    print(np.flip(board, 0))

board = np.zeros((ROWS,COLUMNS))
print_board(board)

pygame.init()

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("impact", 80)

draw_board(board, screen, ROWS, COLUMNS, SQUARESIZE, RADIUS, height)
pygame.display.update()


while not game_over:

    for event in pygame.event.get():

        update_mouse_movement(event, screen, SQUARESIZE, width, RADIUS, turn)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BACKGROUND_COLOR, (0,0, width, SQUARESIZE))

            # Player one's Turn
            if turn == 0:
                # remove event.pos[0] and replace it with the right value based on the AI's choice
                # 50 for COL0, 150 for COL1, 250 for COL3 and so on..
                x_position = event.pos[0]
                update_game_state(board, SQUARESIZE, ROWS, 1, x_position)
                game_over = check_game_state(board, ROWS, COLUMNS, 1, RED, myfont, "PLAYER 1 WINS!!", screen)
                turn += 1
                

			# Player two's turn
            else:
                # remove event.pos[0] and replace it with the right value based on the AI's choice
                # 50 for COL0, 150 for COL1, 250 for COL3 and so on..
                x_position = event.pos[0]
                update_game_state(board, SQUARESIZE, ROWS, 2, x_position)
                game_over = check_game_state(board, ROWS, COLUMNS, 2, YELLOW, myfont, "PLAYER 2 WINS!!", screen)
                turn -= 1

            print_board(board)
            draw_board(board, screen, ROWS, COLUMNS, SQUARESIZE, RADIUS, height)

            if game_over:
                pygame.time.wait(3000)
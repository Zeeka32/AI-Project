import pygame
import numpy as np
from utilities import *
from button import *

ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

# settings and variables
width = COLUMNS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE

def print_board(board):
    print(np.flip(board, 0))

pygame.init()

size = (width, height)

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("impact", 80)


def play():
    screen.fill(BACKGROUND_COLOR)
    pygame.display.set_caption("Connect 4")
    game_over = False
    turn = 0
    board = np.zeros((ROWS,COLUMNS))
    print_board(board)
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

def options():
    pass

def main_menu():
    pygame.display.set_caption("Main Menu")
    while True:
        
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0,0, width, SQUARESIZE))

        screen.fill(BACKGROUND_COLOR)

        MENU_MOUSE_POSITION = pygame.mouse.get_pos()

        MENU_TEXT = myfont.render("MAIN MENU", 1, WHITE)

        PLAY_BUTTON = Button(image=None, pos=(350, 250), text_input="PLAY", font=myfont, base_color=WHITE, hovering_color=GREY)
        OPTIONS_BUTTON = Button(image=None, pos=(350, 350), text_input="OPTIONS", font=myfont, base_color=WHITE, hovering_color=GREY)
        QUIT_BUTTON = Button(image=None, pos=(350, 450), text_input="QUIT", font=myfont, base_color=WHITE, hovering_color=GREY)

        screen.blit(MENU_TEXT, (170, 15))

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POSITION)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                    play()
                    pygame.display.set_caption("Main Menu")
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        

main_menu()
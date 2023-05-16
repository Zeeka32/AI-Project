import pygame
import numpy as np
import sys
from AI import *
from utilities import *
from button import *

ROWS = 6
COLUMNS = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
P1DIFFICULTY = 2
P2DIFFICULTY = 2

# settings and variables
width = COLUMNS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE

def print_board(board):
    print(np.flip(board, 0))

pygame.init()

size = (width, height)

screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont("impact", 80)

p1 = Player()
p1.set_algo(connect4_ai)

p2 = Player()
p2.set_algo(connect4_ai)


def play():

    pygame.display.set_caption("Connect 4")
    screen.fill(BACKGROUND_COLOR)

    AI = True
    game_over = False
    turn = 0
    board = np.zeros((ROWS,COLUMNS))
    print_board(board)
    draw_board(board, screen, ROWS, COLUMNS, SQUARESIZE, RADIUS, height)
    pygame.display.update()

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BACKGROUND_COLOR, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Player one's Turn
                if turn == 1:
                    x_position = event.pos[0]
                    valid = update_game_state(board, SQUARESIZE, ROWS, 2, x_position)
                    if valid:
                        game_over = check_game_state(board, ROWS, COLUMNS, 2, WHITE, myfont, "PLAYER 2 WINS!!", screen)
                        turn -= 1

                        print_board(board)
                        draw_board(board, screen, ROWS, COLUMNS, SQUARESIZE, RADIUS, height)


        # Player two's turn
        # remove event.pos[0] and replace it with the right value based on the AI's choice
        # 50 for COL0, 150 for COL1, 250 for COL3 and so on..
        if turn == 0 and AI:
            x_position = p2.run_algo(board, 1, P2DIFFICULTY)
            valid = update_game_state(board, SQUARESIZE, ROWS, 1, x_position)
            if valid:
                game_over = check_game_state(board, ROWS, COLUMNS, 1, WHITE, myfont, "PLAYER 1 WINS!!", screen)
                turn += 1

                print_board(board)
                draw_board(board, screen, ROWS, COLUMNS, SQUARESIZE, RADIUS, height)

                AI = False


        if turn == 0:
            AI = True

        if game_over:
            pygame.time.wait(3000)
                    

def options():
    pygame.display.set_caption("Options")
    global P2DIFFICULTY
    while True:

        screen.fill(BACKGROUND_COLOR)

        MENU_MOUSE_POSITION = pygame.mouse.get_pos()

        OPTIONS_TEXT = myfont.render("OPTIONS", 1, WHITE)
        PLAYER_TWO_TEXT = myfont.render("2P", 1, YELLOW)

        P2EASY_DIFFICULTY = Button(image=None, pos=(357, 250), text_input="EASY", font=myfont, base_color=YELLOW, hovering_color=GREY)
        P2MEDIUM_DIFFICULTY = Button(image=None, pos=(357, 350), text_input="MEDIUM", font=myfont, base_color=YELLOW, hovering_color=GREY)
        P2HARD_DIFFICULTY = Button(image=None, pos=(357, 450), text_input="HARD", font=myfont, base_color=YELLOW, hovering_color=GREY)

        BACK_BUTTON = Button(image=None, pos=(357, 650), text_input="GO BACK", font=myfont, base_color=WHITE, hovering_color=GREY)

        screen.blit(OPTIONS_TEXT, (210, 10))
        screen.blit(PLAYER_TWO_TEXT, (320, 100))

        for button in [BACK_BUTTON, P2EASY_DIFFICULTY, P2MEDIUM_DIFFICULTY, P2HARD_DIFFICULTY]:
            button.changeColor(MENU_MOUSE_POSITION)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if P2EASY_DIFFICULTY.checkForInput(MENU_MOUSE_POSITION):
                    P2DIFFICULTY = 2
                if P2MEDIUM_DIFFICULTY.checkForInput(MENU_MOUSE_POSITION):
                    P2DIFFICULTY = 3
                if P2HARD_DIFFICULTY.checkForInput(MENU_MOUSE_POSITION):
                    P2DIFFICULTY = 4
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POSITION):
                    main_menu()

        pygame.display.update()


def main_menu():
    pygame.display.set_caption("Main Menu")
    while True:
        
        screen.fill(BACKGROUND_COLOR)

        MENU_MOUSE_POSITION = pygame.mouse.get_pos()

        MENU_TEXT = myfont.render("MAIN MENU", 1, WHITE)

        PLAY_BUTTON = Button(image=None, pos=(357, 250), text_input="PLAY", font=myfont, base_color=WHITE, hovering_color=GREY)
        OPTIONS_BUTTON = Button(image=None, pos=(357, 350), text_input="OPTIONS", font=myfont, base_color=WHITE, hovering_color=GREY)
        QUIT_BUTTON = Button(image=None, pos=(357, 450), text_input="QUIT", font=myfont, base_color=WHITE, hovering_color=GREY)

        screen.blit(MENU_TEXT, (187, 50))

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
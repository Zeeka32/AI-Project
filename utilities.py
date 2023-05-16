import pygame
import math

RED = (255,0,0)
BOARD_COLOR = (146,146,189)
YELLOW = (255,255,0)
WHITE = (230, 230, 230)
GREY = (150, 150, 150)
BACKGROUND_COLOR = (24,20,20)

def get_next_open_row(board, rows, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r


def tie(board):
    for c in range(7):
        if board[5][c] == 0.0:
            return False

    return True

def winning_move(board, piece, rows, columns):
    for c in range(columns):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    for c in range(columns-3):
        for r in range(rows):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    for c in range(columns-3):
        for r in range(3, rows):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    for c in range(columns-3):
        for r in range(rows-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True


def update_game_state(board, square_size, rows, player_number, x_position):
    col = int(math.floor(x_position/square_size))

    if board[rows-1][col] == 0:
        row = get_next_open_row(board, rows, col)
        board[row][col] = player_number
        return True

    return False


def check_game_state(board, rows, columns, player_number, player_color, myfont, message, screen):
    if winning_move(board, player_number, rows, columns):
        label = myfont.render(message, 1, player_color)
        screen.blit(label, (95,10))
        return True
    
    if tie(board):
        label = myfont.render("ITS A TIE!!", 1, BOARD_COLOR)
        screen.blit(label, (200,10))
        return True
    
    return False

def draw_board(board, screen, rows, columns, square_size, radius, height):
    for c in range(columns):
        for r in range(rows):
            pygame.draw.rect(screen, BOARD_COLOR, (c*square_size, r*square_size+square_size, square_size, square_size))
            pygame.draw.circle(screen, BACKGROUND_COLOR, (int(c*square_size+square_size/2), int(r*square_size+square_size+square_size/2)), radius)

    for c in range(columns):
        for r in range(rows):		
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*square_size+square_size/2), height-int(r*square_size+square_size/2)), radius)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*square_size+square_size/2), height-int(r*square_size+square_size/2)), radius)
    pygame.display.update()

def horizon(board, color, i, j, v):
    if j not in range(0, len(board[0])) or board[i][j] != color:
        return 0
    
    return 1+horizon(board, color, i, j+v, v)

def vertical(board, color, i, j, v):
    if i not in range(0, len(board)) or board[i][j] != color:
        return 0
    
    return 1+vertical(board, color, i+v, j, v)

def diagonal(board, color, i, j, v, e):
    if j not in range(0, len(board[0])) or i not in range(0, len(board)) or board[i][j] != color:
        return 0
    
    return 1+diagonal(board, color, i+v, j+e, v, e)

def is_win(board, i, j):
    cons = max(horizon(board, board[i][j], i, j, -1) + horizon(board, board[i][j], i, j, 1),
    vertical(board, board[i][j], i, j, -1) + vertical(board, board[i][j], i, j, 1),
    diagonal(board, board[i][j], i, j, -1, 1) + diagonal(board, board[i][j], i, j, 1, -1),
    diagonal(board, board[i][j], i, j, -1, -1) + diagonal(board, board[i][j], i, j, 1, 1)) - 1
         
    return True if cons == 4 else False

def get_score_core(board, i, j):
    l = [horizon(board, board[i][j], i, j, -1) + horizon(board, board[i][j], i, j, 1) - 1,
    vertical(board, board[i][j], i, j, -1) + vertical(board, board[i][j], i, j, 1) - 1,
    diagonal(board, board[i][j], i, j, -1, 1) + diagonal(board, board[i][j], i, j, 1, -1) - 1,
    diagonal(board, board[i][j], i, j, -1, -1) + diagonal(board, board[i][j], i, j, 1, 1) - 1] 

    two = 0
    three = 0

    for x in l:
        if x == 2:
            two += 1
        elif x == 3:
            three += 1

    score = 4 if j == 3 else 0
    score += two*2 + three*5

    return score

def get_score(board, i, j):
    color = board[i][j]
    sum = 0
    for i in range(6):
        for j in range(7):
            if board[i][j] == color:
                sum+=get_score_core(board, i, j)

    return sum

def get_empty(board):
    empty = [-1]*7
    for i in range(7):
        for j in range(6):
            if board[j][i] == 0:
                empty[i] = j
                break

    return empty

def is_draw(board):
    return False if any(0 in row for row in board) else True

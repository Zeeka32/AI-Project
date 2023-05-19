from utilities import *

# implement your agent here
def connect4_ai(board, turn, depth):

    copyboard = board.copy()

    for i in range(6):
        for j in range(7):
            copyboard[i][j] = board[5 - i][j]
        

    print(copyboard)

    if turn == 2:
        for i in range(6):
            for j in range(7):
                if copyboard[i][j] == 2:
                    copyboard[i][j] = 1
                elif copyboard[i][j] == 1:
                    copyboard[i][j] = 2

    c = [-1]
    alpha = float('-inf')
    beta = float('inf')
    maxi(copyboard, depth, c, alpha, beta)
    return c[0]


def mini(board, depth, alpha, beta):
    if is_draw(board):
        return 0

    empty = get_empty(board)

    for i in range(7):
        if empty[i] != -1:
            board[empty[i]][i] = 2
            isWin = is_win(board, empty[i], i)
            board[empty[i]][i] = 0
            if isWin:
                return float('-inf')

    minimmum = float('inf')

    if depth == 0:
        for i in range(7):
            if empty[i] != -1:
                board[empty[i]][i] = 2
                minimmum = min(maxi(board, 0, [0], alpha, beta), minimmum)
                board[empty[i]][i] = 0

                #alpha beta pruning
                beta = min(beta, minimmum)
                if alpha >= beta:
                    return minimmum

        return minimmum

    for i in range(7):
        if empty[i] != -1:
            board[empty[i]][i] = 2
            minimmum = min(maxi(board, depth - 1, [0], alpha, beta), minimmum)
            board[empty[i]][i] = 0

            #alpha beta pruning
            beta = min(beta, minimmum)
            if alpha >= beta:
                return minimmum

    return minimmum



def maxi(board, depth, c, alpha, beta):

    if is_draw(board):
        c[0] = -1
        return 0

    empty = get_empty(board)

    for i in range(7):
        if empty[i] != -1:
            board[empty[i]][i] = 1
            isWin = is_win(board, empty[i], i)
            board[empty[i]][i] = 0

            if isWin:
                c[0] = i
                return float('inf')

    maximmum = float('-inf')

    if depth == 0:
        for i in range(7):
            if empty[i] != -1:
                board[empty[i]][i] = 1
                maximmum = max(score_position(board, 1), maximmum)
                board[empty[i]][i] = 0

                #alpha beta pruning
                
                alpha = max(alpha, maximmum)
                if alpha >= beta:
                    return maximmum

        return maximmum

    for i in range(7):
        if empty[i] != -1:
            board[empty[i]][i] = 1
            d = mini(board, depth - 1, alpha, beta)

            if d == float('-inf') and c[0] == -1: c[0] = i
            if maximmum < d:
                maximmum = d
                c[0] = i
            board[empty[i]][i] = 0

           #alpha beta pruning
            
            alpha = max(alpha, maximmum)
            if alpha >= beta:
                return maximmum


    return maximmum

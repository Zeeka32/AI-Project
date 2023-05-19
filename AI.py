import numpy as np

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
                maximmum = max(get_score(board, empty[i], i), maximmum)
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

def horizon(board, color, i, j, v):
    if j not in range(0, len(board[0])) or board[i][j] != color:
        return 0

    return 1 + horizon(board, color, i, j + v, v)


def vertical(board, color, i, j, v):
    if i not in range(0, len(board)) or board[i][j] != color:
        return 0

    return 1 + vertical(board, color, i + v, j, v)


def diagonal(board, color, i, j, v, e):
    if j not in range(0, len(board[0])) or i not in range(0, len(board)) or board[i][j] != color:
        return 0

    return 1 + diagonal(board, color, i + v, j + e, v, e)


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

    two = l.count(2)
    three = l.count(3)

    score = 4 if j == 3 else 0
    score += two * 2 + three * 5

    return score


def get_score(board, i, j):
    color = board[i][j]
    sum = 0
    for i in range(6):
        for j in range(7):
            if board[i][j] == color:
                sum += get_score_core(board, i, j)

    return sum


def get_empty(board):
    empty = [-1] * 7
    for i in range(7):
        for j in range(6):
            if board[j][i] == 0:
                empty[i] = j
                break

    return empty


def is_draw(board):
    return False if any(0 in row for row in board) else True
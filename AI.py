from utilities import *

class Player:
    def __init__(self):
        self.algo = None

    def set_algo(self, algo):
        self.algo = algo

    def run_algo(self, board, turn, depth):
        return self.algo(board, turn, depth)


# implement your agent here
def connect4_ai(board, turn, depth):

    copyboard = board.copy()

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
    values = [50, 150, 250, 350, 450, 550, 650]
    return values[c[0]]


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

# minimax without alpha beta pruning, max depth ~ 5
def minimax_no_pruning(board, turn, depth):

    copyboard = board.copy()

    if turn == 2:
        for i in range(6):
            for j in range(7):
                if copyboard[i][j] == 2:
                    copyboard[i][j] = 1
                elif copyboard[i][j] == 1:
                    copyboard[i][j] = 2

    c = [-1]
    maxi(copyboard, depth, c)
    values = [50, 150, 250, 350, 450, 550, 650]
    return values[c[0]]


def mini_no_pruning(board, depth):
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
                minimmum = min(maxi(board, 0, [0]), minimmum)
                board[empty[i]][i] = 0

        return minimmum

    for i in range(7):
        if empty[i] != -1:
            board[empty[i]][i] = 2
            minimmum = min(maxi(board, depth - 1, [0]), minimmum)
            board[empty[i]][i] = 0

    return minimmum


def maxi_no_pruning(board, depth, c):
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

        return maximmum

    for i in range(7):
        if empty[i] != -1:
            board[empty[i]][i] = 1
            d = mini(board, depth - 1)

            if d == float('-inf') and c[0] == -1: c[0] = i
            if maximmum < d:
                maximmum = d
                c[0] = i
            board[empty[i]][i] = 0

    return maximmum
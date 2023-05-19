import numpy as np

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
                maximmum = score_position(board, 1)
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

def score_position(board, piece):
    score = 0

    # Evaluate winning positions
    score += 8 * count_windows(board, 4, piece)  # Four in a row
    score += 4 * count_windows(board, 3, piece)  # Three in a row

    # Evaluate number of possible winning lines
    score += 3 * count_winning_lines(board, piece)

    # Evaluate center column preference
    center_column = board[:, 7 // 2]
    score += 4 * np.count_nonzero(center_column == piece)

    # Evaluate piece count
    ai_count = np.count_nonzero(board == piece)
    player_count = np.count_nonzero(board == (3 - piece))
    score += 2 * (ai_count - player_count)

    return score

def count_windows(board, num_pieces, piece):
    count = 0

    # Check horizontal windows
    for r in range(6):
        for c in range(7 - num_pieces + 1):
            window = board[r, c:c+num_pieces]
            if np.count_nonzero(window == piece) == num_pieces:
                count += 1

    # Check vertical windows
    for c in range(7):
        for r in range(6 - num_pieces + 1):
            window = board[r:r+num_pieces, c]
            if np.count_nonzero(window == piece) == num_pieces:
                count += 1

    # Check positively sloped diagonal windows
    for r in range(6 - num_pieces + 1):
        for c in range(7 - num_pieces + 1):
            window = [board[r+i][c+i] for i in range(num_pieces)]
            if np.count_nonzero(window == piece) == num_pieces:
                count += 1

    # Check negatively sloped diagonal windows
    for r in range(6 - num_pieces + 1):
        for c in range(7 - num_pieces + 1):
            window = [board[r+num_pieces-1-i][c+i] for i in range(num_pieces)]
            if np.count_nonzero(window == piece) == num_pieces:
                count += 1

    return count

def count_winning_lines(board, piece):
    count = 0

    # Check horizontal winning lines
    for r in range(6):
        for c in range(4):
            window = board[r, c:c+4]
            if np.count_nonzero(window == piece) == 3 and np.count_nonzero(window == 0) == 1:
                count += 1

    # Check vertical winning lines
    for c in range(7):
        for r in range(3):
            window = board[r:r+4, c]
            if np.count_nonzero(window == piece) == 3 and np.count_nonzero(window == 0) == 1:
                count += 1

    # Check positively sloped diagonal winning lines
    for r in range(3):
        for c in range(4):
            window = [board[r+i][c+i] for i in range(4)]
            if np.count_nonzero(window == piece) == 3 and np.count_nonzero(window == 0) == 1:
                count += 1

    # Check negatively sloped diagonal winning lines
    for r in range(3):
        for c in range(3):
            window = [board[r+3-i][c+i] for i in range(4)]
            if np.count_nonzero(window == piece) == 3 and np.count_nonzero(window == 0) == 1:
                count += 1

    return count
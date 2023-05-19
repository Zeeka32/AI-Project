import numpy as np

# normal scoring mechanism
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


# chat GPT scoring mechanism
def score_position(board, piece):
    score = 0

    # Evaluate winning positions
    score += 1000 * count_windows(board, 4, piece)  # Four in a row
    score += 4 * count_windows(board, 3, piece)  # Three in a row

    # Evaluate number of possible winning lines
    score += 5 * count_winning_lines(board, piece)

    # Evaluate center column preference
    center_column = board[:, 7 // 2]
    score += 4 * np.count_nonzero(center_column == piece)

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
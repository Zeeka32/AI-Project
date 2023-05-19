from board import Board
import time
from AI import *

# GAME LINK
# http://kevinshannon.com/connect4/


def main():
    board = Board()

    time.sleep(2)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES
        board.print_grid(game_board)
        print("\n")

        game_board = np.array(game_board)
        # YOUR CODE GOES HERE

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column
        best_col = connect4_ai(game_board, 1, 4)
        board.select_column(best_col)

        time.sleep(3)


if __name__ == "__main__":
    main()

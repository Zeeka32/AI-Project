from board import Board
import numpy as np
from tkinter import *
import time
from AI import *

# GAME LINK
# http://kevinshannon.com/connect4/

DIFFICULTY = 4
ALGO = 1

def handle_algo_selection():
    global ALGO
    ALGO = algo_var.get()
    print("Selected option:", ALGO)

def handle_diff_selection():
    global DIFFICULTY
    DIFFICULTY = int(diff_var.get())
    print("Selected option:", DIFFICULTY)

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

        best_col = connect4_ai(game_board, 1, DIFFICULTY)

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column
        board.select_column(best_col)

        time.sleep(2)


def handle_button_click():
    main()

root = Tk()
root.title("Connect 4")
root.geometry("400x330")

algoLabel = Label(root, text="Algorithm Type")
algoLabel.pack()

algo_var = StringVar()

# Create radio buttons
radio_button1 = Radiobutton(root, text="Minimax", variable=algo_var, value=1, command=handle_algo_selection)
radio_button2 = Radiobutton(root, text="Alpha Beta Pruning", variable=algo_var, value=2, command=handle_algo_selection)

# Pack the radio buttons
radio_button1.pack()
radio_button2.pack()

diffLabel = Label(root, text="Algorithm Difficulty")
diffLabel.pack()

diff_var = StringVar()

radio_button11 = Radiobutton(root, text="Easy", variable=diff_var, value=2, command=handle_diff_selection)
radio_button22 = Radiobutton(root, text="Medium", variable=diff_var, value=4, command=handle_diff_selection)
radio_button32 = Radiobutton(root, text="Hard", variable=diff_var, value=6, command=handle_diff_selection)

radio_button11.pack()
radio_button22.pack()
radio_button32.pack()

button = Button(root, text="Excute", command=handle_button_click)

button.pack()

root.mainloop()
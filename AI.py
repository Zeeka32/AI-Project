import random
class Player:
    def __init__(self):
        self.algo = None

    def set_algo(self, algo):
        self.algo = algo

    def run_algo(self, board):
        return self.algo(board)
    
# implement your agent here
def easy_ai(board):
    values = [50, 150, 250, 350, 450, 550]
    return random.choice(values)

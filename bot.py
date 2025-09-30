import random

class Bot:
    def __init__(self, name="Máy", symbol="X"):
        self.name = name
        self.symbol = symbol

    #Nước chơi của bot
    def move(self, board):
        empty_cells = [(r, c) for r in range(len(board)) for c in range(len(board)) if board[r][c] == " "]
        return random.choice(empty_cells)

from player import Player
from bot import Bot

class FiveInARow:
    def __init__(self):
        self.size = 15
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.players = []

    def print_board(self):
        for row in self.board:
            print(" ".join(row))

    def check_win(self, row, col, symbol):
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for dr, dc in directions:
            count = 1
            r, c = row+dr, col+dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                r += dr
                c += dc
            r, c = row-dr, col-dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False

    def is_draw(self):
        return all(self.board[r][c] != " " for r in range(self.size) for c in range(self.size))

    def play(self, players):
        if players is None:
            self.players = [Player("Người chơi", "O"), Bot("Máy", "X")]
        else:
            self.players = players
        turn = 0
        while True:
            self.print_board()
            current_player = self.players[turn % 2]
            print(f"{current_player.name} ({current_player.symbol}) chơi")

            row, col = current_player.move(self.board)

            if self.board[row][col] != " ":
                print("Ô đã được đánh, chọn lại!")
                continue

            self.board[row][col] = current_player.symbol

            if self.check_win(row, col, current_player.symbol):
                self.print_board()
                print(f"{current_player.name} thắng!")
                break
            if self.is_draw():
                self.print_board()
                print("Hòa!")
                break

            turn += 1
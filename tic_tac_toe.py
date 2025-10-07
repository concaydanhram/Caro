import random
from player import Player
from bot import Bot

class TicTacToe:
    def __init__(self):
        self.size = 3
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.players = []

    def print_board(self):
        for row in self.board:
            print("|".join(row))
            print("-" * (2 * self.size - 1))

    def check_win(self, row, col, symbol):
        # hàng
        if all(self.board[row][c] == symbol for c in range(self.size)):
            return True
        # cột
        if all(self.board[r][col] == symbol for r in range(self.size)):
            return True
        # chéo chính
        if row == col and all(self.board[i][i] == symbol for i in range(self.size)):
            return True
        # chéo phụ
        if row + col == self.size - 1 and all(self.board[i][self.size - 1 - i] == symbol for i in range(self.size)):
            return True
        return False

    def is_draw(self):
        return all(self.board[r][c] != " " for r in range(self.size) for c in range(self.size))

    def play(self, players):
        if players is None:
            player = Player("Người chơi", "X")
            bot = Bot("Máy", "O")

            # Ngẫu nhiên chọn ai đi trước
            self.players = [player, bot]
            random.shuffle(self.players)

            # Đảm bảo người đi trước luôn là X, người sau là O
            self.players[0].symbol = "X"
            self.players[1].symbol = "O"

            print(f"{self.players[0].name} đi trước với ký hiệu {self.players[0].symbol}")
        else:
            self.players = players

        turn = 0
        while True:
            self.print_board()
            current_player = self.players[turn % 2]
            print(f"{current_player.name} ({current_player.symbol}) chơi")

            # 👇 Nếu là Bot thì truyền cả game vào
            if isinstance(current_player, Bot):
                row, col = current_player.move(self.board, self)
            else:
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

    def check_win_board(self, board, symbol):
        """chỉ dùng cho bot trong minimax"""
        # Gán tạm self.board = board để có thể tái sử dụng check_win()
        original_board = self.board
        self.board = board  # Tạm thời thay bàn cờ

        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == symbol:
                    if self.check_win(r, c, symbol):
                        self.board = original_board  # khôi phục lại
                        return True

        self.board = original_board  # khôi phục lại
        return False
# game_logic.py
import random
from player import Player
from bot import Bot

class GameLogic:
    def __init__(self, size, win_length):
        self.size = size
        self.win_length = win_length
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.players = []
        self.turn = 0
        self.win_line = None

    def print_board(self):
        for row in self.board:
            print("|".join(row))
            print("-" * (2 * self.size - 1))

    def check_win(self, row, col, symbol):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1 
            
            # Khởi tạo điểm đầu và điểm cuối là chính ô vừa đánh
            start_r, start_c = row, col
            end_r, end_c = row, col
            
            # 1. Quét về phía dương (Positive direction)
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                end_r, end_c = r, c # Cập nhật điểm cuối
                r += dr
                c += dc
                
            # 2. Quét về phía âm (Negative direction)
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                start_r, start_c = r, c # Cập nhật điểm đầu
                r -= dr
                c -= dc
                
            if count >= self.win_length:
                # Lưu lại tọa độ để UI vẽ
                self.win_line = [(start_r, start_c), (end_r, end_c)]
                return True
                
        return False

    def is_draw(self):
        return all(self.board[r][c] != " " for r in range(self.size) for c in range(self.size))

    def check_win_board(self, board, symbol):
        """
        Phiên bản update: Backup self.win_line để Bot không làm mất dữ liệu
        """
        original_board = self.board
        # Backup lại đường thắng hiện tại (nếu có) để Bot không ghi đè lung tung khi đang suy nghĩ
        original_win_line = self.win_line 
        
        self.board = board
        
        winner_found = False
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == symbol:
                    if self.check_win(r, c, symbol):
                        winner_found = True
                        break
            if winner_found: break

        self.board = original_board
        self.win_line = original_win_line # Khôi phục lại trạng thái cũ
        return winner_found
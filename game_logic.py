# game_logic.py
import random
from player import Player
from bot import Bot

class GameLogic:
    def __init__(self, size, win_length):
        self.size = size                # Kích thước bàn cờ NxN
        self.win_length = win_length    # Số ô liên tiếp để thắng

        # Mảng bàn cờ: khởi tạo toàn bộ là ô trống " "
        self.board = [[" " for _ in range(self.size)] for _ in range(self.size)]

        self.players = []               # Danh sách người chơi
        self.turn = 0                   # Chỉ số người chơi hiện tại
        self.win_line = None            # Tọa độ đường thắng để UI vẽ

    # Kiểm tra thắng/thua
    def check_win(self, row, col, symbol):
        # Kiểm tra 8 hướng theo 4 phương:
        # ngang, dọc, chéo chính (trái trên -> phải dưới), chéo phụ (ngược lại)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1 
            
            # Khởi tạo điểm đầu và điểm cuối là chính ô vừa đánh
            start_r, start_c = row, col
            end_r, end_c = row, col
            
            # 1. Quét về phía dương
            r, c = row + dr, col + dc
            # Nếu trong phạm vi bàn cờ và cùng symbol thì tăng đếm và tiếp tục quét
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                end_r, end_c = r, c # Cập nhật điểm cuối
                r += dr
                c += dc
                
            # 2. Quét về phía âm (tương tự nhưng ngược lại)
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == symbol:
                count += 1
                start_r, start_c = r, c # Cập nhật điểm đầu
                r -= dr
                c -= dc
            
            # Nếu đếm được đủ số ô liên tiếp để thắng, ghi nhận lại tọa độ để UI vẽ, trả về True
            if count >= self.win_length:
                self.win_line = [(start_r, start_c), (end_r, end_c)]
                return True
                
        return False

    # Kiểm tra hòa, tức là bàn cờ đã đầy chưa
    def is_draw(self):
        return all(self.board[r][c] != " " for r in range(self.size) for c in range(self.size))

    # Kiểm tra thắng/thua (dành riêng cho Bot, không làm ảnh hưởng đến trạng thái game chính)
    def check_win_board(self, board, symbol):
        # Backup lại trạng thái bàn cờ và đường thắng hiện tại
        original_board = self.board
        original_win_line = self.win_line 
        
        # Gán tạm thời bàn cờ hiện tại bằng bàn cờ do Bot truyền vào
        self.board = board
        
        # Kiểm tra thắng/thua
        is_winner = False
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c] == symbol:
                    if self.check_win(r, c, symbol):
                        is_winner = True
                        break
            if is_winner: break

        # Khôi phục lại trạng thái cũ, trả về kết quả kiểm tra
        self.board = original_board
        self.win_line = original_win_line   
        return is_winner
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

    # Kiểm tra thắng/thua tại trạng thái hiện tại của bàn cờ
    def check_win(self, row, col, symbol, board=None, update_ui=True):

        current_board = self.board if board is None else board
        # 4 huong cần kiểm tra: ngang, dọc, chéo chính, chéo phụ
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1 
            
            # Khởi tạo điểm đầu và điểm cuối là chính ô vừa đánh
            start_r, start_c = row, col
            end_r, end_c = row, col
            
            # 1. Quét về phía dương
            r, c = row + dr, col + dc
            # Nếu trong phạm vi bàn cờ và cùng symbol thì tăng đếm và tiếp tục quét
            while 0 <= r < self.size and 0 <= c < self.size and current_board[r][c] == symbol and count < self.win_length:
                count += 1
                end_r, end_c = r, c # Cập nhật điểm cuối
                r += dr
                c += dc
                
            # 2. Quét về phía âm
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and current_board[r][c] == symbol and count < self.win_length:
                count += 1
                start_r, start_c = r, c # Cập nhật điểm đầu
                r -= dr
                c -= dc
            
            # Nếu đếm được đủ số ô liên tiếp để thắng, ghi nhận lại tọa độ để UI vẽ, trả về True
            if count >= self.win_length:
                if update_ui:
                    self.win_line = ((start_r, start_c), (end_r, end_c))
                return True
                
        return False

    # Kiểm tra hòa, tức là bàn cờ đã đầy chưa
    def is_draw(self):
        return all(self.board[r][c] != " " for r in range(self.size) for c in range(self.size))
import random

class Bot:
    def __init__(self, name="Máy", symbol="X", max_depth=3):
        self.name = name
        self.symbol = symbol
        self.max_depth = max_depth

    def move(self, board, game):
        # Lấy những ô xung quanh các ô đã đánh
        possible_moves = self.get_promising_moves(board)
        
        # Nếu bàn cờ trống trơn (lượt đầu tiên), đánh vào giữa
        if not possible_moves:
            center = len(board) // 2
            return center, center
        
        best_score = float('-inf')
        best_move = None
        
        # Nếu chỉ có 1 nước đi thì đánh luôn 
        if len(possible_moves) == 1:
            return list(possible_moves)[0]

        # Duyệt qua các nước đi khả dĩ
        for r, c in possible_moves:
            board[r][c] = self.symbol
            score = self.minimax(board, 0, False, float('-inf'), float('inf'), game)
            board[r][c] = " "

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    # Minimax với Alpha-Beta Pruning
    def minimax(self, board, depth, is_maximizing, alpha, beta, game):
        opponent = "O" if self.symbol == "X" else "X"

        # Kiểm tra kết quả (Win/Lose) ở trạng thái hiện tại
        if game.check_win_board(board, self.symbol):
            return 10000 - depth
        elif game.check_win_board(board, opponent):
            return -10000 + depth
        
        # Hết độ sâu hoặc hòa
        if depth >= self.max_depth or self.is_full(board):
            return self.evaluate(board, game)

        # LẤY CÁC NƯỚC ĐI KHẢ DĨ (Đã tối ưu)
        possible_moves = self.get_promising_moves(board)
        
        if is_maximizing:
            best_score = float('-inf')
            for r, c in possible_moves:
                board[r][c] = self.symbol
                score = self.minimax(board, depth + 1, False, alpha, beta, game)
                board[r][c] = " "
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for r, c in possible_moves:
                board[r][c] = opponent
                score = self.minimax(board, depth + 1, True, alpha, beta, game)
                board[r][c] = " "
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score

    def get_promising_moves(self, board):
        """
        Thay vì trả về tất cả ô trống, chỉ trả về các ô trống
        nằm trong phạm vi 1-2 ô so với các quân cờ hiện có.
        """
        possible_moves = set()
        size = len(board)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        found_any_piece = False
        for r in range(size):
            for c in range(size):
                if board[r][c] != " ":
                    found_any_piece = True
                    # Tìm các ô trống xung quanh ô đã đánh (phạm vi 1 ô)
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == " ":
                            possible_moves.add((nr, nc))
        
        # Nếu bàn cờ chưa có quân nào (lượt đầu), trả về rỗng để hàm move xử lý đánh vào giữa
        if not found_any_piece:
            return []
            
        return list(possible_moves)

    def evaluate(self, board, game):
        # Đơn giản hóa hàm evaluate để chạy nhanh hơn
        my_score = self.count_sequences(board, self.symbol)
        opp_score = self.count_sequences(board, "O" if self.symbol == "X" else "X")
        # Phòng thủ quan trọng hơn tấn công một chút trong heuristic này
        return my_score - (opp_score * 1.2)

    def count_sequences(self, board, symbol):
        n = len(board)
        score = 0
        # Chỉ xét 4 hướng chính để đỡ lặp
        directions = [(0,1), (1,0), (1,1), (1,-1)]

        for r in range(n):
            for c in range(n):
                if board[r][c] == symbol:
                    for dr, dc in directions:
                        # Đếm số quân liên tiếp
                        count = 0
                        blocked = 0
                        
                        # Kiểm tra chuỗi
                        for k in range(1, 5): 
                            nr, nc = r + dr*k, c + dc*k
                            if 0 <= nr < n and 0 <= nc < n:
                                if board[nr][nc] == symbol:
                                    count += 1
                                elif board[nr][nc] != " ":
                                    blocked += 1
                                    break
                            else:
                                blocked += 1 # Bị chặn bởi biên
                                break
                        
                        # Tính điểm dựa trên độ nguy hiểm
                        if count == 4: score += 100000
                        elif count == 3:
                            if blocked == 0: score += 1000
                            else: score += 100
                        elif count == 2:
                            if blocked == 0: score += 10
                            
        return score

    def is_full(self, board):
        return all(board[r][c] != " " for r in range(len(board)) for c in range(len(board)))
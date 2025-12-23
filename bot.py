import random
import time

class Bot:
    def __init__(self, name="Máy", symbol="X", max_depth=3, use_pruning=True):
        self.name = name
        self.symbol = symbol
        self.max_depth = max_depth
        self.use_pruning = use_pruning  # [NEW] Cờ bật/tắt cắt tỉa
        
        # Thống kê hiệu năng
        self.nodes_visited = 0
        self.last_think_time = 0

    def move(self, board, game):
        start_time = time.time()
        self.nodes_visited = 0
        
        possible_moves = self.get_promising_moves(board)
        
        if not possible_moves:
            center = len(board) // 2
            self.last_think_time = round(time.time() - start_time, 4)
            return center, center
        
        if len(possible_moves) == 1:
            self.last_think_time = round(time.time() - start_time, 4)
            return list(possible_moves)[0]

        best_score = float('-inf')
        best_move = None
        
        for r, c in possible_moves:
            board[r][c] = self.symbol
            # Gọi minimax
            score = self.minimax(board, 0, False, float('-inf'), float('inf'), game)
            board[r][c] = " "

            if score > best_score:
                best_score = score
                best_move = (r, c)

        end_time = time.time()
        self.last_think_time = round(end_time - start_time, 4)
        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta, game):
        self.nodes_visited += 1 # Đếm số node đã duyệt

        opponent = "O" if self.symbol == "X" else "X"

        if game.check_win_board(board, self.symbol):
            return 10000 - depth
        elif game.check_win_board(board, opponent):
            return -10000 + depth
        
        if depth >= self.max_depth or self.is_full(board):
            return self.evaluate(board, game)

        possible_moves = self.get_promising_moves(board)
        
        if is_maximizing:
            best_score = float('-inf')
            for r, c in possible_moves:
                board[r][c] = self.symbol
                score = self.minimax(board, depth + 1, False, alpha, beta, game)
                board[r][c] = " "
                best_score = max(best_score, score)
                
                # [UPDATE] Chỉ cập nhật Alpha và cắt tỉa nếu chế độ Pruning được BẬT
                if self.use_pruning:
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
                
                # [UPDATE] Chỉ cập nhật Beta và cắt tỉa nếu chế độ Pruning được BẬT
                if self.use_pruning:
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    def get_promising_moves(self, board):
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
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == " ":
                            possible_moves.add((nr, nc))
        
        if not found_any_piece:
            return []
            
        return list(possible_moves)

    def evaluate(self, board, game):
        my_score = self.count_sequences(board, self.symbol)
        opp_score = self.count_sequences(board, "O" if self.symbol == "X" else "X")
        return my_score - (opp_score * 1.2)

    def count_sequences(self, board, symbol):
        n = len(board)
        score = 0
        directions = [(0,1), (1,0), (1,1), (1,-1)]

        for r in range(n):
            for c in range(n):
                if board[r][c] == symbol:
                    for dr, dc in directions:
                        count = 0
                        blocked = 0
                        for k in range(1, 5): 
                            nr, nc = r + dr*k, c + dc*k
                            if 0 <= nr < n and 0 <= nc < n:
                                if board[nr][nc] == symbol:
                                    count += 1
                                elif board[nr][nc] != " ":
                                    blocked += 1
                                    break
                            else:
                                blocked += 1
                                break
                        
                        if count == 4: score += 100000
                        elif count == 3:
                            if blocked == 0: score += 1000
                            else: score += 100
                        elif count == 2:
                            if blocked == 0: score += 10
                            
        return score

    def is_full(self, board):
        return all(board[r][c] != " " for r in range(len(board)) for c in range(len(board)))
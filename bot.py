import random
import time
from player import Player

class Bot(Player):
    def __init__(self, name="Máy", symbol="X", max_depth=3, use_pruning=True):
        super().__init__(name, symbol) 
        self.max_depth = max_depth         # Độ sâu tối đa cây tìm kiếm Minimax
        self.use_pruning = use_pruning     # Bật/tắt cắt tỉa Alpha-Beta
        
        # Thống kê hiệu năng
        self.nodes_visited = 0
        self.last_think_time = 0

    #override
    def move(self, board, game):
        start_time = time.time()
        self.nodes_visited = 0
        
        possible_moves = self.get_promising_moves(board)
        
        # Nếu bàn cờ trống (lượt đầu tiên), đánh vào chính giữa
        if not possible_moves:
            center = len(board) // 2
            self.last_think_time = round(time.time() - start_time, 2)
            return center, center
        
        # Nếu chỉ có 1 nước đi, chọn luôn nước đó 
        if len(possible_moves) == 1:
            return list(possible_moves)[0]
        
        # Nếu có nước đi nào giúp thắng ngay lập tức, đánh luôn không cần nghĩ
        for r, c in possible_moves:
            board[r][c] = self.symbol
            if game.check_win_board(board, self.symbol):
                board[r][c] = " " # Trả lại trạng thái cũ trước khi return
                return r, c
            board[r][c] = " " # Trả lại trạng thái cũ
        
        # --- Bắt đầu Minimax để chọn nước đi tốt nhất ---
        best_score = float('-inf')
        best_move = None

        # Duyệt qua các nước đi khả dĩ
        for r, c in possible_moves:
            board[r][c] = self.symbol
            # Gọi minimax
            score = self.minimax(board, 1, False, float('-inf'), float('inf'), game)
            board[r][c] = " "

            if score > best_score:
                best_score = score
                best_move = (r, c)

        end_time = time.time()
        self.last_think_time = round(end_time - start_time, 2)
        return best_move

    def minimax(self, board, depth, is_maximizing, alpha, beta, game):
        # Đếm số node đã duyệt
        self.nodes_visited += 1 

        opponent = "O" if self.symbol == "X" else "X"
        WIN_SCORE = 1000000000

        if game.check_win_board(board, self.symbol):
            return WIN_SCORE - depth
        elif game.check_win_board(board, opponent):
            return -WIN_SCORE + depth
        
        if depth >= self.max_depth or self.is_full(board):
            # Trả về điểm ngẫu nhiên nếu ở độ sâu 1 (chế độ dễ nhất)
            if depth == 1:
                return random.randint(-10, 10)  
            return self.evaluate(board, game)

        # Lấy các nước đi khả dĩ
        possible_moves = self.get_promising_moves(board)
        
        # Đệ quy Minimax
        if is_maximizing:
            best_score = float('-inf')
            for r, c in possible_moves:
                board[r][c] = self.symbol
                score = self.minimax(board, depth + 1, False, alpha, beta, game)
                board[r][c] = " "
                best_score = max(best_score, score)
                
                # Chỉ cập nhật Alpha và cắt tỉa nếu chế độ Pruning được BẬT
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
                
                # Chỉ cập nhật Beta và cắt tỉa nếu chế độ Pruning được BẬT
                if self.use_pruning:
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best_score

    # Lấy các nước đi khả dĩ xung quanh các quân đã đánh
    def get_promising_moves(self, board):
        possible_moves = set()
        size = len(board)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        
        # Tìm các ô trống xung quanh ô đã đánh (phạm vi 1 ô)
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
            
        moves_list = list(possible_moves)

        # Sắp xếp ưu tiên các ô gần trung tâm (Heuristic đơn giản)
        center = size // 2
        moves_list.sort(key=lambda m: abs(m[0]-center) + abs(m[1]-center))
            
        return moves_list

    # Chấm điểm ước tính cho nước đi
    def evaluate(self, board, game):
        my_score = self.count_sequences(board, self.symbol, is_opp=False)
        opp_score = self.count_sequences(board, "O" if self.symbol == "X" else "X", is_opp=True)
        # Nhân 1.2 vào đối thủ để ép Bot ưu tiên chặn hơn là tấn công.
        return my_score - (opp_score * 1.2)

    # Hàm ước tính số điểm dựa trên các chuỗi quân cờ
    def count_sequences(self, board, symbol, is_opp=False):
        n = len(board)
        total_score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for r in range(n):
            for c in range(n):
                if board[r][c] != symbol:
                    continue

                # Đếm fork tại điểm này
                live_three = 0      # Chuỗi 3 quân không bị chặn 2 đầu (--- OOO ---)
                dead_four = 0       # Chuỗi 4 quân bị chặn 1 đầu (X OOOO --- )
                live_four = 0       # Chuỗi 4 quân không bị chặn 2 đầu (--- OOOO --- )

                for dr, dc in directions:
                    # --- 1. TRÁNH ĐẾM TRÙNG ---
                    prev_r, prev_c = r - dr, c - dc
                    if 0 <= prev_r < n and 0 <= prev_c < n and board[prev_r][prev_c] == symbol:
                        continue

                    count = 0
                    gaps = 0
                    blocked_end = 0

                    # Kiểm tra đầu phía sau có bị chặn không
                    if not (0 <= prev_r < n and 0 <= prev_c < n) or board[prev_r][prev_c] != " ":
                        blocked_end += 1

                    # --- 2. QUÉT ---
                    current_r, current_c = r, c
                    while 0 <= current_r < n and 0 <= current_c < n:
                        cell = board[current_r][current_c]

                        # Gặp quân của mình, tăng đếm
                        if cell == symbol:
                            count += 1
                            current_r += dr
                            current_c += dc

                        # Gặp ô trống
                        elif cell == " ":
                            # Kiểm tra ô tiếp theo sau ô trống
                            next_r, next_c = current_r + dr, current_c + dc

                            # Nếu ô tiếp theo là tường, hoặc quân đối phương, dừng quét và đánh dấu bị chặn
                            if not (0 <= next_r < n and 0 <= next_c < n) or (board[next_r][next_c] != " " and board[next_r][next_c] != symbol):
                                blocked_end += 1
                                break
                            
                            # Nếu sau ô trống là quân mình mà chưa có gap, tăng gaps và tiếp tục quét
                            if 0 <= next_r < n and 0 <= next_c < n and board[next_r][next_c] == symbol:
                                if gaps < 1:
                                    gaps += 1
                                    current_r, current_c = next_r, next_c
                                else:
                                    break
                            
                            # Nếu sau ô trống là ô trống hoặc quân đối phương, dừng quét
                            else:
                                break

                        # Gặp quân đối phương hoặc ngoài biên, dừng quét và đánh dấu bị chặn
                        else:
                            blocked_end += 1
                            break

                    # --- 3. CHẤM ĐIỂM CÁC CHUỖI ---
                    # 5 quân: Chính thức chiến thắng
                    if count >= 5:
                        total_score += 100_000_000
                        continue
                    
                    # Bị chặn 2 đầu: không có giá trị
                    if blocked_end == 2:
                        continue
                    
                    # CẢI TIẾN: LIVE THREE ĐIỂM CAO HƠN DEAD FOUR ĐỐI VỚI TẤN CÔNG (BOT)
                    # DEAD FOUR ĐIỂM CAO HƠN LIVE THREE ĐỐI VỚI PHÒNG THỦ (ĐỐI THỦ)
                    # 4 quân: Cực kỳ nguy hiểm
                    if count == 4:
                        # Live-four: không bị chặn 2 đầu
                        if blocked_end == 0:
                            total_score += 10_000_000
                            live_four += 1
                        # Dead-four: bị chặn 1 đầu
                        else:
                            if is_opp:
                                total_score += 15_000_000   # ĐỐI THỦ BẮT BUỘC PHẢI CHẶN
                            else:
                                total_score += 300_000      # Dead four dễ bị đối thủ chặn, nên ít điểm hơn
                            dead_four += 1
                        continue

                    # 3 quân: Nguy hiểm
                    if count == 3:
                        # Live-three: không bị chặn 2 đầu
                        if blocked_end == 0:
                            # Live-three gãy (có 1 ô trống ở giữa)
                            if gaps == 1:
                                total_score += 400_000
                            # Live-three không gãy
                            else:
                                total_score += 450_000
                            live_three += 1
                        # Dead-three: bị chặn 1 đầu
                        else:
                            total_score += 1_000
                        continue

                    # 2 quân: Khởi đầu, nguy hiểm chưa cao
                    if count == 2:
                        # Live-two: không bị chặn 2 đầu
                        if blocked_end == 0:
                            if gaps == 1: total_score += 800
                            else: total_score += 500
                        # Dead-two: bị chặn 1 đầu
                        else:
                            total_score += 10
                        continue

                    # 1 quân: Rất ít giá trị
                    if count == 1 and blocked_end == 0:
                        total_score += 5

                # --- 4. XỬ LÝ CÁC THẾ FORK (TẤN CÔNG KÉP) ---
                # 2 live-three: thắng trong 2 nước 
                if live_three >= 2:
                    total_score += 30_000

                # live-three + dead-four: gần như chắc thắng
                elif live_three >= 1 and dead_four >= 1:
                    total_score += 50_000

                # 2 dead-four: bắt buộc thua
                elif dead_four >= 2:
                    total_score += 80_000

                # live-four + bất kỳ threat nào khác: thắng
                if live_four >= 1 and (live_three + dead_four) >= 1:
                    total_score += 100_000

        return total_score

    # Kiểm tra bàn cờ đã đầy chưa
    def is_full(self, board):
        return all(board[r][c] != " " for r in range(len(board)) for c in range(len(board)))
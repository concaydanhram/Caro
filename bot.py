

class Bot:
    def __init__(self, name="Máy", symbol="X", max_depth=3):
        self.name = name
        self.symbol = symbol
        self.max_depth = max_depth  # Giới hạn độ sâu để đỡ nặng

    def move(self, board, game):
        best_score = float('-inf')
        best_move = None
        empty_cells = self.empty_cells(board)

        for r, c in empty_cells:
            board[r][c] = self.symbol  # giả lập đi
            score = self.minimax(board, 0, False, float('-inf'), float('inf'), game)
            board[r][c] = " "  # hoàn tác

            if score > best_score:
                best_score = score
                best_move = (r, c)

        return best_move

    # minimax có cắt tỉa alpha-beta
    def minimax(self, board, depth, is_maximizing, alpha, beta, game):
        opponent = "O" if self.symbol == "X" else "X"

        # Kiểm tra thắng thua
        if game.check_win_board(board, self.symbol):
            return 100 - depth  # Thắng: điểm cao hơn nếu nhanh
        elif game.check_win_board(board, opponent):
            return depth - 100  # Thua: điểm thấp hơn nếu nhanh
        elif self.is_full(board):
            return 0  # Hòa

        # Giới hạn độ sâu để không bị quá tải
        if depth >= self.max_depth:
            return self.evaluate(board, game)

        # Lượt bot
        if is_maximizing:
            best_score = float('-inf')
            for r, c in self.empty_cells(board):
                board[r][c] = self.symbol
                score = self.minimax(board, depth + 1, False, alpha, beta, game)
                board[r][c] = " "
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Cắt tỉa
            return best_score

        # Lượt đối thủ
        else:
            best_score = float('inf')
            for r, c in self.empty_cells(board):
                board[r][c] = opponent
                score = self.minimax(board, depth + 1, True, alpha, beta, game)
                board[r][c] = " "
                best_score = min(best_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Cắt tỉa
            return best_score

    # Hàm đánh giá tạm thời khi chưa đến kết thúc
    def evaluate(self, board, game):
        # Đếm số ô gần thắng (3 liên tiếp, 4 liên tiếp,...)
        # có thể tùy chỉnh mạnh hơn nếu bạn muốn
        my_score = self.count_sequences(board, self.symbol)
        opp_score = self.count_sequences(board, "O" if self.symbol == "X" else "X")
        return my_score - opp_score

    """Cho biết máy hay người đang có uư thế hơn (Dùng khi giới hạn độ sâu mà vẫn chưa tìm được kết quả thắng thua)"""
    def count_sequences(self, board, symbol):
        n = len(board)
        score = 0
        directions = [(0,1),(1,0),(1,1),(1,-1)]

        for r in range(n):
            for c in range(n):
                if board[r][c] == symbol:
                    for dr, dc in directions:
                        count = 1
                        for k in range(1, 4):  # đếm đến 4 ô liên tiếp
                            nr, nc = r + dr*k, c + dc*k
                            if 0 <= nr < n and 0 <= nc < n and board[nr][nc] == symbol:
                                count += 1
                            else:
                                break
                        score += count ** 2  # càng dài càng nhiều điểm
        return score

    def empty_cells(self, board):
        return [(r, c) for r in range(len(board)) for c in range(len(board)) if board[r][c] == " "]

    def is_full(self, board):
        return all(board[r][c] != " " for r in range(len(board)) for c in range(len(board)))

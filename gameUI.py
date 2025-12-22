# gameUI.py
import pygame
import time
import os
import json
import ctypes

from player import Player
from bot import Bot
from game_logic import GameLogic

class GameUI:
    def __init__(self):
        pygame.init()
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("simple-tic-tac-toe")
        self.WIDTH, self.HEIGHT = 600, 750
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Simple Tic Tac Toe with Minimax AI")
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))
        self.clock = pygame.time.Clock()

        # --- TRẠNG THÁI GAME BAN ĐẦU ---
        self.state = "menu"
        
        # --- MÀU SẮC ---
        self.COLORS = {
            'bg': (236, 240, 241),          
            'board_bg': (255, 255, 255),    
            'line': (189, 195, 199),        
            'text': (44, 62, 80),           
            'x_color': (231, 76, 60),       
            'o_color': (52, 152, 219),      
            'btn_default': (52, 152, 219),  
            'btn_hover': (41, 128, 185),    
            'btn_text': (255, 255, 255),    
            'win': (46, 204, 113),          
            'lose': (231, 76, 60),          
            'draw': (243, 156, 18),         
            'highlight': (241, 196, 15)     
        }

        # --- FONT CHỮ ---
        try:
            self.FONT_BIG = pygame.font.Font('assets/fonts/Montserrat-Bold.ttf', 50)
            self.FONT_MED = pygame.font.Font('assets/fonts/Montserrat-SemiBold.ttf', 25)
            self.FONT_REG = pygame.font.Font('assets/fonts/Montserrat-SemiBold.ttf', 20)
            self.FONT_SMALL = pygame.font.Font('assets/fonts/Montserrat-Regular.ttf', 20)
        except:
            self.FONT_BIG = pygame.font.SysFont('arial', 50, bold=True)
            self.FONT_MED = pygame.font.SysFont('arial', 25, bold=True)
            self.FONT_REG = pygame.font.SysFont('arial', 20, bold=True)
            self.FONT_SMALL = pygame.font.SysFont('arial', 20)

        # --- KHỞI TẠO CÁC BIẾN VỚI TRẠNG THÁI BAN ĐẦU ---
        self.game = None
        self.winner = None
        self.start_time = None
        self.end_time = None
        self.score_file = "scores.json"
        self.scores = []
        self.load_scores()
        
        self.last_move = None 
        self.btn_rects = {}
        self.view_mode = 3
        self.current_mode_size = 3 
        self.current_win_len = 3
        self.difficulty = 1

    # --- XỬ LÝ LƯU VÀ GHI NHẬN ĐIỂM SỐ ---
    def load_scores(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as f:
                    data = json.load(f)
                    self.scores = data if isinstance(data, list) else []
            except:
                self.scores = []
        else:
            self.scores = []

    def save_scores(self):
        # Tách ra 2 danh sách riêng
        list_3 = [s for s in self.scores if s.get('board_size') == 3]
        list_8 = [s for s in self.scores if s.get('board_size') == 8]
        
        # Sắp xếp và lấy top 10 mỗi loại
        list_3 = sorted(list_3, key=lambda x: x['score'], reverse=True)[:10]
        list_8 = sorted(list_8, key=lambda x: x['score'], reverse=True)[:10]
        
        # Gộp lại để lưu file
        self.scores = list_3 + list_8
        
        with open(self.score_file, 'w') as f:
            json.dump(self.scores, f, indent=4)

    # --- VẼ GIAO DIỆN ---
    def draw_button(self, text, rect, color_default, color_hover, action_name):
        mouse_pos = pygame.mouse.get_pos()
        rect_obj = pygame.Rect(rect)
        
        is_hovered = rect_obj.collidepoint(mouse_pos)
        color = color_hover if is_hovered else color_default
        
        pygame.draw.rect(self.screen, color, rect_obj, border_radius=12)
        
        text_surf = self.FONT_MED.render(text, True, self.COLORS['btn_text'])
        text_rect = text_surf.get_rect(center=rect_obj.center)
        self.screen.blit(text_surf, text_rect)

        self.btn_rects[action_name] = rect_obj

    # --- VẼ CHỮ Ở GIỮA ---
    def draw_text_centered(self, text, font, color, y_pos):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(self.WIDTH // 2, y_pos))
        self.screen.blit(surf, rect)

    # --- VẼ MÀN HÌNH MENU ---
    def draw_menu(self):
        self.screen.fill(self.COLORS['bg'])
        self.btn_rects = {} 

        self.draw_text_centered("TIC TAC TOE", self.FONT_BIG, self.COLORS['text'], 80)
        
        # --- PHẦN CHỌN ĐỘ KHÓ ---
        self.draw_text_centered("SELECT DIFFICULTY", self.FONT_REG, self.COLORS['text'], 130)
        
        # Tọa độ và kích thước nút độ khó
        diff_y = 160
        diff_w = 100
        diff_h = 40
        gap = 20
        start_x = (self.WIDTH - (3 * diff_w + 2 * gap)) // 2

        # Vẽ 3 nút: Easy, Medium, Hard
        levels = [("EASY", 1), ("MEDIUM", 2), ("HARD", 3)]
        
        for i, (label, level) in enumerate(levels):
            x = start_x + i * (diff_w + gap)
            rect = (x, diff_y, diff_w, diff_h)
            
            # Nếu level này đang được chọn -> Màu sáng (Active)
            # Nếu không -> Màu xám (Inactive)
            if self.difficulty == level:
                color = self.COLORS['win'] # Màu xanh lá
                text_color = (255, 255, 255)
            else:
                color = (189, 195, 199) # Màu xám
                text_color = self.COLORS['text']

            # Vẽ nút thủ công (vì hàm draw_button mặc định dùng màu khác)
            rect_obj = pygame.Rect(rect)
            pygame.draw.rect(self.screen, color, rect_obj, border_radius=8)
            
            text_surf = self.FONT_SMALL.render(label, True, text_color)
            text_rect = text_surf.get_rect(center=rect_obj.center)
            self.screen.blit(text_surf, text_rect)
            
            # Đăng ký vùng bấm (quan trọng)
            self.btn_rects[f"diff_{level}"] = rect_obj


        # --- CÁC NÚT CHƠI GAME (Dời xuống thấp hơn chút) ---
        self.draw_text_centered("SELECT MODE", self.FONT_MED, self.COLORS['text'], 240)

        btn_width, btn_height = 420, 65
        center_x = (self.WIDTH - btn_width) // 2
        
        # Nút 3x3
        self.draw_button("Classic (3x3 - Win 3)", (center_x, 280, btn_width, btn_height), 
                         self.COLORS['btn_default'], self.COLORS['btn_hover'], "mode_3x3")
        
        # Nút 8x8 (hoặc 10x10)
        self.draw_button("Big Board (8x8 - Win 5)", (center_x, 360, btn_width, btn_height), 
                         self.COLORS['btn_default'], self.COLORS['btn_hover'], "mode_8x8")

        self.draw_button("Leaderboard", (center_x, 440, btn_width, btn_height), 
                         (149, 165, 166), (127, 140, 141), "view_leaderboard") 

        self.draw_button("Quit", (center_x, 520, btn_width, btn_height), 
                         (231, 76, 60), (192, 57, 43), "quit")

    # --- VẼ BẢNG XẾP HẠNG ---
    def draw_leaderboard(self):
        self.screen.fill(self.COLORS['bg'])
        self.btn_rects = {}
        
        self.draw_text_centered("LEADERBOARD", self.FONT_BIG, self.COLORS['text'], 50)
        
        # --- VẼ NÚT TAB CHỌN BẢNG (3x3 vs 8x8) ---
        tab_y = 90
        tab_w = 160
        tab_h = 40
        gap = 20
        start_x = (self.WIDTH - (2 * tab_w + gap)) // 2
        
        # Nút Tab 3x3
        color_3 = self.COLORS['btn_default'] if self.view_mode == 3 else (189, 195, 199)
        self.draw_button("3x3 Board", (start_x, tab_y, tab_w, tab_h), 
                         color_3, color_3, "view_3x3")
        
        # Nút Tab 8x8
        color_8 = self.COLORS['btn_default'] if self.view_mode == 8 else (189, 195, 199)
        self.draw_button("8x8 Board", (start_x + tab_w + gap, tab_y, tab_w, tab_h), 
                         color_8, color_8, "view_8x8")

        # --- TIÊU ĐỀ CỘT ---
        header_y = 150
        pygame.draw.line(self.screen, self.COLORS['text'], (50, header_y + 30), (550, header_y + 30), 2)
        
        header_font = self.FONT_MED
        # Cột: Rank | Diff | Time | Date
        self.screen.blit(header_font.render("Diff", True, self.COLORS['text']), (80, header_y))
        self.screen.blit(header_font.render("Time", True, self.COLORS['text']), (250, header_y))
        self.screen.blit(header_font.render("Date", True, self.COLORS['text']), (400, header_y))
        
        # --- LỌC DỮ LIỆU ĐỂ HIỂN THỊ ---
        # Chỉ lấy dữ liệu đúng với Tab đang chọn
        current_list = [s for s in self.scores if s.get('board_size') == self.view_mode]
        # Sắp xếp lại lần nữa cho chắc (đảm bảo hiển thị đúng thứ tự)
        current_list = sorted(current_list, key=lambda x: x['score'], reverse=True)
        
        start_y = 200
        if not current_list:
            self.draw_text_centered("No records yet!", self.FONT_SMALL, self.COLORS['text'], start_y + 20)
            
        for i, entry in enumerate(current_list):
            if i >= 10: break # Chỉ hiện 10 dòng
            
            # Màu top 3
            if i in [0, 1, 2]: color = (241, 196, 15)  # Vàng cho top 3
            else: color = self.COLORS['text']
            
            date_short = entry['date'][5:16]
            diff_text = entry.get('difficulty', 'Unknown') 
        
            # Vẽ dòng
            # Cột 1: Rank + Difficulty
            rank_str = f"{i+1}. {diff_text}"
            self.screen.blit(self.FONT_SMALL.render(rank_str, True, color), (60, start_y + i * 45))
            
            # Cột 2: Time
            time_str = f"{entry['duration']}s"
            self.screen.blit(self.FONT_SMALL.render(time_str, True, color), (260, start_y + i * 45))
            
            # Cột 3: Date
            self.screen.blit(self.FONT_SMALL.render(date_short, True, color), (400, start_y + i * 45))

        self.draw_button("Back to Menu", (self.WIDTH//2 - 125, self.HEIGHT - 100, 250, 55), 
                         self.COLORS['btn_default'], self.COLORS['btn_hover'], "back_menu")

    # --- VẼ BÀN CỜ ---
    def draw_game_board(self):
        self.screen.fill(self.COLORS['bg'])
        self.btn_rects = {}
        
        # Vẽ khung bàn cờ
        board_rect = pygame.Rect(20, 20, self.WIDTH - 40, self.WIDTH - 40)
        pygame.draw.rect(self.screen, self.COLORS['board_bg'], board_rect)
        pygame.draw.rect(self.screen, self.COLORS['text'], board_rect, 3)

        size = self.game.size
        square_size = board_rect.width // size

        # Vẽ lưới
        for i in range(1, size):
            # Dọc
            start_pos = (board_rect.left + i * square_size, board_rect.top)
            end_pos = (board_rect.left + i * square_size, board_rect.bottom)
            pygame.draw.line(self.screen, self.COLORS['line'], start_pos, end_pos, 2)
            # Ngang
            start_pos = (board_rect.left, board_rect.top + i * square_size)
            end_pos = (board_rect.right, board_rect.top + i * square_size)
            pygame.draw.line(self.screen, self.COLORS['line'], start_pos, end_pos, 2)

        # Vẽ X/O
        for r in range(size):
            for c in range(size):
                symbol = self.game.board[r][c]
                if symbol != " ":
                    center_x = board_rect.left + c * square_size + square_size // 2
                    center_y = board_rect.top + r * square_size + square_size // 2
                    
                    if self.last_move == (r, c):
                        pygame.draw.rect(self.screen, self.COLORS['highlight'], 
                                         (board_rect.left + c * square_size + 2, 
                                          board_rect.top + r * square_size + 2, 
                                          square_size - 4, square_size - 4), 3)

                    self.draw_symbol(symbol, center_x, center_y, square_size)

        panel_y = self.WIDTH 

        # Vẽ đường thắng nếu có
        if self.game and self.game.win_line:
            # Lấy tọa độ hàng/cột từ logic
            (start_r, start_c), (end_r, end_c) = self.game.win_line
            
            # Chuyển đổi sang tọa độ Pixel (x, y)
            # Công thức: Lề trái + (Cột * kích thước ô) + (nửa ô để vào tâm)
            start_x = board_rect.left + start_c * square_size + square_size // 2
            start_y = board_rect.top + start_r * square_size + square_size // 2
            
            end_x = board_rect.left + end_c * square_size + square_size // 2
            end_y = board_rect.top + end_r * square_size + square_size // 2
            
            # Vẽ đường thẳng
            # Dùng màu chiến thắng (self.COLORS['win']) hoặc màu đậm hơn
            line_color = (46, 204, 113) # Xanh lá đậm
            line_width = 8 # Độ dày nét vẽ
            
            pygame.draw.line(self.screen, line_color, (start_x, start_y), (end_x, end_y), line_width)
            
            # Vẽ thêm 2 chấm tròn ở đầu và cuối cho đẹp
            pygame.draw.circle(self.screen, line_color, (start_x, start_y), line_width // 2)
            pygame.draw.circle(self.screen, line_color, (end_x, end_y), line_width // 2)
        
        # Thông báo trạng thái
        if self.state == "playing":
            current_p = self.game.players[self.game.turn % 2]
            if isinstance(current_p, Bot):
                status_text = "BOT TURN. THINKING..."
                color = self.COLORS['text']
            else:
                status_text = "YOUR TURN"
                color = self.COLORS['btn_default']
        else:
            if self.winner:
                status_text = "YOU WIN!" if self.winner.name == "Player" else "YOU LOSE!"   
                color = self.COLORS['win'] if self.winner.name == "Player" else self.COLORS['lose']
            else:
                status_text = "DRAW!"
                color = self.COLORS['draw']

        self.draw_text_centered(status_text, self.FONT_MED, color, panel_y + 30)

        btn_y = panel_y + 80
        btn_h = 55
        
        if self.state == "game_over":
            btn_w = 180
            gap = 20
            self.draw_button("Play Again", (self.WIDTH//2 - btn_w - gap//2, btn_y, btn_w, btn_h), 
                             self.COLORS['win'], (39, 174, 96), "restart")
            self.draw_button("Menu", (self.WIDTH//2 + gap//2, btn_y, btn_w, btn_h), 
                             (149, 165, 166), (127, 140, 141), "back_menu")
        else:
            self.draw_button("Menu", (self.WIDTH//2 - 75, btn_y, 150, 50), 
                             (149, 165, 166), (127, 140, 141), "back_menu")

    # --- VẼ KÝ HIỆU X HOẶC O ---
    def draw_symbol(self, symbol, x, y, size):
        radius = size // 3
        width = max(3, size // 15) # Tự động điều chỉnh độ dày nét theo size ô
        if symbol == 'X':
            color = self.COLORS['x_color']
            offset = radius - 5
            pygame.draw.line(self.screen, color, (x - offset, y - offset), (x + offset, y + offset), width)
            pygame.draw.line(self.screen, color, (x + offset, y - offset), (x - offset, y + offset), width)
        elif symbol == 'O':
            color = self.COLORS['o_color']
            pygame.draw.circle(self.screen, color, (x, y), radius, width)

    # --- BẮT ĐẦU TRÒ CHƠI MỚI ---
    def start_game(self, size, win_length):
        self.current_mode_size = size
        self.current_win_len = win_length
        
        # Khởi tạo logic game
        self.game = GameLogic(size, win_length)
        
        # --- CẤU HÌNH ĐỘ SÂU (DEPTH) THEO ĐỘ KHÓ ---
        # 1: Easy, 2: Medium, 3: Hard
        actual_depth = 3  # Mặc định
        # --- Bàn 8x8 ---
        if size == 8:  
            if self.difficulty == 1:
                actual_depth = 0  # Easy: Chơi ngẫu nhiên
            elif self.difficulty == 2:
                actual_depth = 1  # Medium: Nhìn trước 1 nước
            else:
                actual_depth = 3  # Hard: Nhìn trước 3 nước
        
        # --- Bàn 3x3 ---
        else:  # size == 3
            if self.difficulty == 1:
                actual_depth = 0  # Easy: Chơi ngẫu nhiên
            elif self.difficulty == 2:
                actual_depth = 3  # Medium: Nhìn trước 3 nước
            else:
                actual_depth = 9  # Hard: Nhìn trước 3 nước
            
        print(f"Game started: Size {size}x{size}, Difficulty Level: {self.difficulty}, Bot Depth: {actual_depth}")

        self.game.players = [
            Player("Player", "O"), 
            Bot("Bot", "X", max_depth=actual_depth) 
        ]
        self.game.turn = 0
        
        self.state = "playing"
        self.winner = None
        self.last_move = None
        self.start_time = time.time()
        self.end_time = None

    # --- XỬ LÝ SỰ KIỆN CLICK ---
    def handle_click(self, pos):
        for action, rect in self.btn_rects.items():
            if rect.collidepoint(pos):
                # --- XỬ LÝ TAB LEADERBOARD ---
                if action == "view_3x3":
                    self.view_mode = 3 # Chuyển sang xem 3x3
                elif action == "view_8x8":
                    self.view_mode = 8 # Chuyển sang xem 8x8
                
                # --- CÁC NÚT KHÁC ---
                elif action == "diff_1": self.difficulty = 1
                elif action == "diff_2": self.difficulty = 2
                elif action == "diff_3": self.difficulty = 3
                elif action == "mode_3x3": self.start_game(3, 3)
                elif action == "mode_8x8": self.start_game(8, 5)
                # Khi bấm vào nút Leaderboard ở Menu, mặc định xem 3x3 hoặc giữ nguyên
                elif action == "view_leaderboard": 
                    self.state = "leaderboard"
                    self.view_mode = 3 # Reset về 3x3 hoặc tùy bạn
                elif action == "back_menu": self.state = "menu"
                elif action == "restart": self.start_game(self.current_mode_size, self.current_win_len)
                elif action == "quit": 
                    pygame.quit()
                    exit()
                return

        if self.state == "playing":
            board_rect = pygame.Rect(20, 20, self.WIDTH - 40, self.WIDTH - 40)
            if board_rect.collidepoint(pos):
                size = self.game.size
                square_size = board_rect.width // size
                
                # Sửa lại công thức tính dòng cột để chính xác hơn với lưới động
                col = int((pos[0] - board_rect.left) / square_size)
                row = int((pos[1] - board_rect.top) / square_size)
                
                # Bảo vệ biên (nếu click vào đúng đường kẻ rìa ngoài cùng)
                if row >= size: row = size - 1
                if col >= size: col = size - 1
                
                current_p = self.game.players[self.game.turn % 2]
                if isinstance(current_p, Player):
                    self.make_move(row, col, current_p)

    # --- XỬ LÝ NƯỚC ĐI ---
    def make_move(self, row, col, player):
        if 0 <= row < self.game.size and 0 <= col < self.game.size and self.game.board[row][col] == " ":
            self.game.board[row][col] = player.symbol
            self.last_move = (row, col)
            
            if self.game.check_win(row, col, player.symbol):
                self.winner = player
                self.state = "game_over"
                self.end_time = time.time()
                self.save_game_result()
            elif self.game.is_draw():
                self.winner = None
                self.state = "game_over"
                self.end_time = time.time()
                self.save_game_result()
            else:
                self.game.turn += 1

    # --- LƯU KẾT QUẢ TRÒ CHƠI ---
    def save_game_result(self):
        if not self.winner or self.winner.name != "Player":
            return

        duration = round(self.end_time - self.start_time, 2)
        
        # Text độ khó
        diff_text = "Easy"
        if self.difficulty == 2: diff_text = "Medium"
        elif self.difficulty == 3: diff_text = "Hard"
        
        # Score: Hard > Medium > Easy
        base_score = self.difficulty * 1000
        time_bonus = max(0, 500 - int(duration))
        total_score = base_score + time_bonus
        
        entry = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "board_size": self.game.size, # <-- QUAN TRỌNG: Lưu size để lọc
            "difficulty": diff_text,      # Lưu tên độ khó để hiển thị
            "duration": duration,
            "score": total_score
        }
        
        self.scores.append(entry)
        self.save_scores()

    # --- VÒNG LẶP CHÍNH CỦA GAME ---
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            elif self.state == "playing" or self.state == "game_over":
                self.draw_game_board()
                
                if self.state == "playing":
                    current_p = self.game.players[self.game.turn % 2]
                    if isinstance(current_p, Bot):
                        # Vẽ board trước khi bot suy nghĩ để không bị trắng màn hình
                        pygame.display.flip() 
                        
                        # Cho bot suy nghĩ
                        row, col = current_p.move(self.game.board, self.game)
                        
                        # Bot đánh (nếu bot không trả về None)
                        if row is not None and col is not None:
                            self.make_move(row, col, current_p)
                        else:
                            # Trường hợp hiếm: bàn cờ đầy hoặc lỗi
                            pass 
                        pygame.event.clear()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = GameUI()
    game.run()
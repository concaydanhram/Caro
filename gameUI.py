import pygame
import time
import os
import json
import ctypes
import threading
import copy

from player import Player
from bot import Bot
from game_logic import GameLogic

class GameUI:
    def __init__(self):
        pygame.init()
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("simple-tic-tac-toe")
        except:
            pass
            
        self.WIDTH, self.HEIGHT = 550, 750
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Simple Tic Tac Toe with Minimax AI")
        self.clock = pygame.time.Clock()

        self.state = "menu"
        
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

        self.game = None
        self.winner = None
        self.start_time = None
        self.end_time = None
        self.score_file = "scores.json"
        self.scores = []
        self.load_scores()
        self.bot_thread = None
        self.bot_move_result = None
        self.last_move = None 
        self.btn_rects = {}
        self.view_mode = 3
        self.current_mode_size = 3 
        self.current_win_len = 3
        self.difficulty = 1
        
        # Mặc định bật cắt tỉa Alpha-Beta
        self.use_pruning = True

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
        list_3 = [s for s in self.scores if s.get('board_size') == 3]
        list_8 = [s for s in self.scores if s.get('board_size') == 8]
        
        list_3 = sorted(list_3, key=lambda x: x['score'], reverse=True)[:10]
        list_8 = sorted(list_8, key=lambda x: x['score'], reverse=True)[:10]
        
        self.scores = list_3 + list_8
        
        with open(self.score_file, 'w') as f:
            json.dump(self.scores, f, indent=4)

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

    def draw_text_centered(self, text, font, color, y_pos):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(self.WIDTH // 2, y_pos))
        self.screen.blit(surf, rect)

    def draw_menu(self):
        self.screen.fill(self.COLORS['bg'])
        self.btn_rects = {} 

        self.draw_text_centered("TIC TAC TOE", self.FONT_BIG, self.COLORS['text'], 60)
        self.draw_text_centered("SELECT DIFFICULTY", self.FONT_REG, self.COLORS['text'], 110)
        
        diff_y = 140
        diff_w = 100
        diff_h = 40
        gap = 20
        start_x = (self.WIDTH - (3 * diff_w + 2 * gap)) // 2

        levels = [("EASY", 1), ("MEDIUM", 2), ("HARD", 3)]
        
        for i, (label, level) in enumerate(levels):
            x = start_x + i * (diff_w + gap)
            rect = (x, diff_y, diff_w, diff_h)
            
            if self.difficulty == level:
                color = self.COLORS['win']
                text_color = (255, 255, 255)
            else:
                color = (189, 195, 199)
                text_color = self.COLORS['text']

            rect_obj = pygame.Rect(rect)
            pygame.draw.rect(self.screen, color, rect_obj, border_radius=8)
            
            text_surf = self.FONT_SMALL.render(label, True, text_color)
            text_rect = text_surf.get_rect(center=rect_obj.center)
            self.screen.blit(text_surf, text_rect)
            self.btn_rects[f"diff_{level}"] = rect_obj

        # Bật tắt cắt tỉa Alpha-Beta
        pruning_y = 210
        pruning_text = "Alpha-Beta: ON" if self.use_pruning else "Alpha-Beta: OFF"
        pruning_color = self.COLORS['win'] if self.use_pruning else self.COLORS['lose']
        
        self.draw_button(pruning_text, ((self.WIDTH - 250)//2, pruning_y, 250, 45), 
                         pruning_color, pruning_color, "toggle_pruning")

        self.draw_text_centered("SELECT MODE", self.FONT_MED, self.COLORS['text'], 300)

        btn_width, btn_height = 420, 65
        center_x = (self.WIDTH - btn_width) // 2
        
        self.draw_button("Classic (3x3 - Win 3)", (center_x, 340, btn_width, btn_height), 
                         self.COLORS['btn_default'], self.COLORS['btn_hover'], "mode_3x3")
        
        self.draw_button("Big Board (8x8 - Win 5)", (center_x, 420, btn_width, btn_height), 
                         self.COLORS['btn_default'], self.COLORS['btn_hover'], "mode_8x8")

        self.draw_button("Leaderboard", (center_x, 500, btn_width, btn_height), 
                         (149, 165, 166), (127, 140, 141), "view_leaderboard") 

        self.draw_button("Quit", (center_x, 580, btn_width, btn_height), 
                         (231, 76, 60), (192, 57, 43), "quit")

    def draw_leaderboard(self):
        self.screen.fill(self.COLORS['bg'])
        self.btn_rects = {}
        
        self.draw_text_centered("LEADERBOARD", self.FONT_BIG, self.COLORS['text'], 50)
        
        tab_y = 90
        tab_w = 160
        tab_h = 40
        gap = 20
        start_x = (self.WIDTH - (2 * tab_w + gap)) // 2
        
        color_3 = self.COLORS['btn_default'] if self.view_mode == 3 else (189, 195, 199)
        self.draw_button("3x3 Board", (start_x, tab_y, tab_w, tab_h), 
                         color_3, color_3, "view_3x3")
        
        color_8 = self.COLORS['btn_default'] if self.view_mode == 8 else (189, 195, 199)
        self.draw_button("8x8 Board", (start_x + tab_w + gap, tab_y, tab_w, tab_h), 
                         color_8, color_8, "view_8x8")

        header_y = 150
        pygame.draw.line(self.screen, self.COLORS['text'], (50, header_y + 30), (550, header_y + 30), 2)
        
        header_font = self.FONT_MED
        self.screen.blit(header_font.render("Diff", True, self.COLORS['text']), (80, header_y))
        self.screen.blit(header_font.render("Time", True, self.COLORS['text']), (250, header_y))
        self.screen.blit(header_font.render("Date", True, self.COLORS['text']), (400, header_y))
        
        current_list = [s for s in self.scores if s.get('board_size') == self.view_mode]
        current_list = sorted(current_list, key=lambda x: x['score'], reverse=True)
        
        start_y = 200
        if not current_list:
            self.draw_text_centered("No records yet!", self.FONT_SMALL, self.COLORS['text'], start_y + 20)
            
        for i, entry in enumerate(current_list):
            if i >= 10: break 
            
            if i in [0, 1, 2]: color = (241, 196, 15)
            else: color = self.COLORS['text']
            
            date_short = entry['date'][5:16]
            diff_text = entry.get('difficulty', 'Unknown') 
        
            rank_str = f"{i+1}. {diff_text}"
            self.screen.blit(self.FONT_SMALL.render(rank_str, True, color), (60, start_y + i * 45))
            
            time_str = f"{entry['duration']}s"
            self.screen.blit(self.FONT_SMALL.render(time_str, True, color), (260, start_y + i * 45))
            
            self.screen.blit(self.FONT_SMALL.render(date_short, True, color), (400, start_y + i * 45))

        self.draw_button("Back to Menu", (self.WIDTH//2 - 125, self.HEIGHT - 100, 250, 55), 
                         self.COLORS['btn_default'], self.COLORS['btn_hover'], "back_menu")

    def draw_game_board(self):
        self.screen.fill(self.COLORS['bg'])
        self.btn_rects = {}
        
        board_rect = pygame.Rect(20, 20, self.WIDTH - 40, self.WIDTH - 40)
        pygame.draw.rect(self.screen, self.COLORS['board_bg'], board_rect)
        pygame.draw.rect(self.screen, self.COLORS['text'], board_rect, 3)

        size = self.game.size
        square_size = board_rect.width // size

        for i in range(1, size):
            start_pos = (board_rect.left + i * square_size, board_rect.top)
            end_pos = (board_rect.left + i * square_size, board_rect.bottom)
            pygame.draw.line(self.screen, self.COLORS['line'], start_pos, end_pos, 2)
            
            start_pos = (board_rect.left, board_rect.top + i * square_size)
            end_pos = (board_rect.right, board_rect.top + i * square_size)
            pygame.draw.line(self.screen, self.COLORS['line'], start_pos, end_pos, 2)

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

        if self.game and self.game.win_line:
            (start_r, start_c), (end_r, end_c) = self.game.win_line
            start_x = board_rect.left + start_c * square_size + square_size // 2
            start_y = board_rect.top + start_r * square_size + square_size // 2
            end_x = board_rect.left + end_c * square_size + square_size // 2
            end_y = board_rect.top + end_r * square_size + square_size // 2
            
            line_color = (46, 204, 113) 
            line_width = 8 
            
            pygame.draw.line(self.screen, line_color, (start_x, start_y), (end_x, end_y), line_width)
            pygame.draw.circle(self.screen, line_color, (start_x, start_y), line_width // 2)
            pygame.draw.circle(self.screen, line_color, (end_x, end_y), line_width // 2)
        
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

        # Hiển thị thống kê Bot nếu có
        bot_player = None
        for p in self.game.players:
            if isinstance(p, Bot):
                bot_player = p
                break

        # Khi bot đang suy nghĩ, hiển thị số node đã duyệt
        if self.state == "playing" and bot_player and self.bot_thread and self.bot_thread.is_alive():
            stats_text = f"Nodes visited: {bot_player.nodes_visited}"
            self.draw_text_centered(stats_text, self.FONT_SMALL, (127, 140, 141), panel_y + 65)
        # Khi bot xong, hiển thị thời gian suy nghĩ lần trước và số node đã duyệt
        else:
            stats_text = f"Last think time: {bot_player.last_think_time}s, Nodes visited: {bot_player.nodes_visited}"
            self.draw_text_centered(stats_text, self.FONT_SMALL, (127, 140, 141), panel_y + 65)

        btn_y = panel_y + 100
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

    def draw_symbol(self, symbol, x, y, size):
        radius = size // 3
        width = max(3, size // 15) 
        if symbol == 'X':
            color = self.COLORS['x_color']
            offset = radius - 5
            pygame.draw.line(self.screen, color, (x - offset, y - offset), (x + offset, y + offset), width)
            pygame.draw.line(self.screen, color, (x + offset, y - offset), (x - offset, y + offset), width)
        elif symbol == 'O':
            color = self.COLORS['o_color']
            pygame.draw.circle(self.screen, color, (x, y), radius, width)

    def start_game(self, size, win_length):
        self.current_mode_size = size
        self.current_win_len = win_length
        self.game = GameLogic(size, win_length)
        
        actual_depth = 3  
        if size == 8:  
            if self.difficulty == 1: actual_depth = 1
            elif self.difficulty == 2: actual_depth = 2
            else: actual_depth = 4
        else:
            if self.difficulty == 1: actual_depth = 1
            elif self.difficulty == 2: actual_depth = 3
            else: actual_depth = 9 
            
        print(f"Game started: Size {size}x{size}, Diff: {self.difficulty}, Depth: {actual_depth}, Pruning: {self.use_pruning}")

        self.game.players = [
            Player("Player", "O"),
            Bot("Bot", "X", max_depth=actual_depth, use_pruning=self.use_pruning) 
        ]
        self.game.turn = 0
        self.state = "playing"
        self.winner = None
        self.last_move = None
        self.start_time = time.time()
        self.end_time = None

    def handle_click(self, pos):
        for action, rect in self.btn_rects.items():
            if rect.collidepoint(pos):
                if action == "view_3x3": self.view_mode = 3
                elif action == "view_8x8": self.view_mode = 8
                elif action == "diff_1": self.difficulty = 1
                elif action == "diff_2": self.difficulty = 2
                elif action == "diff_3": self.difficulty = 3
                elif action == "toggle_pruning": self.use_pruning = not self.use_pruning
                elif action == "mode_3x3": self.start_game(3, 3)
                elif action == "mode_8x8": self.start_game(8, 5)
                elif action == "view_leaderboard": 
                    self.state = "leaderboard"
                    self.view_mode = 3
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
                
                col = int((pos[0] - board_rect.left) / square_size)
                row = int((pos[1] - board_rect.top) / square_size)
                
                if row >= size: row = size - 1
                if col >= size: col = size - 1
                
                current_p = self.game.players[self.game.turn % 2]
                if isinstance(current_p, Player):
                    self.make_move(row, col, current_p)

    def make_move(self, row, col, player):
        if 0 <= row < self.game.size and 0 <= col < self.game.size and self.game.board[row][col] == " ":
            self.game.board[row][col] = player.symbol
            self.last_move = (row, col)
            
            if self.game.check_win(row, col, player.symbol, board=None, update_ui=True):
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

    def save_game_result(self):
        if not self.winner or self.winner.name != "Player":
            return

        duration = round(self.end_time - self.start_time, 2)
        
        diff_text = "Easy"
        if self.difficulty == 2: diff_text = "Medium"
        elif self.difficulty == 3: diff_text = "Hard"
        
        base_score = self.difficulty * 1000
        time_bonus = max(0, 500 - int(duration))
        total_score = base_score + time_bonus
        
        entry = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "board_size": self.game.size,
            "difficulty": diff_text,
            "duration": duration,
            "score": total_score
        }
        
        self.scores.append(entry)
        self.save_scores()

    # --- HÀM HỖ TRỢ ĐA LUỒNG ---
    def run_bot_calculation(self, bot_player):
        # Tạo bản sao của game để bot tính toán (tránh xung đột dữ liệu)
        game_clone = copy.deepcopy(self.game)
        # Hàm move của bot có thể mất thời gian, ta cho chạy trong luồng riêng
        row, col = bot_player.move(game_clone.board, game_clone)
        # Lưu kết quả để luồng chính lấy ra dùng
        self.bot_move_result = (row, col)

    # --- VÒNG LẶP CHÍNH CỦA GAME ---
    def run(self):
        running = True
        while running:
            # 1. Xử lý sự kiện, ngay cả khi bot đang suy nghĩ
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Chỉ cho phép click khi không phải lượt Bot
                    if self.state == "playing":
                        current_p = self.game.players[self.game.turn % 2]
                        if not isinstance(current_p, Bot):
                            self.handle_click(event.pos)
                    else:
                        self.handle_click(event.pos)

            # 2. Vẽ giao diện
            if self.state == "menu":
                self.draw_menu()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            
            elif self.state == "playing" or self.state == "game_over":
                self.draw_game_board()
                
                if self.state == "playing":
                    current_p = self.game.players[self.game.turn % 2]

                    # LOGIC ĐA LUỒNG CHO BOT
                    if isinstance(current_p, Bot):
                        # TH1: Chưa bắt đầu tính toán -> Tạo luồng mới
                        if self.bot_thread is None:
                            # Reset kết quả cũ
                            self.bot_move_result = None 
                            # Tạo luồng mới với hàm run_bot_calculation
                            self.bot_thread = threading.Thread(target=self.run_bot_calculation, args=(current_p,))
                            # Bắt đầu chạy
                            self.bot_thread.start()
                        
                        # TH2: Luồng đang chạy -> Không làm gì cả, game chính vẫn tiếp tục vẽ
                        elif self.bot_thread.is_alive():
                            pass 
                        
                        # TH3: Luồng đã chạy xong -> Lấy kết quả và đánh
                        else:
                            if self.bot_move_result:
                                row, col = self.bot_move_result
                                if row is not None and col is not None:
                                    self.make_move(row, col, current_p)
                            
                            # Dọn dẹp để chuẩn bị cho lượt sau
                            self.bot_thread = None
                            self.bot_move_result = None

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = GameUI()
    game.run()
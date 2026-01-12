# scenes.py
import pygame
from game_logic import GameLogic # Giả sử bạn để class Game ở file game_logic.py
from player import Player
from bot import Bot

class MenuScene:
    def __init__(self, app):
        self.app = app
        self.font = pygame.font.Font(None, 36)
        
        # Các lựa chọn mặc định
        self.mode = "PvE"      # hoặc "PvP"
        self.depth = 3         # Độ khó
        self.use_pruning = True # Alpha-beta pruning
        
        # UI đơn giản (Text)
        self.options = ["Mode (M): ", "Depth (D): ", "Pruning (P): ", "ENTER to Start"]

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # 1. Chọn chế độ
                if event.key == pygame.K_m:
                    self.mode = "PvP" if self.mode == "PvE" else "PvE"
                
                # 2. Chọn độ khó (tăng dần, max 5 rồi về 1)
                elif event.key == pygame.K_d:
                    self.depth = self.depth + 1 if self.depth < 5 else 1
                
                # 3. Bật/Tắt Pruning
                elif event.key == pygame.K_p:
                    self.use_pruning = not self.use_pruning
                
                # 4. Bắt đầu game (QUAN TRỌNG: Chuyển dữ liệu sang GameScene)
                elif event.key == pygame.K_RETURN:
                    self.start_game()

    def start_game(self):
        # Tạo đối tượng Game mới
        game = Game()
        
        p1 = Player("X") # Người luôn là X
        if self.mode == "PvP":
            p2 = Player("O")
        else:
            p2 = Bot("O", depth=self.depth, pruning=self.use_pruning)

        game.players = [p1, p2] # Thêm người chơi vào list
        
        # Chuyển cảnh sang GameScene với game đã config
        self.app.active_scene = GameScene(self.app, game)

    def update(self):
        pass # Menu thường không cần update logic liên tục trừ animation

    def render(self, screen):
        screen.fill((30, 30, 30))
        
        # Hiển thị text trạng thái hiện tại
        texts = [
            f"Mode (Press M): {self.mode}",
            f"Depth (Press D): {self.depth}",
            f"Pruning (Press P): {'ON' if self.use_pruning else 'OFF'}",
            "Press ENTER to Start"
        ]
        
        for i, text in enumerate(texts):
            surf = self.font.render(text, True, (255, 255, 255))
            screen.blit(surf, (50, 50 + i * 50))

# --- Game Scene ---
class GameScene:
    def __init__(self, app, game):
        self.app = app
        self.game = game # Nhận game đã có players từ MenuScene chuyển sang

    def handle_input(self, events):
        for event in events:
            # Logic xử lý click chuột để đánh cờ...
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Xử lý nước đi ở đây
                pass
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Quay về menu
                self.app.active_scene = MenuScene(self.app)

    def update(self):
        # Đây là chỗ gây lỗi cũ của bạn
        # Bây giờ self.game.players đã có dữ liệu nên không lỗi nữa
        current_p = self.game.players[self.game.turn % 2]
        
        # Nếu là AI thì gọi AI đi
        if isinstance(current_p, Bot) and not self.game.game_over:
            move = current_p.get_move(self.game.board)
            self.game.make_move(move)

    def render(self, screen):
        screen.fill((200, 200, 200))
        # Code vẽ bàn cờ...
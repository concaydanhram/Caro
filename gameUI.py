import pygame
import random
from player import Player
from bot import Bot
from tic_tac_toe import TicTacToe
from five_in_a_row import FiveInARow

class GameUI:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 700  # Tăng chiều cao để có không gian hiển thị trạng thái
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Caro")
        self.clock = pygame.time.Clock()

        self.state = "menu"
        self.game = None
        self.LINE_COLOR = (0, 0, 0)
        self.BG_COLOR = (240, 240, 240)
        self.SYMBOL_COLORS = {'X': (255, 0, 0), 'O': (0, 0, 255)}
        self.FONT = pygame.font.Font(None, 74)
        self.STATUS_FONT = pygame.font.Font(None, 36) # Font cho thông báo trạng thái
        self.winner = None # Lưu người thắng cuộc

    def draw_menu(self):
        self.screen.fill(self.BG_COLOR)

        title = self.FONT.render("CHON CHE DO", True, self.LINE_COLOR)
        self.screen.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 100))

        text1 = self.FONT.render("1. Tic Tac Toe (3x3)", True, self.LINE_COLOR)
        text2 = self.FONT.render("2. Five in a Row (15x15)", True, self.LINE_COLOR)

        self.screen.blit(text1, (self.WIDTH // 2 - text1.get_width() // 2, 250))
        self.screen.blit(text2, (self.WIDTH // 2 - text2.get_width() // 2, 350))

        pygame.display.flip()

    def draw_game(self):
        BOARD_H = self.WIDTH
        self.screen.fill(self.BG_COLOR)

        if not self.game:
            return

        size = self.game.size
        self.SQUARE_SIZE = BOARD_H // size

        # 1. Vẽ lưới
        for i in range(size + 1):
            pygame.draw.line(self.screen, self.LINE_COLOR,
                             (i * self.SQUARE_SIZE, 0),
                             (i * self.SQUARE_SIZE, BOARD_H), 2)
            pygame.draw.line(self.screen, self.LINE_COLOR,
                             (0, i * self.SQUARE_SIZE),
                             (self.WIDTH, i * self.SQUARE_SIZE), 2)

        for r in range(size):
            for c in range(size):
                symbol = self.game.board[r][c]
                if symbol != " ":
                    center_x = c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    center_y = r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    color = self.SYMBOL_COLORS.get(symbol, self.LINE_COLOR)

                    MARK_SIZE = self.SQUARE_SIZE // 3

                    if symbol == 'X':
                        pygame.draw.line(self.screen, color, (center_x - MARK_SIZE, center_y - MARK_SIZE), (center_x + MARK_SIZE, center_y + MARK_SIZE), 5)
                        pygame.draw.line(self.screen, color, (center_x + MARK_SIZE, center_y - MARK_SIZE), (center_x - MARK_SIZE, center_y + MARK_SIZE), 5)
                    elif symbol == 'O':
                        pygame.draw.circle(self.screen, color, (center_x, center_y), MARK_SIZE, 5)

        self.draw_status()
        pygame.display.flip()

    def draw_status(self):
        status_rect = pygame.Rect(0, 600, self.WIDTH, 100)
        pygame.draw.rect(self.screen, (200, 200, 200), status_rect)

        player_info = {}
        for p in self.game.players:
            if isinstance(p, Player):
                player_info['Player'] = p.symbol
            elif isinstance(p, Bot):
                player_info['Bot'] = p.symbol

        if self.state == "playing":
            current_player = self.game.players[self.game.turn % 2]
            msg = f"Turn: {current_player.name} ({current_player.symbol})"
        elif self.state == "game_over":
            if self.winner:
                msg = f"{self.winner.name} ({self.winner.symbol}) WIN!"
            else:
                msg = "DRAW!"
        else:
            msg = "Start!"

        # Hiển thị thông tin người chơi (quân X/O)
        info_text = f"You: {player_info.get('Player', '?')}, Bot: {player_info.get('Bot', '?')}"
        info_surface = self.STATUS_FONT.render(info_text, True, self.LINE_COLOR)
        self.screen.blit(info_surface, (10, 610))

        # Hiển thị trạng thái game
        status_surface = self.STATUS_FONT.render(msg, True, self.LINE_COLOR)
        self.screen.blit(status_surface, (10, 650))

        # Nếu game kết thúc, hiển thị nút chơi lại đơn giản
        if self.state == "game_over":
            restart_text = self.STATUS_FONT.render("Play Again", True, (0, 100, 0))
            self.screen.blit(restart_text, (self.WIDTH - restart_text.get_width() - 10, 650))


    def handle_mouse_click(self, pos):
        if self.state == "playing":
            size = self.game.size
            self.SQUARE_SIZE = self.WIDTH // size

            mouse_x, mouse_y = pos
            # Chỉ xử lý click trong khu vực bàn cờ
            if mouse_y >= self.WIDTH: return

            col = mouse_x // self.SQUARE_SIZE
            row = mouse_y // self.SQUARE_SIZE

            current_player = self.game.players[self.game.turn % 2]

            if isinstance(current_player, Player):
                self.make_move(row, col, current_player)
        elif self.state == "game_over":
            # Nếu game kết thúc, chuyển về menu để chọn lại
            self.state = "menu"
            self.winner = None
            self.game = None


    def make_move(self, row, col, player):
        if 0 <= row < self.game.size and 0 <= col < self.game.size and self.game.board[row][col] == " ":
            self.game.board[row][col] = player.symbol

            if self.game.check_win(row, col, player.symbol):
                self.winner = player
                self.state = "game_over"
            elif self.game.is_draw():
                self.winner = None
                self.state = "game_over"
            else:
                self.game.turn += 1

    def handle_menu_click(self, pos):
        # Xác định loại game dựa trên vị trí click menu
        if pos[1] < self.HEIGHT / 2:
            self.game = TicTacToe()
        else:
            self.game = FiveInARow()

        self.winner = None

        # Thiết lập ngẫu nhiên người đi trước, X đi trước
        if random.choice([True, False]):
            p1 = Player("Player", "X") # Người chơi đi trước (X)
            p2 = Bot("Bot", "O")
        else:
            p1 = Bot("Bot", "X") # Máy đi trước (X)
            p2 = Player("Player", "O")

        self.game.players = [p1, p2]
        self.game.turn = 0
        self.state = "playing"


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "menu":
                        self.handle_menu_click(event.pos)
                    else:
                        self.handle_mouse_click(event.pos)

            if self.state == "playing" and self.game:
                current_player = self.game.players[self.game.turn % 2]
                if isinstance(current_player, Bot):
                    row, col = current_player.move(self.game.board, self.game)
                    self.make_move(row, col, current_player)

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "playing" or self.state == "game_over":
                self.draw_game()

            self.clock.tick(60)

        pygame.quit()
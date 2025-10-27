import tkinter as tk
from tkinter import messagebox
from tic_tac_toe import TicTacToe
from bot import Bot
from player import Player

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro 3x3 (Tic Tac Toe)")
        self.game = TicTacToe()

        # Người chơi & Bot
        self.player = Player("Bạn", "X")
        self.bot = Bot("Máy", "O")
        self.game.players = [self.player, self.bot]

        # Tạo khung và bảng
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.frame, text=" ", width=5, height=2, font=("Arial", 24, "bold"),
                                command=lambda r=r, c=c: self.handle_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

        self.info_label = tk.Label(self.root, text="Lượt của bạn (X)", font=("Arial", 14))
        self.info_label.pack(pady=10)

    def handle_click(self, r, c):
        # Người chơi đánh
        if self.game.board[r][c] != " ":
            return  # Ô đã có nước đi
        self.game.board[r][c] = self.player.symbol
        self.buttons[r][c].config(text=self.player.symbol, state="disabled")

        if self.game.check_win(r, c, self.player.symbol):
            self.end_game("Bạn thắng!")
            return
        if self.game.is_draw():
            self.end_game("Hòa!")
            return

        self.info_label.config(text="Lượt của máy (O)")
        self.root.after(500, self.bot_move)  # Bot đánh sau 0.5s

    def bot_move(self):
        r, c = self.bot.move(self.game.board, self.game)
        self.game.board[r][c] = self.bot.symbol
        self.buttons[r][c].config(text=self.bot.symbol, state="disabled")

        if self.game.check_win(r, c, self.bot.symbol):
            self.end_game("Máy thắng!")
            return
        if self.game.is_draw():
            self.end_game("Hòa!")
            return

        self.info_label.config(text="Lượt của bạn (X)")

    def end_game(self, message):
        messagebox.showinfo("Kết thúc ván", message)
        self.reset_board()

    def reset_board(self):
        self.game = TicTacToe()
        self.game.players = [self.player, self.bot]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=" ", state="normal")
        self.info_label.config(text="Lượt của bạn (X)")

if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()

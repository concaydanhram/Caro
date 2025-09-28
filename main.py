from player import Player
from tic_tac_toe import TicTacToe
from five_in_a_row import FiveInARow

def main():
    print("Chọn trò chơi:")
    print("1. Tic Tac Toe (3x3, 3 liên tiếp thắng)")
    print("2. Five in a Row (15x15, 5 liên tiếp thắng)")

    choice = input("Nhập lựa chọn (1/2): ")

    p1 = Player("Người chơi 1", "X")
    p2 = Player("Người chơi 2", "O")
    players = [p1, p2]

    if choice == "1":
        game = TicTacToe()
    elif choice == "2":
        game = FiveInARow()
    else:
        print("Lựa chọn không hợp lệ!")
        return

    game.play(players)

if __name__ == "__main__":
    main()

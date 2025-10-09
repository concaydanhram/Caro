import random
from player import Player
from bot import Bot
from tic_tac_toe import TicTacToe
from five_in_a_row import FiveInARow

def main():
    print("Chọn trò chơi:")
    print("1. Tic Tac Toe (3x3, 3 liên tiếp thắng)")
    print("2. Five in a Row (15x15, 5 liên tiếp thắng)")
    choice = input("Nhập lựa chọn (1/2): ")

    if choice == "1":
        game = TicTacToe()
    elif choice == "2":
        game = FiveInARow()
    else:
        print("Lựa chọn không hợp lệ!")
        return

    print("Chọn chế độ:")
    print("1. Chơi với máy")
    print("2. Chơi với người")
    choice = input("Nhập lựa chọn (1/2): ")

    if choice == "1":
            # random chọn ai đi trước
        if random.choice([True, False]):
            p1 = Player("Người chơi", "X")
            p2 = Bot("Máy", "O")
            print("Người chơi đi trước với ký hiệu X")
        else:
            p1 = Bot("Máy", "X")
            p2 = Player("Người chơi", "O")
            print("Máy đi trước với ký hiệu X")
        players = [p1, p2]
        game.play(players)

    elif choice == "2":
        names = ["Người chơi 1", "Người chơi 2"]
        random.shuffle(names)
        p1 = Player(names[0], "X")  # đi trước
        p2 = Player(names[1], "O")
        print(f"{p1.name} đi trước với ký hiệu X")
        players = [p1, p2]
        game.play(players)

    else:
        print("Lựa chọn không hợp lệ!")
        return


if __name__ == "__main__":
    main()

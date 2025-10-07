class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    # Nước đi của người chơi
    def move(self, board, game=None):
        while True:
            try:
                row, col = map(int, input("Nhập hàng và cột (0-2): ").split())
                if 0 <= row < len(board) and 0 <= col < len(board):
                    return row, col
                else:
                    print("Tọa độ không hợp lệ, nhập lại!")
            except ValueError:
                print("Sai định dạng, hãy nhập hai số cách nhau bởi khoảng trắng.")

import chess

class Board:
    def __init__(self):
        self.board = chess.Board()
        print(self.board)

if __name__ == '__main__':
    board = Board()
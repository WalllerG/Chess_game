import pygame
import chess
from PIL import Image

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 8
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE
COLOR1 = pygame.Color(225, 216, 17)
COLOR2 = pygame.Color(255, 246, 196)

def draw_board(screen):
    for row in range(8):
        for col in range(8):
            color = COLOR1 if (row + col) % 2 == 0 else COLOR2
            pygame.draw.rect(screen, color,
                             pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE,
                                         SQUARE_SIZE, SQUARE_SIZE))
def draw_pieces(screen, board, piece_images):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            col = chess.square_file(square)
            row = 7 - chess.square_rank(square)
            img = piece_images[piece.symbol()]
            screen.blit(img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def load_pieces():
    pieces = {}
    symbols = ['P','R','N','B','Q','K','p','r','n','b','q','k']
    for s in symbols:
        prefix = 'w' if s.isupper() else 'b'
        image = Image.open(f'images/{prefix}{s.upper()}.png')
        image.save('temp.bmp')
        img = pygame.transform.scale(pygame.image.load('temp.bmp'), (SQUARE_SIZE, SQUARE_SIZE))
        pieces[s] = img
    return pieces

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    board = chess.Board()
    pieces = load_pieces()
    selected_square = None
    running = True
    while running:
        draw_board(screen)
        draw_pieces(screen, board, pieces)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                clicked_square = chess.square(col, 7 - row)

                if selected_square is None:
                    if board.piece_at(clicked_square):
                        selected_square = clicked_square
                else:
                    move = chess.Move(selected_square, clicked_square)
                    if move in board.legal_moves:
                        board.push(move)
                    selected_square = None
        if board.is_checkmate():
            print("Checkmate!")
            running = False
        elif board.is_stalemate():
            print("Stalemate!")
            running = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
if __name__ == '__main__':
    main()


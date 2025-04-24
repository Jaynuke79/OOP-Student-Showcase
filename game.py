import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'event_classes'))

# Re-imports and setup after kernel reset
import pygame
import random
from chess_piece import ChessPiece, Pawn, Rook, Knight
from chess_piece import Bishop, King, Queen
from promote_to_queen import PromoteToQueenEvent
from freeze_piece import FreezePieceEvent

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
BOARD_HEIGHT = WIDTH
FONT = pygame.font.SysFont('Arial', 20)
dragging_piece = None
offset_x = 0
offset_y = 0

# Colors
WHITE = (245, 245, 245)
BLACK = (40, 40, 40)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
BLUE = (50, 50, 255)
RED = (255, 50, 50)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Party")


pieces = [Pawn("Pawn", "White", 1, 0, 8, 1, "forward"),
          Pawn("Pawn", "White", 1, 1, 8, 1, "forward"), 
          Pawn("Pawn", "White", 1, 2, 8, 1, "forward"), 
          Pawn("Pawn", "White", 1, 3, 8, 1, "forward"), 
          Pawn("Pawn", "White", 1, 4, 8, 1, "forward"), 
          Pawn("Pawn", "White", 1, 5, 8, 1, "forward"), 
          Pawn("Pawn", "White", 1, 6, 8, 1, "forward"), 
          Pawn("Pawn", "White", 1, 7, 8, 1, "forward"),

          Rook("Rook", "White", 0, 0, 2, 8, "line"),
          Rook("Rook", "White", 0, 7, 2, 8, "line"),

          Knight("Knight", "White", 0, 1, 2, 5, "L"),
          Knight("Knight", "White", 0, 6, 2, 5, "L"),

          Bishop("Bishop", "White", 0, 2, 2, 8, "diagonal"),
          Bishop("Bishop", "White", 0, 5, 2, 8, "diagonal"),

          King("King", "White", 0, 4, 1, 1, "any"),
          Queen("Queen", "White", 0, 3, 1, 8, "any"),


          Pawn("Pawn", "Black", 6, 0, 8, 1, "forward"),
          Pawn("Pawn", "Black", 6, 1, 8, 1, "forward"), 
          Pawn("Pawn", "Black", 6, 2, 8, 1, "forward"), 
          Pawn("Pawn", "Black", 6, 3, 8, 1, "forward"), 
          Pawn("Pawn", "Black", 6, 4, 8, 1, "forward"), 
          Pawn("Pawn", "Black", 6, 5, 8, 1, "forward"), 
          Pawn("Pawn", "Black", 6, 6, 8, 1, "forward"), 
          Pawn("Pawn", "Black", 6, 7, 8, 1, "forward"),

          Rook("Rook", "Black", 7, 0, 2, 8, "line"),
          Rook("Rook", "Black", 7, 7, 2, 8, "line"),

          Knight("Knight", "Black", 7, 1, 2, 5, "L"),
          Knight("Knight", "Black", 7, 6, 2, 5, "L"),

          Bishop("Bishop", "Black", 7, 2, 2, 8, "diagonal"),
          Bishop("Bishop", "Black", 7, 5, 2, 8, "diagonal"),

          King("King", "Black", 7, 4, 1, 1, "any"),
          Queen("Queen", "Black", 7, 3, 1, 8, "any"),
          ]

piece_images = { ("Pawn", "White"): pygame.image.load("assets/pieces/whitePawn.png"),
                 ("Pawn", "Black"): pygame.image.load("assets/pieces/blackPawn.png"),

                 ("Rook", "White"): pygame.image.load("assets/pieces/whiteRook.png"),
                 ("Rook", "Black"): pygame.image.load("assets/pieces/blackRook.png"),

                 ("Knight", "White"): pygame.image.load("assets/pieces/whiteKnight.png"),
                 ("Knight", "Black"): pygame.image.load("assets/pieces/blackKnight.png"),

                 ("King", "White"): pygame.image.load("assets/pieces/whiteKing.png"),
                 ("King", "Black"): pygame.image.load("assets/pieces/blackKing.png"),

                 ("Queen", "White"): pygame.image.load("assets/pieces/whiteQueen.png"),
                 ("Queen", "Black"): pygame.image.load("assets/pieces/blackQueen.png"),

                 ("Bishop", "White"): pygame.image.load("assets/pieces/whiteBishop.png"),
                 ("Bishop", "Black"): pygame.image.load("assets/pieces/blackBishop.png")
}

# Jpg scaling for tiles
for key in piece_images:
    piece_images[key] = pygame.transform.scale(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))

events = [FreezePieceEvent(), PromoteToQueenEvent()]
event_log = []

# Draw functions
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = GRAY if (row + col) % 2 == 0 else DARK_GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for piece in pieces:
        # center = (piece._col * SQUARE_SIZE + SQUARE_SIZE // 2, piece._row * SQUARE_SIZE + SQUARE_SIZE // 2)
        # color = BLUE if piece._color == "White" else RED
        # pygame.draw.circle(screen, color, center, 20)
        pos = (piece._col * SQUARE_SIZE, piece._row * SQUARE_SIZE)
        key = (piece._name, piece._color)
        image = piece_images.get(key)

        if image:
            if pos is None:
                    pos = (piece._col * SQUARE_SIZE, piece._row * SQUARE_SIZE)
            screen.blit(image, pos)

        if piece.is_frozen():
            # pygame.draw.circle(screen, BLACK, center, 10)
            overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            overlay.set_alpha(100)
            overlay.fill(BLACK)
            screen.blit(overlay, pos)

def draw_log():
    y = BOARD_HEIGHT + 10

    for i, msg in enumerate(event_log[-3:]):
        text_surface = FONT.render(msg, True, WHITE)
        screen.blit(text_surface, (10, y + i * 20))

def play_turn():
    messages = []

    board = Board(pieces)

    # Randomly select non-frozen piece
    movable_pieces = [p for p in pieces if not p.is_frozen()]
    if not movable_pieces:
        messages.append("All pieces are frozen!")
        return messages

    selected_piece = random.choice(movable_pieces)

    # Reduce frozen turns by 1
    for piece in pieces:
        if piece.is_frozen():
            piece.reduce_frozen()
            messages.append(f"{piece._name} is frozen.")

        
    if random.random() < 0.5:
        event = random.choice(events)

        if isinstance(event, PromoteToQueenEvent):
            result = event.apply(selected_piece, pieces)
        else:
            result = event.apply(selected_piece)
        
        messages.append(result)

    else:
        valid_moves = selected_piece.get_valid_moves(board)
        messages.append(f"{selected_piece._name} valid moves: {valid_moves}")
    
    return messages

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)
    draw_board()
    draw_pieces()
    draw_log()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            event_log.extend(play_turn())
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            row = mouse_y // SQUARE_SIZE
            col = mouse_x // SQUARE_SIZE

            for piece in reversed(pieces):
                if piece._row == row and piece._col == col and not piece.is_frozen():
                    dragging_piece = piece
                    offset_x = mouse_x - col * SQUARE_SIZE
                    offset_y = mouse_y - row * SQUARE_SIZE
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_piece:
                mouse_x, mouse_y = event.pos
                dragging_piece._col = max(0, min(COLS - 1, mouse_x // SQUARE_SIZE))
                dragging_piece._row = max(0, min(ROWS - 1, mouse_y // SQUARE_SIZE))
                dragging_piece = None
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            event_log.extend(play_turn())

    clock.tick(30)

pygame.quit()

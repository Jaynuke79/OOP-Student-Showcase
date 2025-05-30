import sys
import os
from typing import cast
import pygame
from pygame.surface import Surface
import random
from chess_piece import Pawn, Rook, Knight
from chess_piece import ChessPiece, Bishop, King, Queen
from board import Board

sys.path.append(os.path.join(os.path.dirname(__file__), 'event_classes'))
from promote_to_queen import PromoteToQueenEvent  # noqa: E402
from freeze_piece import FreezePieceEvent  # noqa: E402


def resource_path(relative_path: str) -> str:
    """Path to resource for dev or PyInstaller"""
    try:
        base_path = cast(str, getattr(sys, "_MEIPASS", os.path.abspath(".")))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
BG_COLOR = [0, 0, 20]
BG_DRIFT = [1, 1, 1]

# Captured Pieces
captured_white: list[ChessPiece] = []
captured_black: list[ChessPiece] = []
event_log: list[str] = []

# Conditions for victory
winner: str | None = None
game_over: bool = False

# Screen setup
screen = pygame.display.set_mode((WIDTH + 125, HEIGHT))
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

ap: str = "assets/pieces/"
ae: str = "assets/effects/"


def li(path: str) -> Surface:
    """
    Helper function for loading images
    """
    return pygame.image.load(resource_path(path)).convert_alpha()


piece_images = {
    ("Pawn", "White"): li(f"{ap}whitePawn.png"),
    ("Pawn", "Black"): li(f"{ap}blackPawn.png"),

    ("Rook", "White"): li(f"{ap}whiteRook.png"),
    ("Rook", "Black"): li(f"{ap}blackRook.png"),

    ("Knight", "White"): li(f"{ap}whiteKnight.png"),
    ("Knight", "Black"): li(f"{ap}blackKnight.png"),

    ("King", "White"): li(f"{ap}whiteKing.png"),
    ("King", "Black"): li(f"{ap}blackKing.png"),

    ("Queen", "White"): li(f"{ap}whiteQueen.png"),
    ("Queen", "Black"): li(f"{ap}blackQueen.png"),

    ("Bishop", "White"): li(f"{ap}whiteBishop.png"),
    ("Bishop", "Black"): li(f"{ap}blackBishop.png")
}

pts = pygame.transform.scale  # shortened
pil = pygame.image.load  # shortened
pdr = pygame.draw.rect  # shortened
rss_path = resource_path
promotion_overlay = pil(rss_path(f"{ae}promotion_sparkle.png"))
promotion_overlay = pts(promotion_overlay, (SQUARE_SIZE, SQUARE_SIZE))
frozen_overlay = pil(rss_path(f"{ae}frozen.png"))
frozen_overlay = pts(frozen_overlay, (SQUARE_SIZE, SQUARE_SIZE))


# Jpg scaling for tiles
for key in piece_images:
    piece_images[key] = pts(piece_images[key], (SQUARE_SIZE, SQUARE_SIZE))

events = [FreezePieceEvent(), PromoteToQueenEvent()]
event_log = []


# Draw functions
def draw_board() -> None:
    """
    Draws the chessboard
    """
    for row in range(ROWS):
        for col in range(COLS):
            color = GRAY if (row + col) % 2 == 0 else DARK_GRAY
            pdr(screen, color, (col * SQUARE_SIZE,
                row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Highlights all valid moves when dragging a piece
    if dragging_piece:
        for move_row, move_col in valid_drag_moves:
            highlight = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE),
                                       pygame.SRCALPHA)  # Opacity/Transparency
            highlight.fill((0, 255, 0, 100))  # Green color, 100 alpha
            screen.blit(highlight,
                        (move_col * SQUARE_SIZE, move_row * SQUARE_SIZE))


def draw_captured() -> None:
    """
    Draws a sidebar displaying all captured pieces during a game
    """
    sidebar_x = WIDTH
    sidebar_width = 125
    pdr(screen, BLACK, (WIDTH, 0, sidebar_width, HEIGHT))

    # Top half for captured White pieces
    y = 10
    screen.blit(FONT.render("White Captured:", True, WHITE),
                (sidebar_x + 5, y))
    y += 30
    for piece in captured_black:  # Captured from Black
        key = (piece.get_name(), "Black")
        image = piece_images.get(key)
        if image:
            small_image = pygame.transform.scale(image, (30, 30))
            screen.blit(small_image, (sidebar_x + 35, y))
            y += 35

    # Bottom half for captured Black pieces
    y = HEIGHT // 2 + 10
    screen.blit(FONT.render("Black Captured:", True, WHITE),
                (sidebar_x + 5, y))
    y += 30
    for piece in captured_white:  # Captured from White
        key = (piece.get_name(), "White")
        image = piece_images.get(key)
        if image:
            small_image = pygame.transform.scale(image, (30, 30))
            screen.blit(small_image, (sidebar_x + 35, y))
            y += 35


def draw_pieces() -> None:
    """
    Draws all chess pieces on the board
    """
    for piece in pieces:
        pos = (piece._col * SQUARE_SIZE, piece._row * SQUARE_SIZE)
        key = (piece._name, piece._color)
        image = piece_images.get(key)

        if image:
            if pos is None:
                pos = (piece._col * SQUARE_SIZE, piece._row * SQUARE_SIZE)
            screen.blit(image, pos)

        # Overlay for Promotion effect
        if hasattr(piece, "promoted") and piece.promoted:
            if hasattr(piece, "promotion_timer"):
                # Transparency transition
                alpha = int((cast(int, piece.promotion_timer) / 100) * 255)
                alpha = max(0, min(255, alpha))

                overlay_copy = promotion_overlay.copy()
                overlay_copy.set_alpha(alpha)

                screen.blit(overlay_copy, pos)

        if piece.is_frozen():
            # pygame.draw.circle(screen, BLACK, center, 10)
            overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            overlay.set_alpha(100)
            overlay.fill((0, 100, 255))
            screen.blit(overlay, pos)

        # Overlay for Frozen effect
        if hasattr(piece, "frozen_timer") and piece.frozen_timer is not None:
            alpha = int((piece.frozen_timer) / 100 * 255)
            alpha = max(0, min(255, alpha))

            frozen_copy = frozen_overlay.copy()
            frozen_copy.set_alpha(alpha)

            screen.blit(frozen_copy, pos)


def draw_log() -> None:
    """
    Displays log of actions taken on bottom of screen
    """
    y = BOARD_HEIGHT + 10

    for i, msg in enumerate(event_log[-3:]):
        text_surface = FONT.render(msg, True, WHITE)
        screen.blit(text_surface, (10, y + i * 20))


def draw_victory_screen() -> None:
    """
    Screen that appears if game has been won by either side
    """

    # Background changes color
    for i in range(3):
        BG_COLOR[i] += BG_DRIFT[i]

        if BG_COLOR[i] >= 100 or BG_COLOR[i] <= 20:
            BG_DRIFT[i] *= -1

    screen.fill(BG_COLOR)

    font = pygame.font.SysFont('Arial', 50)
    text = font.render(f"{winner} WINS!", True, (255, 255, 0))
    text_rect = text.get_rect(center=((WIDTH + 125) // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    small_font = pygame.font.SysFont('Arial', 24)
    subtext = small_font.render("Click to exit", True, (200, 200, 200))
    subtext_rect = subtext.get_rect(center=((WIDTH + 125) // 2,
                                            HEIGHT // 2 + 50))
    screen.blit(subtext, subtext_rect)


def play_turn() -> list[str]:
    """
    Plays turn when action such as space
    bar pressed or piece is moved
    """
    messages = []

    board = Board(pieces, ROWS, COLS)

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

dragging_piece = None
original_row = None
original_col = None
valid_drag_moves = []

current_turn = "White"

while running:
    screen.fill(BLACK)

    if game_over:
        draw_victory_screen()

    else:
        draw_board()
        draw_pieces()
        draw_log()
        draw_captured()

    pygame.display.flip()

    for piece in pieces:
        # Promotion effect timer
        if (hasattr(piece, "promotion_timer")
                and piece.promotion_timer is not None):
            if isinstance(piece.promotion_timer, int):
                piece.promotion_timer -= 1
            if piece.promotion_timer <= 0:
                piece.promoted = False
                del piece.promotion_timer

        # Frozen effect timer
        if hasattr(piece, "frozen_timer") and piece.frozen_timer is not None:
            piece.frozen_timer -= 1
            if piece.frozen_timer <= 0:
                piece.frozen = False
                del piece.frozen_timer

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            running = False

        # Event for press space bar
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            event_log.extend(play_turn())

        # Handle mouse clicks + drags
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if mouse_y is not None:
                row = mouse_y // SQUARE_SIZE
            else:
                row = 0
            col = mouse_x // SQUARE_SIZE

            for piece in reversed(pieces):
                if (
                    piece._row == row
                    and piece._col == col
                    and not piece.is_frozen()
                    and piece.get_color() == current_turn
                ):
                    dragging_piece = piece
                    offset_x = mouse_x - col * SQUARE_SIZE
                    offset_y = mouse_y - row * SQUARE_SIZE
                    original_row = piece._row
                    original_col = piece._col

                    board = Board(pieces, ROWS, COLS)
                    valid_drag_moves = dragging_piece.get_valid_moves(board)
                    break

        # Handle event when mouse click is released
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_piece:
                mouse_x, mouse_y = event.pos
                new_row = max(0, min(ROWS - 1, mouse_y // SQUARE_SIZE))
                new_col = max(0, min(COLS - 1, mouse_x // SQUARE_SIZE))

                # Board to determine valid moves
                board = Board(pieces, ROWS, COLS)
                valid_moves = dragging_piece.get_valid_moves(board)

                dp = dragging_piece
                if (new_row, new_col) in valid_moves:
                    # Check if capture is needed
                    tp = board.get_piece(new_row, new_col)

                    if (
                        tp is not None
                        and tp.get_color() != dp.get_color()
                    ):
                        event_log.extend([f"{dragging_piece.get_color()}"
                                          f"{dragging_piece.get_name()}"
                                          f" captured {tp.get_color()}"
                                          f"{tp.get_name()}"
                                          f"at ({new_row}, {new_col})"])

                        if tp.get_color() == "White":
                            captured_white.append(tp)
                            if tp.get_name() == "King":
                                event_log.extend("Checkmate! Black wins.")
                                game_over = True
                                winner = "Black"

                        else:
                            captured_black.append(tp)
                            if tp.get_name() == "King":
                                event_log.extend("Checkmate! White wins.")
                                game_over = True
                                winner = "White"

                        pieces.remove(tp)

                    dragging_piece._row = new_row
                    dragging_piece._col = new_col

                    # Play next turn
                    ct = current_turn
                    event_log.extend(play_turn())
                    current_turn = "Black" if ct == "White" else "White"

                else:
                    # Invalid move, snap piece back
                    if original_row is not None and original_col is not None:
                        dragging_piece._row = original_row
                        dragging_piece._col = original_col

                dragging_piece = None
                valid_drag_moves = []

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            event_log.extend(play_turn())

    clock.tick(30)

pygame.quit()

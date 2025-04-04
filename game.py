# Re-imports and setup after kernel reset
import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
BOARD_HEIGHT = WIDTH
FONT = pygame.font.SysFont('Arial', 20)

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

# Data model
class ChessPiece:
    def __init__(self, name, color, row, col):
        self.name = name
        self.color = color
        self.row = row
        self.col = col
        self.frozen_turns = 0

    def is_frozen(self):
        return self.frozen_turns > 0

    def freeze(self, turns=1):
        self.frozen_turns += turns

    def reduce_freeze(self):
        if self.frozen_turns > 0:
            self.frozen_turns -= 1

class FreezePieceEvent:
    def apply(self, piece):
        piece.freeze()
        return f"{piece.name} is frozen!"

class PromoteToQueenEvent:
    def apply(self, piece):
        piece.name = "Queen"
        return f"A piece is promoted to Queen!"

# Setup board and pieces
pieces = [ChessPiece("Pawn", "White", 1, 0), ChessPiece("Bishop", "Black", 6, 7)]
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
        center = (piece.col * SQUARE_SIZE + SQUARE_SIZE // 2, piece.row * SQUARE_SIZE + SQUARE_SIZE // 2)
        color = BLUE if piece.color == "White" else RED
        pygame.draw.circle(screen, color, center, 20)
        if piece.is_frozen():
            pygame.draw.circle(screen, BLACK, center, 10)

def draw_log():
    y = BOARD_HEIGHT + 10
    for i, msg in enumerate(event_log[-3:]):
        text_surface = FONT.render(msg, True, WHITE)
        screen.blit(text_surface, (10, y + i * 20))

def play_turn():
    messages = []
    for piece in pieces:
        if piece.is_frozen():
            piece.reduce_freeze()
            messages.append(f"{piece.name} is frozen.")
        else:
            if random.random() < 0.5:
                event = random.choice(events)
                result = event.apply(piece)
                messages.append(result)
            else:
                messages.append(f"{piece.name} moves normally.")
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

    clock.tick(30)

pygame.quit()

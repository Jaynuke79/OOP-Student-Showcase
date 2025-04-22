from board_piece import BoardPiece

class Board:
    """
    A class to manage BoardPieces and create a fully
    cohesive board for Chess Party
    """
    def __init__(self, pieces: list):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.board_state = [[None for _ in range(COLS)] for _ in range(ROWS)]

        # Initialize board with empty instances of BoardPiece
        for row in range(ROWS):
            for col in range (COLS):
                label = f"{chr(65 + col)}{ROWS - row}"
                color = "white" if (row + col) %2 == 0 else "black"
                self.board_state[row][col] = BoardPiece(label, color, surprise=None,
                                                        piece_in_place=False)
        self.update(pieces)

    def update(self, pieces):
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                self.board_state[row][col].set_piece_in_place(False)
            
        for piece in pieces:
            row, col = piece._row, piece._col
            self.grid[row][col] = piece
            self.board_state[row][col].set_piece_in_place(True)

    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.grid[row][col]
        return None

    def is_empty(self, row, col):
        return self.get_piece(row, col) is None

    def get_tile(self, row, col) -> BoardPiece:
        return self.board_state[row][col]
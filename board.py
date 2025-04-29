from board_piece import BoardPiece

class Board:
    """
    A class to manage BoardPieces and create a fully
    cohesive board for Chess Party
    """
    
    def __init__(self, pieces: list, rows: int = 8, cols: int = 8):
        """
        Initalize Chess board
            - Rows
            - Columns
            - Grid
            - Board state
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.board_state = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Initialize board with empty instances of BoardPiece
        for row in range(rows):
            for col in range (cols):
                label = f"{chr(65 + col)}{rows - row}"
                color = "white" if (row + col) %2 == 0 else "black"
                self.board_state[row][col] = BoardPiece(label, color, surprise=None,
                                                        piece_in_place=False)
        self.update(pieces)

    def update(self, pieces):
        """
        """
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                self.board_state[row][col].set_piece_in_place(False)
            
        for piece in pieces:
            row, col = piece._row, piece._col
            self.grid[row][col] = piece
            self.board_state[row][col].set_piece_in_place(True)

    def get_piece(self, row, col):
        """
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def is_empty(self, row, col):
        """
        """
        return self.get_piece(row, col) is None

    def get_tile(self, row, col) -> BoardPiece:
        """
        """
        return self.board_state[row][col]
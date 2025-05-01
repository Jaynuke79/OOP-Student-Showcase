# explosion.py
from board import Board
from chess_piece import ChessPiece


class Explosion:
    """
    Explosions effect a 3x3 area centered at the given tile.
    """

    def __init__(self, board: Board) -> None:
        """
        initialize the explosion manager with the board reference.

        Args:
            board (Board): The current game board instance.
        """
        self.board = board

    def trigger(self, row: int, col: int,
                pieces: list[ChessPiece]) -> list[ChessPiece]:
        """
        trigger an explosion centered at row, col. Any piece in the 3x3
        area around this tile is removed from the board

        Args:
            row (int): center row of explosion
            col (int): center column of explosion
            pieces (list): the list of current pieces on the board

        Returns:
            list: Updated list of pieces after the explosion.
        """
        effected_positions = [
            (r, c)
            for r in range(row - 1, row + 2)
            for c in range(col - 1, col + 2)
            if 0 <= r < self.board.rows and 0 <= c < self.board.cols
        ]

        # Filter out any pieces that are at the effected positions
        new_pieces = []
        for piece in pieces:
            if (piece._row, piece._col) not in effected_positions:
                new_pieces.append(piece)
            else:
                # Remove piece from grid and board_state
                self.board.grid[piece._row][piece._col] = None
                bbs = self.board.board_state
                bbs[piece._row][piece._col].set_piece_in_place(False)

        return new_pieces

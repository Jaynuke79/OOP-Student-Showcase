from __future__ import annotations
from board_piece import BoardPiece

from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from chess_piece import ChessPiece


class Board:
    """
    A class to manage BoardPieces and create a fully
    cohesive board for Chess Party
    """

    def __init__(self, pieces: list[ChessPiece],
                 rows: int = 8, cols: int = 8) -> None:
        """
        Initalize Chess board
            - Rows
            - Columns
            - Grid
            - Board state
        """
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Optional[ChessPiece]]] = [
            [None for _ in range(self.cols)]
            for _ in range(self.rows)]
        self.board_state: list[list[BoardPiece]] = [
            [
                BoardPiece(
                    f"{chr(65 + col)}{rows - row}",
                    "white" if (row + col) % 2 == 0 else "black",
                    surprise=None,
                    piece_in_place=False
                )
                for col in range(self.cols)
            ]
            for row in range(self.rows)
        ]
        self.update(pieces)

    def update(self, pieces: list[ChessPiece]) -> None:
        """
        """
        self.grid = [[None for _ in range(self.cols)]
                     for _ in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                self.board_state[row][col].set_piece_in_place(False)

        for piece in pieces:
            row, col = piece._row, piece._col
            self.grid[row][col] = piece
            self.board_state[row][col].set_piece_in_place(True)

    def get_piece(self, row: int, col: int) -> Optional[ChessPiece]:
        """
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def is_empty(self, row: int, col: int) -> bool:
        """
        """
        return self.get_piece(row, col) is None

    def get_tile(self, row: int, col: int) -> BoardPiece | None:
        """
        """
        return self.board_state[row][col]

from typing import Optional
from event_classes.base_random_event import RandomEvent
from chess_piece import ChessPiece, Queen


class PromoteToQueenEvent(RandomEvent):
    """
    Promotes a random unit to a Queen if there
    are not already four Queens on the board.
    """

    def __init__(self) -> None:
        """
        Initialize QueenEvent random event
        """
        self._queen_limit = 4

    def apply(self, piece: ChessPiece,
              pieces: Optional[list[ChessPiece]] = None) -> str:
        """
        Apply promotion if not already 4 Queens on board
        """
        if pieces is None:
            return "Promotion failed -- no list provided for pieces"

        if Queen.get_unit_count() != self._queen_limit:
            new_queen = Queen("Queen", piece.get_color(),
                              piece._row, piece._col,
                              1, 8, "any")

            new_queen.promoted = True
            new_queen.promotion_timer = 100

            # Replace promoted unit with new Queen unit
            index = pieces.index(piece)
            pieces[index] = new_queen

            promoted_str: str = "has been promoted to Queen!"
            return f"{piece.get_color()} {piece.get_name()} {promoted_str}"
        else:
            return "Promotion failed -- too many Queens"

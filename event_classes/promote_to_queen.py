from event_classes.base_random_event import RandomEvent
from chess_piece import ChessPiece

class PromoteToQueenEvent(RandomEvent):

    def __init__(self, unit_count: int):
        self._queen_limit = 4

    def apply(self, piece: ChessPiece):
        if unit_count != self._queen_limit:
            piece.set_name("Queen")
            return f"{piece.get_color()} piece has been promoted to Queen!"

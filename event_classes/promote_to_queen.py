from event_classes.base_random_event import RandomEvent
from chess_piece import ChessPiece

class PromoteToQueenEvent(RandomEvent):
    def apply(self, piece: ChessPiece):
        piece.set_name("Queen")
        return f"{piece.get_color()} piece has been promoted to Queen!"

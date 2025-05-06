from typing import Optional
from event_classes.base_random_event import RandomEvent
from chess_piece import ChessPiece


class FreezePieceEvent(RandomEvent):
    def __init__(self, turns: int = 1):
        self.turns = turns

    def apply(self, piece: ChessPiece,
              pieces: Optional[list[ChessPiece]] = None) -> str:
        piece.freeze(self.turns)
        piece.frozen = True
        piece.frozen_timer = 100
        return f"{piece.get_name()} is frozen for {self.turns} turn(s)!"

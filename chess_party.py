from typing import List
from chess_piece import ChessPiece
from board_piece import BoardPiece
from event_classes.freeze_piece import FreezePieceEvent
from event_classes.promote_to_queen import PromoteToQueenEvent
import random

# Chess Party Core
class ChessParty:
    def __init__(self, pieces: List[ChessPiece], board: List[BoardPiece]):
        self.pieces = pieces
        self.board = board
        self.turn = 0
        self.events = [FreezePieceEvent, PromoteToQueenEvent]

    def play_turn(self):
        log = []
        self.turn += 1
        log.append(f"Turn {self.turn} begins!")

        for piece in self.pieces:
            if piece.is_frozen():
                piece.reduce_frozen()
                log.append(f"{piece.get_name()} is frozen and cannot move this turn.")
                continue

            # 50% chance to get an event
            if random.random() < 0.5:
                event_cls = random.choice(self.events)
                event = event_cls()
                result = event.apply(piece)
                log.append(result)
            else:
                log.append(f"{piece.get_name()} takes a normal move.")

        return log

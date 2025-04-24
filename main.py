import random
from typing import List, Optional
from dataclasses import dataclass

# Import provided classes (mocked here for code execution; replace with actual file import if running externally)
from chess_piece import ChessPiece
from board_piece import BoardPiece

from event_classes.freeze_piece import FreezePieceEvent 
from event_classes.promote_to_queen import PromoteToQueenEvent

from chess_party import ChessParty

# # Sample usage
# pieces = [
#     ChessPiece("Pawn", 8, 1, "forward", "White"),
#     ChessPiece("Bishop", 2, 8, "diagonal", "Black"),
# ]

# board = [BoardPiece(f"{chr(65+i)}1", "White", None, False) for i in range(8)]

# game = ChessParty(pieces, board)
# turn_logs = [game.play_turn() for _ in range(3)]  # Play 3 turns

# print(turn_logs)

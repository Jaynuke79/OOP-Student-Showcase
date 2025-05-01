from abc import ABC, abstractmethod
from chess_piece import ChessPiece
from typing import List, Optional


class RandomEvent(ABC):
    @abstractmethod
    def apply(self, piece: ChessPiece,
              pieces: Optional[List[ChessPiece]] = None) -> str:
        pass

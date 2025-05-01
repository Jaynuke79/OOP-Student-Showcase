import unittest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st
from typing import Optional, List
from event_classes.base_random_event import RandomEvent
from event_classes.explosion import Explosion
from event_classes.freeze_piece import FreezePieceEvent
from event_classes.promote_to_queen import PromoteToQueenEvent
from board import Board
from chess_piece import ChessPiece, Pawn, Queen


class DummyPiece(ChessPiece):
    unit_count = 0

    def __init__(self, name: str = "Pawn", color: str = "white",
                 row: int = 0, col: int = 0) -> None:
        unit_count_limit = 8
        movement_count = 1
        movement_style = "normal"
        super().__init__(name, color, row, col,
                         unit_count_limit, movement_count,
                         movement_style)
        self.frozen = False
        self.freeze_calls = 0
        self.frozen_timer = 0

    def freeze(self, turns: int) -> None:
        self.frozen = True
        self.freeze_calls += 1
        self.frozen_timer = 100


class DummyBoard:
    def __init__(self, rows: int = 8, cols: int = 8) -> None:
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.board_state: list[list[MagicMock]] = [
            [MagicMock(set_piece_in_place=MagicMock())
             for _ in range(cols)] for _ in range(rows)]


class TestRandomEvent(unittest.TestCase):
    def test_random_event_not_implemented(self) -> None:
        class IncompleteEvent(RandomEvent):
            def apply(self, piece: ChessPiece,
                      pieces: Optional[List[ChessPiece]] = None) -> str:
                raise NotImplementedError()

        with self.assertRaises(NotImplementedError):
            IncompleteEvent().apply(MagicMock())


class TestExplosion(unittest.TestCase):
    def setUp(self) -> None:
        self.board = Board(pieces=[])
        self.explosion = Explosion(self.board)

    def test_explosion_removes_pieces_in_3x3(self) -> None:
        pieces: list[ChessPiece] = []
        for r in range(3):
            for c in range(3):
                p = DummyPiece(row=r, col=c)
                pieces.append(p)
                self.board.grid[r][c] = p

        updated_pieces = self.explosion.trigger(1, 1, pieces)

        self.assertEqual(len(updated_pieces), 0)
        bs = self.board.board_state
        for r in range(3):
            for c in range(3):
                self.assertIsNone(self.board.grid[r][c])
                self.assertFalse(bs[r][c].is_piece_in_place())

    def test_explosion_preserves_outside_pieces(self) -> None:
        piece1 = DummyPiece(row=0, col=0)
        piece2 = DummyPiece(row=4, col=4)
        self.board.grid[0][0] = piece1
        self.board.grid[4][4] = piece2

        pieces: list[ChessPiece] = [piece1, piece2]
        result = self.explosion.trigger(0, 0, pieces)
        self.assertEqual(result, [piece2])


class TestFreezePieceEvent(unittest.TestCase):
    def test_freeze_applies_properly(self) -> None:
        piece = DummyPiece()
        event = FreezePieceEvent(turns=2)
        msg = event.apply(piece)
        self.assertTrue(piece.frozen)
        self.assertEqual(piece.freeze_calls, 1)
        self.assertEqual(piece.frozen_timer, 100)
        self.assertIn("frozen for 2 turn(s)", msg)

    @given(st.integers(min_value=1, max_value=10))
    def test_freeze_with_random_turns(self, turns: int) -> None:
        piece = DummyPiece()
        event = FreezePieceEvent(turns=turns)
        msg = event.apply(piece)

        self.assertTrue(piece.frozen)
        self.assertEqual(piece.freeze_calls, 1)
        self.assertEqual(piece.frozen_timer, 100)
        self.assertIn(f"frozen for {turns} turn(s)", msg)


class TestPromoteToQueenEvent(unittest.TestCase):
    def setUp(self) -> None:
        Queen.unit_count = 0

    def test_promotes_piece_when_under_limit(self) -> None:
        piece = DummyPiece("Pawn", "white", 3, 3)
        pieces: list[ChessPiece] = [piece]
        event = PromoteToQueenEvent()
        msg = event.apply(piece, pieces)

        self.assertIsInstance(pieces[0], Queen)
        self.assertTrue(pieces[0].promoted)
        self.assertEqual(pieces[0].promotion_timer, 100)
        self.assertIn("has been promoted to Queen", msg)

    def test_does_not_promote_if_limit_reached(self) -> None:

        board = Board(pieces=[])
        pawn = Pawn("Pawn", "White", 6, 0, 8, 1, "forward")
        board.update([pawn])

        pieces: list[ChessPiece] = [pawn]
        event = PromoteToQueenEvent()
        event.apply(pawn, pieces)

        self.assertIsInstance(board.get_piece(6, 0), Pawn)


if __name__ == "__main__":
    unittest.main()

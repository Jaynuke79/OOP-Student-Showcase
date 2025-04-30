import unittest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st

from event_classes.base_random_event import RandomEvent
from event_classes.explosion import Explosion
from event_classes.freeze_event import FreezePieceEvent
from event_classes.promote_event import PromoteToQueenEvent
from chess_piece import ChessPiece, Queen
from board import Board


class DummyPiece(ChessPiece):
    def __init__(self, name="Pawn", color="white", row=0, col=0):
        super().__init__(name, color, row, col, health=1, power=1, move_type="any")
        self.frozen = False
        self.freeze_calls = 0

    def freeze(self, turns):
        self.frozen = True
        self.freeze_calls += 1
        self.frozen_timer = 0


class DummyBoard:
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.board_state = [[MagicMock() for _ in range(cols)] for _ in range(rows)]


class TestRandomEvent(unittest.TestCase):
    def test_random_event_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            RandomEvent().apply(MagicMock())


class TestExplosion(unittest.TestCase):
    def setUp(self):
        self.board = DummyBoard()
        self.explosion = Explosion(self.board)

    def test_explosion_removes_pieces_in_3x3(self):
        pieces = []
        for r in range(3):
            for c in range(3):
                p = DummyPiece(row=r, col=c)
                pieces.append(p)
                self.board.grid[r][c] = p

        updated_pieces = self.explosion.trigger(1, 1, pieces)

        self.assertEqual(len(updated_pieces), 0)
        for r in range(3):
            for c in range(3):
                self.assertIsNone(self.board.grid[r][c])
                self.board.board_state[r][c].set_piece_in_place.assert_called_with(False)

    def test_explosion_preserves_outside_pieces(self):
        piece1 = DummyPiece(row=0, col=0)
        piece2 = DummyPiece(row=4, col=4)
        self.board.grid[0][0] = piece1
        self.board.grid[4][4] = piece2

        pieces = [piece1, piece2]
        result = self.explosion.trigger(0, 0, pieces)
        self.assertEqual(result, [piece2])


class TestFreezePieceEvent(unittest.TestCase):
    def test_freeze_applies_properly(self):
        piece = DummyPiece()
        event = FreezePieceEvent(turns=2)
        msg = event.apply(piece)
        self.assertTrue(piece.frozen)
        self.assertEqual(piece.freeze_calls, 1)
        self.assertEqual(piece.frozen_timer, 100)
        self.assertIn("frozen for 2 turn(s)", msg)

    @given(st.integers(min_value=1, max_value=10))
    def test_freeze_with_random_turns(self, turns):
        """Property-based test to ensure freeze always applies."""
        piece = DummyPiece()
        event = FreezePieceEvent(turns=turns)
        msg = event.apply(piece)

        self.assertTrue(piece.frozen)
        self.assertEqual(piece.freeze_calls, 1)
        self.assertEqual(piece.frozen_timer, 100)
        self.assertIn(f"frozen for {turns} turn(s)", msg)


class TestPromoteToQueenEvent(unittest.TestCase):
    def setUp(self):
        Queen._unit_count = 0  # Reset static count before each test

    def test_promotes_piece_when_under_limit(self):
        piece = DummyPiece("Pawn", "white", 3, 3)
        pieces = [piece]
        event = PromoteToQueenEvent()
        msg = event.apply(piece, pieces)

        self.assertIsInstance(pieces[0], Queen)
        self.assertTrue(pieces[0].promoted)
        self.assertEqual(pieces[0].promotion_timer, 100)
        self.assertIn("has been promoted to Queen", msg)

    def test_does_not_promote_if_limit_reached(self):
        Queen._unit_count = 4
        piece = DummyPiece("Pawn", "white", 3, 3)
        pieces = [piece]
        event = PromoteToQueenEvent()
        msg = event.apply(piece, pieces)

        self.assertEqual(pieces[0], piece)
        self.assertIn("Promotion failed", msg)


if __name__ == "__main__":
    unittest.main()

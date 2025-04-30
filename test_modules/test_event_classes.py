import unittest
from unittest.mock import MagicMock
from hypothesis import given, strategies as st

from event_classes.base_random_event import RandomEvent
from event_classes.explosion import Explosion
from event_classes.freeze_piece import FreezePieceEvent
from event_classes.promote_to_queen import PromoteToQueenEvent
from board import Board
from chess_piece import ChessPiece
from board import Board
from chess_piece import Pawn, Queen


class DummyPiece(ChessPiece):
    unit_count = 0

    def __init__(self, name="Pawn", color="white", row=0, col=0):
        unit_count_limit = 8
        movement_count = 1
        movement_style = "normal"
        super().__init__(name, color, row, col, unit_count_limit, movement_count, movement_style)
        self.frozen = False
        self.freeze_calls = 0
        self.frozen_timer = 0

    def freeze(self, turns):
        self.frozen = True
        self.freeze_calls += 1
        self.frozen_timer = 100


class DummyBoard:
    def __init__(self, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.board_state = [[MagicMock() for _ in range(cols)] for _ in range(rows)]


class TestRandomEvent(unittest.TestCase):
    def test_random_event_not_implemented(self):
        # test if random event raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            RandomEvent().apply(MagicMock())


class TestExplosion(unittest.TestCase):
    def setUp(self):
        # set up board and explosion event
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

        self.assertEqual(len(updated_pieces), 0)  # ensure all pieces are removed
        for r in range(3):
            for c in range(3):
                self.assertIsNone(self.board.grid[r][c])  # check grid is empty
                self.board.board_state[r][c].set_piece_in_place.assert_called_with(False)

    def test_explosion_preserves_outside_pieces(self):
        # test explosion does not affect pieces outside the blast zone
        piece1 = DummyPiece(row=0, col=0)
        piece2 = DummyPiece(row=4, col=4)
        self.board.grid[0][0] = piece1
        self.board.grid[4][4] = piece2

        pieces = [piece1, piece2]
        result = self.explosion.trigger(0, 0, pieces)
        self.assertEqual(result, [piece2])  # ensure piece2 is preserved


class TestFreezePieceEvent(unittest.TestCase):
    def test_freeze_applies_properly(self):
        # test freeze applies correctly to piece
        piece = DummyPiece()
        event = FreezePieceEvent(turns=2)
        msg = event.apply(piece)
        self.assertTrue(piece.frozen)  # piece should be frozen
        self.assertEqual(piece.freeze_calls, 1)  # freeze called once
        self.assertEqual(piece.frozen_timer, 100)  # frozen timer should be 100
        self.assertIn("frozen for 2 turn(s)", msg)  # check the message

    @given(st.integers(min_value=1, max_value=10))
    def test_freeze_with_random_turns(self, turns):
        # test freeze with random number of turns
        piece = DummyPiece()
        event = FreezePieceEvent(turns=turns)
        msg = event.apply(piece)

        self.assertTrue(piece.frozen)  # piece should be frozen
        self.assertEqual(piece.freeze_calls, 1)  # freeze called once
        self.assertEqual(piece.frozen_timer, 100)  # frozen timer should be 100
        self.assertIn(f"frozen for {turns} turn(s)", msg)  # check the message


class TestPromoteToQueenEvent(unittest.TestCase):
    def setUp(self):
        # reset queen count before each test
        Queen._unit_count = 0

    def test_promotes_piece_when_under_limit(self):
        # test promote piece to queen when unit count is under limit
        piece = DummyPiece("Pawn", "white", 3, 3)
        pieces = [piece]
        event = PromoteToQueenEvent()
        msg = event.apply(piece, pieces)

        self.assertIsInstance(pieces[0], Queen)  # piece should be promoted to Queen
        self.assertTrue(pieces[0].promoted)  # check if promoted flag is True
        self.assertEqual(pieces[0].promotion_timer, 100)  # promotion timer should be 100
        self.assertIn("has been promoted to Queen", msg)  # check the message

    def test_does_not_promote_if_limit_reached(self):
        # dynamically add attribute for test
        if not hasattr(Queen, 'unit_count_limit'):
            Queen.unit_count_limit = 2

        Queen.unit_count = Queen.unit_count_limit  # simulate the limit being reached

        # create board and pawn for the test
        board = Board(pieces=[])
        pawn = Pawn("Pawn", "White", 6, 0, 8, 1, "forward")
        board.update([pawn])

        # dynamically set pieces
        pieces = [pawn]

        # create the PromoteToQueenEvent with only one argument
        event = PromoteToQueenEvent()

        # apply the event to the pawn, not the board
        event.apply(pawn, pieces)

        # the pawn should not be promoted
        self.assertIsInstance(board.get_piece(6, 0), Pawn)


if __name__ == "__main__":
    unittest.main()

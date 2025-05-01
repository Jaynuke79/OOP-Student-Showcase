"""
Unittest for Board class found in board.py

"""

import unittest
from hypothesis import given
from hypothesis.strategies import integers
from board import Board
from chess_piece import ChessPiece


class MockPiece(ChessPiece):
    """
    Mock class for ChessPiece class
    for testing purposes
    """
    def get_move_directions(self): return [(1, 0)]
    def get_max_steps(self): return 1


class TestBoard(unittest.TestCase):
    """
    TestBoard class to test Board class functions
    """

    def setUp(self) -> None:
        """
        Generate Board object
        """

        self.piece1 = MockPiece("Test", "White", 1, 1, 1, 1, "line")
        self.piece2 = MockPiece("Test", "White", 2, 1, 1, 1, "line")
        self.piece3 = MockPiece("Test", "Black", 3, 4, 1, 1, "line")
        self.board = Board(pieces=[self.piece1, self.piece2, self.piece3])

    def test_piece_placement1(self) -> None:
        """
        Test piece placement function (1)
        """
        result = self.board.get_piece(1, 1)
        self.assertEqual(result, self.piece1)

    def test_piece_placement2(self) -> None:
        """
        Test piece placement function (2)
        """
        result = self.board.get_piece(2, 1)
        self.assertEqual(result, self.piece2)

    def test_piece_placement3(self) -> None:
        """
        Test piece placement function (3)
        """
        result = self.board.get_piece(3, 4)
        self.assertEqual(result, self.piece3)

    def test_is_empty_false1(self) -> None:
        """
        Test is empty false function (1)
        """
        self.assertFalse(self.board.is_empty(1, 1))

    def test_is_empty_false2(self) -> None:
        """
        Test is empty false function (2)
        """
        self.assertFalse(self.board.is_empty(2, 1))

    def test_is_empty_false3(self) -> None:
        """
        Test is empty false function (3)
        """
        self.assertFalse(self.board.is_empty(3, 4))

    def test_is_empty_true1(self) -> None:
        """
        Test is empty true function (1)
        """
        self.assertTrue(self.board.is_empty(0, 0))

    def test_is_empty_true2(self) -> None:
        """
        Test is empty true function (2)
        """
        self.assertTrue(self.board.is_empty(5, 0))

    def test_is_empty_true3(self) -> None:
        """
        Test is empty true function (3)
        """
        self.assertTrue(self.board.is_empty(6, 4))

    @given(integers(min_value=0, max_value=7),
           integers(min_value=0, max_value=7))
    def test_valid_get_piece_bounds(self, row: int, col: int) -> None:
        """
        Test valid get piece bounds using hypothesis generated data
        """
        piece = self.board.get_piece(row, col)
        if row == 1 and col == 1:
            self.assertEqual(piece, self.piece1)
        elif row == 2 and col == 1:
            self.assertEqual(piece, self.piece2)
        elif row == 3 and col == 4:
            self.assertEqual(piece, self.piece3)
        else:
            self.assertIsNone(piece)

    @given(integers(), integers())
    def test_out_of_bounds_get_piece(self, row: int, col: int) -> None:
        """
        Test out of bounds get piece function using hypothesis generated data
        """
        if not (0 <= row < 8 and 0 <= col < 8):
            self.assertIsNone(self.board.get_piece(row, col))

    @given(integers(min_value=0, max_value=7),
           integers(min_value=0, max_value=7))
    def test_is_empty_matches_get_piece(self, row: int, col: int) -> None:
        """
        Test is empty = get piece using hypothesis generated data
        """
        is_empty = self.board.is_empty(row, col)
        piece = self.board.get_piece(row, col)
        self.assertEqual(is_empty, piece is None)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover

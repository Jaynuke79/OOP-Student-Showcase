"""
Unittest for ChessPiece class found in chess_piece.py
Did not test move directions - Unsure how to do so/difficult to test
But, lots of playtesting demonstrates that only movement
that adheres to the Chess rules are allowed, as intended
"""

import unittest
from hypothesis import given
from hypothesis.strategies import integers
from hypothesis import strategies as st
from chess_piece import ChessPiece, Pawn, Rook, Knight
from chess_piece import Bishop, King, Queen


class TestChessPiece(unittest.TestCase):
    """
    TestChessPiece class to test ChessPiece + children class functions
    """

    def setUp(self) -> None:
        """
        Generate ChessPiece and other Chess objects
        """

        self.pawn = Pawn("Test", "White", 1, 1, 1, 1, "line")
        self.rook = Rook("Test", "White", 2, 1, 1, 1, "line")
        self.knight = Knight("Test", "Black", 3, 4, 1, 1, "line")
        self.bishop = Bishop("Test", "Black", 3, 4, 1, 1, "line")
        self.king = King("Test", "Black", 3, 4, 1, 1, "line")
        self.queen = Queen("Test", "Black", 3, 4, 1, 1, "line")

    def test_get_max_steps(self) -> None:
        """
        Test get max steps functions for each child class
        derived from ChessPiece
        """
        self.assertEqual(self.pawn.get_max_steps(), 2)
        self.assertEqual(self.rook.get_max_steps(), 8)
        self.assertEqual(self.knight.get_max_steps(), 4)
        self.assertEqual(self.bishop.get_max_steps(), 8)
        self.assertEqual(self.king.get_max_steps(), 1)
        self.assertEqual(self.queen.get_max_steps(), 8)
    
    @given(freeze_turns=st.integers(min_value=1, max_value=10))
    def test_piece_frozen(self, freeze_turns: int) -> None:
        """
        Test when a piece is frozen
        Applies to all Chess Pieces
        """
        for piece in [self.pawn, self.rook, self.knight,
                      self.bishop, self.queen, self.king]:
                piece.freeze(freeze_turns)
                self.assertTrue(piece.is_frozen())

                for _ in range(freeze_turns - 1):
                    piece.reduce_frozen()
                    self.assertTrue(piece.is_frozen())

                piece.reduce_frozen()
                self.assertFalse(piece.is_frozen())

        
    def test_unit_count(self) -> None:
        """
        Test class unit_count 
        """
        # Start with 3 because of previous tests
        self.assertEqual(3, self.pawn.get_unit_count())
        self.pawn2 = Pawn("Test", "White", 2, 4, 1, 1, "line")
        self.assertEqual(4, self.pawn.get_unit_count())
        
        self.assertEqual(3, self.rook.get_unit_count())
        self.rook2 = Rook("Test", "White", 2, 1, 1, 1, "line")
        self.assertEqual(4, self.rook.get_unit_count())

        self.assertEqual(3, self.knight.get_unit_count())
        self.knight2 = Knight("Test", "Black", 3, 4, 1, 1, "line")
        self.assertEqual(4, self.knight.get_unit_count())

        self.assertEqual(3, self.bishop.get_unit_count())
        self.bishop2 = Bishop("Test", "Black", 3, 4, 1, 1, "line")
        self.assertEqual(4, self.bishop.get_unit_count())

        self.assertEqual(3, self.king.get_unit_count())
        self.king2 = King("Test", "Black", 3, 4, 1, 1, "line")
        self.assertEqual(4, self.king.get_unit_count())

        self.assertEqual(3, self.queen.get_unit_count())
        self.queen2 = Queen("Test", "Black", 3, 4, 1, 1, "line")
        self.assertEqual(4, self.queen.get_unit_count())

if __name__ == "__main__":
    unittest.main()  # pragma: no cover

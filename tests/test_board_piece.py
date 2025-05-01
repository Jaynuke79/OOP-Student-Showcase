"""
Unittest for BoardPiece class found in board_piece.py

"""

import unittest
from board_piece import BoardPiece


class TestBoardPiece(unittest.TestCase):
    """
    TestBoardPiece class to test BoardPiece class functions
    """

    def setUp(self) -> None:
        """
        Generate BoardPiece object
        """

        self.obj = BoardPiece(":", ":", ":", ":")

    """
    Below test functions are just for getters and setters
    as there are no regular functions in this class
    """
    def test_get_label(self) -> None:
        """ Simple test function for get label"""
        lbl: str = "this_is_a_label"
        self.obj.set_label(lbl)
        self.assertEqual(self.obj.get_label(), "this_is_a_label")

    def test_get_color(self) -> None:
        """ Simple test function for get color"""
        clr: str = "orange"
        self.obj.set_color(clr)
        self.assertEqual(self.obj.get_color(), "orange")

    def test_get_surprise(self) -> None:
        """ Simple test function for get surprise"""
        srp: str = "boom!"
        self.obj.set_surprise(srp)
        self.assertEqual(self.obj.get_surprise(), "boom!")

    def test_is_piece_in_place(self) -> None:
        """ Simple test function for get piece in place"""
        pip: str = "yes"
        self.obj.set_piece_in_place(pip)
        self.assertEqual(self.obj.is_piece_in_place(), "yes")


if __name__ == "__main__":
    unittest.main()  # pragma: no cover

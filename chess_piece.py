from abc import ABC, abstractmethod

# ChessPiece class
class ChessPiece:
    """
    Base/parent class for Chess Pieces
    Each unique piece will inherit from this class
    """

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        self._name = name
        self._color = color
        self._row = row
        self._col = col
        self._unit_count_limit = unit_count_limit
        self._movement_count = movement_count
        self._movement_style = movement_style
        self._frozen_turns = 0  # For event tracking
        self.__class__.unit_count += 1

    def get_name(self) -> str: return self._name
    def set_name(self, name: str): self._name = name

    def get_color(self) -> str: return self._color
    def set_color(self, color: str): self._color = color

    # Placeholder method for valid movements
    @abstractmethod
    def get_valid_moves(self, board) -> list:
        """ 
        Return list of (row, col) tuples that represent
        the legal movements of each piece
        """
        pass


    def freeze(self, turns: int):
        self._frozen_turns += turns

    def is_frozen(self) -> bool:
        return self._frozen_turns > 0

    def reduce_frozen(self):
        if self._frozen_turns > 0:
            self._frozen_turns -= 1
    
    @classmethod
    def get_unit_count(cls):
        return cls.unit_count

class Pawn(ChessPiece):
    """
    Class for Pawn pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)

    def get_valid_moves(self, board):
        direction: int = 1 if self._color == "White" else -1
        moves = []

        one_step = (self._row + direction, self._col)
        if 0 <= one_step[0] < 8:
            moves.append(one_step)

        start_row = 1 if self._color == "White" else 6
        if self._row == start_row:
            two_step = (self._row + 2 * direction, self._col)
            if 0 <= two_step[0] < 8:
                moves.append(two_step)
        return moves

class Queen(ChessPiece):
    """
    Class for Queen pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)
    
    #def get_valid_moves(self, board):

class King(ChessPiece):
    """
    Class for King pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)

    #def get_valid_moves(self, board):

class Bishop(ChessPiece):
    """
    Class for Bishop pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)
        
    #def get_valid_moves(self, board):

class Knight(ChessPiece):
    """
    Class for Knight pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)
        
    #def get_valid_moves(self, board):

class Rook(ChessPiece):
    """
    Class for Rook pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)
    
    #def get_valid_moves(self, board):
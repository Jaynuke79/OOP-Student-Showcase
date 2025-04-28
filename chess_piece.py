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

    @abstractmethod
    def get_move_directions(self) -> list[tuple[int, int]]:
        """
        Abstract method; allow each piece class to define
        allowed move directions (row_offset, col_offset)
        """
        pass

    @abstractmethod
    def get_max_steps(self) -> int:
        """
        Defines the movement count limit of each piece
        - King: 1
        - Queen: 8
        - Rook: 8
        - Pawn: 1 (2 if at start)
        etc.
        """
        pass

    def get_valid_moves(self, board) -> list:
        """ 
        Return list of (row, col) tuples that represent
        the legal movements of each piece
        """
        moves = []
        directions = self.get_move_directions()
        max_steps = self.get_max_steps()

        for dr, dc in directions:
            for step in range(1, max_steps + 1):
                new_row = self._row + dr * step
                new_col = self._col + dc * step
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))
                else:
                    if target.get_color() != self._color:
                        moves.append((new_row, new_col)) # Capture
                    break # Can't jump over pieces
        
        return moves

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
    
    # def get_move_directions(self):
    #     """

    #     """
    #     return [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    def get_max_steps(self):
        """
        Pawn max movement: 1 (except when at beginning)
        """
        return 1


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
    def get_max_steps(self):
        """
        Queen max movement: 8 (across board)
        """

class King(ChessPiece):
    """
    Class for King pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)

    def get_move_directions(self):
        """
        Up, down, left, right, diagonal
        """
        return [
            (1, 0), (-1, 0), (0, 1), (0, -1)
            (1, 1), (-1, 1), (1, -1), (-1, -1)
            ]
    
    def get_max_steps(self):
        return 1

class Bishop(ChessPiece):
    """
    Class for Bishop pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)

    def get_move_directions(self):
        """
        Diagonal in any direction
        Bottom right, bottom left
        Top right, top left
        """
        return [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
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
    def get_move_directions(self):
        """
        Knight moves in an L shape
        (2, 1) = Move down twice, then move right once (down 2, right 1)
        """
        return [(2, 1), (1, 2), (-1, 2), (-2,1)
                (-2, -1), (2, -1), (-1, -2), (1, -2)]


class Rook(ChessPiece):
    """
    Class for Rook pieces
    """
    unit_count = 0

    def __init__(self, name: str, color: str, row: int, col: int, 
                 unit_count_limit: int, movement_count: int, movement_style: str):
        super().__init__(name, color, row, col, unit_count_limit, 
                         movement_count, movement_style)

    def get_move_directions(self):
        """
        Up, down, left, right
        """
        return [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    #def get_valid_moves(self, board):
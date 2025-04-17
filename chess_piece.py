# ChessPiece class
class ChessPiece:
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

    def get_name(self) -> str: return self._name
    def set_name(self, name: str): self._name = name

    def get_color(self) -> str: return self._color
    def set_color(self, color: str): self._color = color

    def freeze(self, turns: int):
        self._frozen_turns += turns

    def is_frozen(self) -> bool:
        return self._frozen_turns > 0

    def reduce_frozen(self):
        if self._frozen_turns > 0:
            self._frozen_turns -= 1
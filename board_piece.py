# BoardPiece class
class BoardPiece:
    def __init__(self, label: str, color: str,
                 surprise: object, piece_in_place: bool):
        self._label = label
        self._color = color
        self._surprise = surprise
        self._piece_in_place = piece_in_place

    # Getters
    def get_label(self) -> str:
        return self._label

    def get_color(self) -> str:
        return self._color

    def get_surprise(self) -> object:
        return self._surprise

    def is_piece_in_place(self) -> bool:
        return self._piece_in_place

    # Setters
    def set_label(self, label: str):
        self._label = label

    def set_color(self, color: str):
        self._color = color

    def set_surprise(self, surprise: object):
        self._surprise = surprise

    def set_piece_in_place(self, in_place: bool):
        self._piece_in_place = in_place

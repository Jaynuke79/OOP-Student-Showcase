from chess_piece import ChessPiece


class RandomEvent:
    def apply(self, piece: ChessPiece):
        raise NotImplementedError()

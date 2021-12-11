from pieces.pieces import Rook


def get_piece(notation: str):
    if notation.startswith("R"):
        return Rook()

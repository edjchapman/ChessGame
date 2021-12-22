class Piece:
    """
    Chess piece.
    """
    pos_x: int
    pos_y: int

    def __init__(self, pos_x: int, pos_y: int, side: bool):
        """sets initial values"""
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.side = side

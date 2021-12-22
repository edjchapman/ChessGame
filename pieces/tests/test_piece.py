from pieces.piece import Piece


def test_initialising_piece_with_values():
    p = Piece(pos_x=1, pos_y=2, side=True)
    assert p.pos_x == 1
    assert p.pos_y == 2
    assert p.side is True

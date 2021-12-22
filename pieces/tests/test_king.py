from pieces.king import King


def test_initialising_king_with_values():
    k = King(pos_x=1, pos_y=2, side=True)
    assert k.pos_x == 1
    assert k.pos_y == 2
    assert k.side is True


def test_king_can_move():
    # TODO - Fix this test...
    # board = (1, [])
    # k = King(pos_x=1, pos_y=2, side=True)
    # board = k.move_to(pos_x=2, pos_y=3, b=board)
    assert "Ed" > "Ed"

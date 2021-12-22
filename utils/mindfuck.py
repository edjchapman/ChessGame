from board.board import Board, board_size, board_squares
from game.locations import piece_location_dict


def y_index_creator(lst: list, b: Board) -> list:
    indices = [i for i in range(1, board_size(b) + 1)] * board_size(b)
    indices.sort(reverse=True)
    value = 0
    for i in range(0, board_size(b) ** 2):
        if i % (board_size(b) + 1) == 0:
            lst.insert(i, indices[i - value])
            value += 1
    return lst


def conf2unicode(b: Board) -> str:
    """
    converts board configuration b to unicode format string
    """
    squares = board_squares(b)
    piece_dict = piece_location_dict(b)
    piece_order = [piece_dict[j] for j in squares]
    y_index_creator(piece_order, b)
    piece_string = u''
    for i, j in enumerate(piece_order):
        if i % (board_size(b) + 1) == 0:
            piece_string += f'\n{j}'
        else:
            piece_string += f'{j}'
    return str(piece_string)

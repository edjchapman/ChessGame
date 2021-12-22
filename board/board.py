from game.locations import index2location, get_letter
from pieces.piece import Piece

Board = tuple[int, list[Piece]]


def board_size(b: Board):
    return b[0]


def board_pieces(b: Board):
    return b[1]


def save_board(filename: str, b: Board) -> None:
    """
    saves board configuration into file in current directory in plain format
    """
    f_out = open(filename, 'w')
    first_line = board_size(b)
    white_pieces = [get_letter(p) + index2location(p.pos_x, p.pos_y) for p in board_pieces(b) if p.side is True]
    black_pieces = [get_letter(p) + index2location(p.pos_x, p.pos_y) for p in board_pieces(b) if p.side is False]
    second_line = ', '.join(white_pieces)
    third_line = ', '.join(black_pieces)
    f_out.write(f'{first_line}\n{second_line}\n{third_line}\n')
    print('The game configuration saved.')
    f_out.close()


def board_squares(b: Board) -> list[tuple[int, int]]:
    size = board_size(b)
    x_ranges = range(1, size + 1)
    y_ranges = range(size, 0, -1)
    squares = [(x, y) for y in y_ranges for x in x_ranges]
    return squares

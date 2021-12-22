import string

from pieces.bishop import Bishop
from pieces.king import King
from pieces.piece import Piece
from pieces.rook import Rook

Board = tuple[int, list[Piece]]


def location2index(loc: str) -> tuple[int, int]:
    """
    converts chess location to corresponding x and y coordinates - COMPLETED
    Be2
    """
    # create dictionary of alphabet
    column_names = list(string.ascii_lowercase)
    row_names = list(range(1, 27))
    alpha_dict = dict(zip(column_names, row_names))

    # obtain row and column as integers
    row = int(loc[2:])
    column = alpha_dict[loc[1]]

    return column, row


def index2location(x: int, y: int) -> str:
    """
    converts  pair of coordinates to corresponding location - COMPLETED
    """
    # create dictionary of alphabet
    column_names = list(string.ascii_lowercase)
    row_names = list(range(1, 27))
    alpha_dict = dict(zip(row_names, column_names))

    column = alpha_dict[x]

    return column + str(y)


def is_piece_at(pos_x: int, pos_y: int, b: Board) -> bool:
    """
    checks if a piece is at coordinates pos_x, pos_y of board B
    """
    coords = []
    from board.board import board_pieces
    for p in board_pieces(b):
        if p.pos_x == pos_x and p.pos_y == pos_y:
            coords.append((pos_x, pos_y))
    if len(coords) > 0:
        return True
    else:
        return False


def piece_at(pos_x: int, pos_y: int, b: Board) -> Piece:
    """
    returns the piece at coordinates pos_x, pos_y of board B
    assumes some piece at coordinates pos_x, pos_y of board B is present
    """
    if is_piece_at(pos_x, pos_y, b):
        from board.board import board_pieces
        for p in board_pieces(b):
            if p.pos_x == pos_x:
                if p.pos_y == pos_y:
                    return p


def get_king(side: bool, b: Board) -> King:
    from board.board import board_pieces
    king = [piece for piece in board_pieces(b) if type(piece) == King if piece.side == side]
    return King(king[0].pos_x, king[0].pos_y, king[0].side)


def get_piece(pos_x, pos_y, piece, side):
    if piece == 'B':
        return Bishop(pos_x, pos_y, side)
    if piece == 'R':
        return Rook(pos_x, pos_y, side)
    if piece == 'K':
        return King(pos_x, pos_y, side)


def get_letter(piece: Piece) -> str:
    if type(piece) == Rook:
        return 'R'
    if type(piece) == Bishop:
        return 'B'
    if type(piece) == King:
        return 'K'


def piece_location_dict(b: Board) -> dict[tuple[int, int], str]:
    # create dictionary of pieces
    black_dict = {King: '\u2654', Rook: '\u2656', Bishop: '\u2657'}
    white_dict = {King: '\u265A', Rook: '\u265C', Bishop: '\u265D'}
    from board.board import board_squares
    squares = board_squares(b)
    piece_dict: dict[tuple[int, int], str] = {}
    from board.board import board_pieces
    for piece in board_pieces(b):
        if piece.side is True:
            p = white_dict[type(piece)]
            piece_dict[(piece.pos_x, piece.pos_y)] = p
        if piece.side is False:
            p = black_dict[type(piece)]
            piece_dict[(piece.pos_x, piece.pos_y)] = p
    for s in squares:
        if s not in piece_dict:
            piece_dict[s] = '\u2001'
    return piece_dict

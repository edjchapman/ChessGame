import random
import re

from board.board import Board, board_pieces, board_squares
from game.locations import location2index, get_king
from game.status import is_check
from pieces.bishop import Bishop
from pieces.king import King
from pieces.piece import Piece
from pieces.rook import Rook


def move_piece(location_destination: str) -> list[tuple[int, int]]:
    """
    Move piece to a given destination.
    """
    # crCR with no piece definition, 4-6 letters e.g a1b1 or a20b1 or a1b20 or a20b20
    try:
        chess_regex = re.compile(r'[a-z][0-9]+')
        matches = chess_regex.findall(location_destination)
        matches = ['P' + p for p in matches]
        piece_location = location2index(matches[0])
        piece_destination = location2index(matches[1])
        return [piece_location, piece_destination]
    except IndexError as i:
        print(f'Length of string too short. Must be at least 4 characters long! Further details: {i}')
    except TypeError as t:
        print(f'String not in correct format or too short. Must be in the format [a-z][0-9]+. Further details: {t}')


def find_black_move(b: Board) -> tuple[Piece, int, int]:
    """
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere
    """
    squares = board_squares(b)
    random.shuffle(squares)

    bk = get_king(False, b)
    # possible_move = [(x, y) for x, y in squares if bk.can_move_to(x,y,b)]
    if is_check(False, b):
        for x, y in squares:
            if bk.can_move_to(x, y, b):
                return bk, x, y

    black_pieces = [piece for piece in board_pieces(b) if piece.side is False]

    if len(black_pieces) == 1:
        for x, y in squares:
            if bk.can_move_to(x, y, b):
                return bk, x, y
        else:
            print('Stalemate! Game over.')
            quit()

    black_piece = random.choice(black_pieces)

    if type(black_piece) == King:
        for x, y in squares:
            if black_piece.can_move_to(x, y, b):
                return black_piece, x, y
        else:
            black_piece = random.choice(black_pieces)  # does this work? Or should I call the function again e.g.
            # find_black_move(b)

    if type(black_piece) == Rook:
        for x, y in squares:
            if black_piece.can_move_to(x, y, b):
                return black_piece, x, y
            else:
                black_piece = random.choice(black_pieces)
    if type(black_piece) == Bishop:
        for x, y in squares:
            if black_piece.can_move_to(x, y, b):
                return black_piece, x, y
            else:
                black_piece = random.choice(black_pieces)

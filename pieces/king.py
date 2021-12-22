from copy import deepcopy

from game.status import is_check
from pieces.piece import Piece

Board = tuple[int, list[Piece]]


class King(Piece):
    def __init__(self, pos_x: int, pos_y: int, side: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_x, pos_y, side)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.side = side

    def king_move(self, pos_x, pos_y) -> bool:
        result_x = (pos_x - self.pos_x) ** 2
        result_y = (pos_y - self.pos_y) ** 2
        if result_x == 0:
            if result_y == 0:
                return False
        if result_x == 0 or result_x == 1:
            if result_y == 0 or result_y == 1:
                return True
            else:
                return False
        else:
            return False

    def king_range(self, b) -> list[tuple[int, int]]:
        king_coords: list[tuple[int, int]]
        # eight possible positions a king can move to
        from board.board import board_size
        size = board_size(b)
        if self.pos_x == size:
            p3 = (self.pos_x, self.pos_y + 1)
            p4 = (self.pos_x, self.pos_y - 1)
            p5 = (self.pos_x - 1, self.pos_y - 1)
            p6 = (self.pos_x - 1, self.pos_y)
            p7 = (self.pos_x - 1, self.pos_y + 1)
            king_coords = [p3, p4, p5, p6, p7]

        if self.pos_y == size:
            p1 = (self.pos_x + 1, self.pos_y)
            p4 = (self.pos_x, self.pos_y - 1)
            p5 = (self.pos_x - 1, self.pos_y - 1)
            p6 = (self.pos_x - 1, self.pos_y)
            p8 = (self.pos_x + 1, self.pos_y - 1)
            king_coords = [p1, p4, p5, p6, p8]

        else:
            p1 = (self.pos_x + 1, self.pos_y)
            p2 = (self.pos_x + 1, self.pos_y + 1)
            p3 = (self.pos_x, self.pos_y + 1)
            p4 = (self.pos_x, self.pos_y - 1)
            p5 = (self.pos_x - 1, self.pos_y - 1)
            p6 = (self.pos_x - 1, self.pos_y)
            p7 = (self.pos_x - 1, self.pos_y + 1)
            p8 = (self.pos_x + 1, self.pos_y - 1)

            king_coords = [p1, p2, p3, p4, p5, p6, p7, p8]

        return king_coords

    def can_reach(self, pos_x: int, pos_y: int, b: Board) -> bool:
        """
        checks if this king can move to coordinates pos_x, pos_y on board b according to rule [Rule3] and [Rule4]
        """
        from board.board import board_size
        from game.locations import is_piece_at, piece_at

        if pos_x > board_size(b) or pos_y > board_size(b):
            raise ValueError('values are greater than the specified board size')

        if pos_x < 1 or pos_y < 1:
            raise ValueError('chess coordinates must be greater than 0!')

        # king can move to eight positions, all within one x or y coord
        if self.king_move(pos_x, pos_y):
            # check is_piece_at final position
            if is_piece_at(pos_x, pos_y, b):
                # if there's a piece, check its side and make sure it is not the same colour
                p = piece_at(pos_x, pos_y, b)
                if p.side == self.side:
                    return False
                else:
                    return True
            return True
        else:
            return False

    def can_move_to(self, pos_x: int, pos_y: int, b: Board) -> bool:
        """
        checks if this king can move to coordinates pos_x, pos_y on board b according to all chess rules
        """
        from board.board import board_pieces
        from game.locations import is_piece_at, piece_at, get_king

        if not self.can_reach(pos_x, pos_y, b):
            return False
        else:
            test_board = deepcopy(b)

            king = get_king(self.side, test_board)
            if is_piece_at(pos_x, pos_y, test_board):
                piece_out = piece_at(pos_x, pos_y, test_board)
                board_pieces(test_board).remove(piece_out)
            for piece in board_pieces(test_board):
                if piece.pos_x == king.pos_x:
                    if piece.pos_y == king.pos_y:
                        piece.pos_x = pos_x
                        piece.pos_y = pos_y
            if is_check(self.side, test_board):
                return False
            else:
                return True

    def move_to(self, pos_x: int, pos_y: int, b: Board) -> Board:
        """
        returns new board resulting from move of this king to coordinates pos_x, pos_y on board b
        assumes this move is valid according to chess rules
        """
        # check can_move_to for legality of move
        # if True, update King(Piece) with new coordinates
        # if piece of other side has the same coordinates, remove/delete that piece from memory
        # check can_move_to for legality of move
        from board.board import board_pieces
        from game.locations import is_piece_at, piece_at, get_king

        if self.can_move_to(pos_x, pos_y, b):
            king = get_king(self.side, b)
            if is_piece_at(pos_x, pos_y, b):
                piece_out = piece_at(pos_x, pos_y, b)
                board_pieces(b).remove(piece_out)
            for piece in board_pieces(b):
                if piece.pos_x == king.pos_x and piece.pos_y == king.pos_y:
                    piece.pos_x = pos_x
                    piece.pos_y = pos_y
        else:
            raise ValueError('cannot move to that square - check self.can_move_to')

        return b

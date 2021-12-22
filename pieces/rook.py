from copy import deepcopy

from pieces.piece import Piece

Board = tuple[int, list[Piece]]


class Rook(Piece):
    def __init__(self, pos_x: int, pos_y: int, side: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_x, pos_y, side)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.side = side

    def rook_move(self, pos_x: int, pos_y: int) -> bool:
        """returns True if the Rook move is physically possible"""
        if self.pos_x == pos_x or self.pos_y == pos_y:
            return True
        else:
            return False

    def rook_range(self, pos_x: int, pos_y: int) -> list[tuple[int, int]]:
        if self.pos_x == pos_x:
            y_ranges = [i for i in range(self.pos_y + 1, pos_y + 1) if self.pos_y < pos_y] or \
                       [i for i in range(self.pos_y - 1, pos_y - 1, -1) if self.pos_y > pos_y]
            x_ranges = [pos_x] * len(y_ranges)
            return list(zip(x_ranges, y_ranges))

        if self.pos_y == pos_y:
            x_ranges = [i for i in range(self.pos_x + 1, pos_x + 1) if self.pos_x < pos_x] or \
                       [i for i in range(self.pos_x - 1, pos_x - 1, -1) if self.pos_x > pos_x]
            y_ranges = [pos_y] * len(x_ranges)
            return list(zip(x_ranges, y_ranges))

    def can_reach(self, pos_x: int, pos_y: int, b: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_x, pos_y on board b
        [Rule2] A rook can move any number of squares along a row
        or column, but cannot leap over other pieces.
        [Rule4] A piece of side X (Black or White) cannot move to a location occupied by a piece of side X.
        Hint: use is_piece_at
        """
        from board.board import board_size
        from game.locations import is_piece_at, piece_at

        # slice self.pos_y and pos_y to get a range of x values between desired spot and
        if pos_x > board_size(b) or pos_y > board_size(b):
            raise ValueError('values are greater than the specified board size')

        if pos_x < 1 or pos_y < 1:
            raise ValueError('chess coordinates must be greater than 0!')

        if self.rook_move(pos_x, pos_y):
            ranges = self.rook_range(pos_x, pos_y)
            if len(ranges) == 1:
                if is_piece_at(pos_x, pos_y, b):
                    # if there's a piece, check its side and make sure it is not the same colour
                    p = piece_at(pos_x, pos_y, b)
                    if p.side == self.side:
                        return False
                    else:
                        return True
            if len(ranges) > 1:
                for x, y in ranges[0:(len(ranges) - 1)]:
                    if is_piece_at(x, y, b):
                        return False
            # check is_piece_at final position
            if is_piece_at(pos_x, pos_y, b):
                # if there's a piece, check its side and make sure it is not the same colour
                p = piece_at(pos_x, pos_y, b)
                if p.side == self.side:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False

    def can_move_to(self, pos_x: int, pos_y: int, b: Board) -> bool:
        """
        checks if this rook can move to coordinates pos_x, pos_y on board b according to all chess rules
        [Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
        """
        from board.board import board_pieces
        from game.status import is_check

        test_board = deepcopy(b)
        if is_check(self.side, b):
            # rewrite logic for if piece can move when is_check = True. Can move piece if is_check = False after move
            for piece in board_pieces(test_board):
                if piece.pos_x == self.pos_x:
                    if piece.pos_y == self.pos_y:
                        piece.pos_x = pos_x
                        piece.pos_y = pos_y
            if is_check(self.side, test_board):
                return False

        if not self.can_reach(pos_x, pos_y, b):
            return False
        # [Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
        # need to update coordinates temporarily then check if is_check is True for the same side
        # if after self.pos_x = pos_x and self.pos_y = pos_y is check is true, return False

        for piece in board_pieces(test_board):
            if piece.pos_x == self.pos_x:
                if piece.pos_y == self.pos_y:
                    piece.pos_x = pos_x
                    piece.pos_y = pos_y
        if is_check(self.side, test_board):
            return False
        else:
            return True

    def move_to(self, pos_x: int, pos_y: int, b: Board) -> Board:
        """
        returns new board resulting from move of this rook to coordinates pos_x, pos_y on board b
        assumes this move is valid according to chess rules
        """
        from board.board import board_pieces
        from game.locations import piece_at
        from game.locations import is_piece_at

        # check can_move_to for legality of move
        if self.can_move_to(pos_x, pos_y, b):
            if is_piece_at(pos_x, pos_y, b):
                piece_out = piece_at(pos_x, pos_y, b)
                # if True, update Rook(Piece) with new coordinates
                self.pos_x = pos_x
                self.pos_y = pos_y
                # if piece of other side has the same coordinates, remove/delete that piece from memory
                board_pieces(b).remove(piece_out)
            else:
                self.pos_x = pos_x
                self.pos_y = pos_y
        else:
            raise ValueError('cannot move to that square - check self.can_move_to')

        return b

from copy import deepcopy

from game.status import is_check
from pieces.piece import Piece

Board = tuple[int, list[Piece]]


class Bishop(Piece):
    def __init__(self, pos_x: int, pos_y: int, side: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_x, pos_y, side)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.side = side

        # subtracting cell coordinates for two possible bishop moves results in a pair of numbers that are equal when squared

    def bishop_move(self, pos_x: int, pos_y: int) -> bool:
        """
        returns True if the bishop move is physically possible
        """
        # x,y coords will change in every scenario, otherwise move isn't legal
        rows = self.pos_x - pos_x
        columns = self.pos_y - pos_y
        # if columns or rows == 0:
        #     return False
        if columns ** 2 == rows ** 2:
            if columns != 0:
                return True
            else:
                return False
        else:
            return False

    def bishop_range(self, pos_x: int, pos_y: int) -> list[tuple[int, int]]:
        # four possibilities - either x, y both increase, x, y both decrease,
        # x increases and y decreases, or x decreases and y increases
        x_ranges = [i for i in range(self.pos_x + 1, pos_x + 1) if pos_x > self.pos_x] or \
                   [i for i in range(self.pos_x - 1, pos_x - 1, -1) if pos_x < self.pos_x]
        y_ranges = [j for j in range(self.pos_y + 1, pos_y + 1) if pos_y > self.pos_y] or \
                   [j for j in range(self.pos_y - 1, pos_y - 1, -1) if pos_y < self.pos_y]

        return list(zip(x_ranges, y_ranges))

    def can_reach(self, pos_x: int, pos_y: int, b: Board) -> bool:
        """checks if this bishop can move to coordinates pos_x, pos_y on board b according to rule [Rule1] and [Rule4]"""
        # check along the range of legal moves in between pos_x, pos_y and pos_x, pos_y along board b
        # if there is a piece in the way - using is_piece_at function, return false
        # check if move is legal
        from board.board import board_size
        from game.locations import is_piece_at

        if pos_x > board_size(b) or pos_y > board_size(b):
            raise ValueError('values are greater than the specified board size')

        if pos_x < 1 or pos_y < 1:
            raise ValueError('chess coordinates must be greater than 0!')

        if self.bishop_move(pos_x, pos_y):
            # check if pieces are in the way
            ranges = self.bishop_range(pos_x, pos_y)
            for x, y in ranges[0:(len(ranges) - 1)]:
                if is_piece_at(x, y, b):
                    return False
            # is_piece_at final position
            if is_piece_at(pos_x, pos_y, b):
                # if there's a piece, check its side and make sure it is not the same colour
                from game.locations import piece_at
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
        """checks if this bishop can move to coordinates pos_x, pos_y on board b according to all chess rules"""
        # [Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
        # work out logic for preventing self check by moving bishop
        # cannot move this piece if the King is in check
        from board.board import board_pieces
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
        returns new board resulting from move of this bishop to coordinates pos_x, pos_y on board b
        assumes this move is valid according to chess rules
        """
        from game.locations import is_piece_at
        from game.locations import piece_at
        from board.board import board_pieces
        # check can_move_to for legality of move
        if self.can_move_to(pos_x, pos_y, b):
            if is_piece_at(pos_x, pos_y, b):
                piece_out = piece_at(pos_x, pos_y, b)
                # if True, update Bishop(Piece) with new coordinates
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

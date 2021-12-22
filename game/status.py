from pieces.piece import Piece
from pieces.rook import Rook

Board = tuple[int, list[Piece]]


def is_check(side: bool, b: Board) -> bool:
    """
    checks if configuration of b is check for side
    Hint: use can_reach
    returns True if it is check
    """
    from board.board import board_pieces
    from game.locations import get_king
    from pieces.bishop import Bishop

    king = get_king(side, b)
    enemy_side = not side
    enemy_pieces = [ep for ep in board_pieces(b) if ep.side == enemy_side]
    enemy_bishops = [Bishop(eb.pos_x, eb.pos_y, eb.side) for eb in enemy_pieces if type(eb) == Bishop]
    enemy_rooks = [Rook(er.pos_x, er.pos_y, er.side) for er in enemy_pieces if type(er) == Rook]
    enemy_king = get_king(enemy_side, b)

    for bishop in enemy_bishops:
        if bishop.can_reach(king.pos_x, king.pos_y, b):
            return True

    for rook in enemy_rooks:
        if rook.can_reach(king.pos_x, king.pos_y, b):
            return True

    if enemy_king.can_reach(king.pos_x, king.pos_y, b):
        return True
    else:
        return False


def is_checkmate(side: bool, b: Board) -> bool:
    """
    checks if configuration of b is checkmate for side
    """
    from board.board import board_squares
    from game.locations import get_king
    king = get_king(side, b)
    if is_check(side, b):
        for x, y in board_squares(b):
            if king.can_move_to(x, y, b):
                return False
        else:
            return True
    else:
        return False


def read_board(filename: str) -> Board:
    """
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    Ba1, Ra2, Be2, Ra5, Kc5
    """
    # read chess_puzzle
    from game.locations import location2index
    from game.locations import get_piece

    loop_statement = True
    while loop_statement:
        if filename == 'QUIT':
            quit()
        try:
            with open(filename) as chess:
                lines = chess.readlines()
                size = int(lines[0].strip('\n'))
                white_pieces = (lines[1].strip('\n')).split(', ')
                black_pieces = (lines[2].strip('\n')).split(', ')
                pieces = []
                for wp in white_pieces:
                    x, y = location2index(wp)
                    z = wp[0]
                    pieces.append(get_piece(pos_x=x, pos_y=y, piece=z, side=True))

                for bp in black_pieces:
                    x, y = location2index(bp)
                    z = bp[0]
                    pieces.append(get_piece(pos_x=x, pos_y=y, piece=z, side=False))

                b = (size, pieces)
                loop_statement = False
                return b
        except Exception as e:
            print(e)
            filename = input('This is not a valid file. File name for initial configuration: ')

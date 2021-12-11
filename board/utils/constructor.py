from pieces.utils.get_piece import get_piece


def construct_board(board, notation_list):
    for notation in notation_list:
        board.pieces.append(
            get_piece(notation=notation)
        )

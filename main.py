from board.board import Board
from board.utils.constructor import construct_board
from locations.locations import is_piece_at

notation_list = [
    "Be4"
]

if __name__ == '__main__':
    b = Board()
    construct_board(board=b, notation_list=notation_list)
    is_piece_at("B", 1, 2)

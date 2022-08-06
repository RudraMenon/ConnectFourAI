import numpy as np
from Board import Board
from connect_4 import *
import time

empty_board = np.zeros((7, 7))

winning_board_1_hor = empty_board.copy()
winning_board_1_hor[5, 1:5] = 2

winning_board_1_vert = empty_board.copy()
winning_board_1_vert[:4, 0] = 2

winning_board_incline_diag = empty_board.copy()
winning_board_incline_diag[0, 4] = 2
winning_board_incline_diag[1, 3] = 2
winning_board_incline_diag[2, 2] = 2
winning_board_incline_diag[3, 1] = 2

winning_board_decline_diag = empty_board.copy()
winning_board_decline_diag[5, 4] = 2
winning_board_decline_diag[4, 3] = 2
winning_board_decline_diag[3, 2] = 2
winning_board_decline_diag[2, 1] = 2

not_win_board = empty_board.copy()
not_win_board[5, 4] = 2
not_win_board[4, 3] = 2
not_win_board[3, 2] = 2
not_win_board[3, 1] = 2

b = Board()
for win_board in [winning_board_1_vert, winning_board_1_hor, winning_board_decline_diag, winning_board_decline_diag,
                  not_win_board]:
    b.board = win_board
    b.prtBoard()
    print(evaulate_board(b))
    st = time.time()
    print(f"Winning: {b.check_win(2)}")
    print(time.time() - st)
    print()

import cv2
import numpy as np
from Board import Board


def evaulate_board(board, pos=None):
    connected_lengths = [3, 4]
    multipliers = [1000, 1000000]
    evaluation = 0

    alpha_player = 1
    beta_player = 2
    for i, connected_len in enumerate(connected_lengths):
        beta_occurence, alpha_occurence = 0, 0
        padding = [0] if connected_len < 4 else []

        arr_to_find = padding + [beta_player] * connected_len
        beta_occurence += board.get_connected_occurences(arr_to_find, pos=pos)
        arr_to_find = [beta_player] * connected_len + padding
        beta_occurence += board.get_connected_occurences(arr_to_find, pos=pos)

        arr_to_find = padding + [alpha_player] * connected_len
        alpha_occurence += board.get_connected_occurences(arr_to_find, pos=pos)
        arr_to_find = [alpha_player] * connected_len + padding
        alpha_occurence += board.get_connected_occurences(arr_to_find, pos=pos)

        evaluation += (alpha_occurence * multipliers[i]) - (beta_occurence * multipliers[i])
    return evaluation



def minimax(board, pos, depth, is_max_player, alpha, beta):
    board_value = evaulate_board(board, pos=pos)
    if abs(board_value) > 100000 or depth > DEPTH:  # Is a winning board:
        return None, board_value,

    player = 1 if is_max_player else 2
    if is_max_player:
        best_val = -np.inf
        best_col = 0
        for col_num in range(7):
            dropped, pos = board.drop_player_token(player, col_num)
            if not dropped:
                continue
            _, next_val = minimax(board, pos, depth + 1, False, alpha, beta)
            board.remove_top_token(col_num)
            if next_val > best_val:
                best_col = col_num
                best_val = next_val
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
        return best_col, best_val
    else:
        best_val = np.inf
        best_col = 0
        for col_num in range(7):
            dropped, pos = board.drop_player_token(player, col_num)
            if not dropped:
                continue
            _, next_val = minimax(board, pos, depth + 1, True, alpha, beta)
            board.remove_top_token(col_num)
            if next_val < best_val:
                best_col = col_num
                best_val = next_val
            beta = min(beta, best_val)
            if beta <= alpha:
                break
        return best_col, best_val


DEPTH = 5
if __name__ == "__main__":
    board = Board()
    player_num = 1
    while True:

        is_over, winner = board.check_any_winner()
        if is_over:
            print(f"Game Over!, winner: {winner}!!!!")
        board.show_board()
        key = cv2.waitKey(0)

        chosen_slot = int(chr(key)) - 1
        board.drop_player_token(player_num, chosen_slot)
        board.show_board()
        board.prt_board()
        print("\n\n")
        cv2.waitKey(10)

        ## speed profiling
        # import cProfile
        # import pstats
        # from pstats import SortKey
        # cProfile.run("minimax(board, None,0,  False, -np.inf, np.inf)", "minimax")
        # p = pstats.Stats('minimax')
        # p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
        col, val = minimax(board, None, 0, False, -np.inf, np.inf)
        print(col, val)
        board.drop_player_token(2, col)

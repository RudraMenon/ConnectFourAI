import numpy as np
from Board import Board


def evaulate_board(board):
    connected_lengths = [1, 2, 3, 4]
    multipliers = [10, 100, 1000, 100000]
    len_occurences = [0, 0, 0, 0]

    alpha_player = 1
    beta_player = 2
    for i, connected_len in enumerate(connected_lengths):
        beta_occurence, alpha_occurence = 0, 0

        arr_to_find = [0] + [beta_player] * connected_len
        print(arr_to_find)
        beta_occurence += board.get_connected_occurences(arr_to_find)
        arr_to_find = [beta_player] * connected_len + [0]
        beta_occurence += board.get_connected_occurences(arr_to_find)

        arr_to_find = [0] + [alpha_player] * connected_len
        alpha_occurence += board.get_connected_occurences(arr_to_find)
        arr_to_find = [alpha_player] * connected_len + [0]
        alpha_occurence += board.get_connected_occurences(arr_to_find)

        len_occurences[i] = (alpha_occurence * multipliers[i]) - (beta_occurence * multipliers[i])
    return np.sum(len_occurences)

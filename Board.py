import copy
import time

import numpy as np
from scipy.ndimage import rotate
from scipy.signal import convolve2d
import numba as nb

BOARD_SIZE = 7


@nb.jit(parallel=False)
def count_arr_occurence(a1, a2):
    occ = 0
    for i in nb.prange(len(a1) - len(a2) + 1):
        for j in range(len(a2)):
            if a1[i + j] != a2[j]:
                break
        else:
            occ += 1
    return occ


class Board():
    def __init__(self):
        self.size = BOARD_SIZE
        self.board = np.zeros((self.size, self.size))

    def drop_player_token(self, player, col_num):
        """ Place a player's token in the bottom of a column. Returns if drop was successful.
        (Fails if column is full)"""
        col = self.board[:, col_num]
        if np.min(col) > 0:
            return False
        row = self.size if (np.max(col) == 0) else (col != 0).argmax(axis=0)
        self.board[col_num][row] = player
        return True

    def check_win(self, player):
        return self.get_connected_occurences([player] * 4) > 0

    def get_connected_occurences(self, arr_to_find):
        """ check if a player has 4 in a row"""
        mat_to_find = np.asarray(arr_to_find)
        diag_mat = np.diagflat(arr_to_find)
        occurences = 0
        occurences += np.sum(np.apply_along_axis(lambda x: count_arr_occurence(x, mat_to_find), 0, self.board))
        occurences += np.sum(np.apply_along_axis(lambda x: count_arr_occurence(x, mat_to_find), 0, self.board.T))
        for k in range(-3,3):
            diag = np.diag(self.board, k=k)
            diag_t = np.diag(self.board.T, k=k)
            occurences += count_arr_occurence(diag, mat_to_find)
            occurences += count_arr_occurence(diag_t, mat_to_find)
        return occurences

    def prtBoard(self):
        """ Print board as a string"""
        chars = " XO"
        print("|", end="")
        for i in range(7):
            print(f"{i}|", end="")
        print()
        for rowNum in range(self.size):
            row = self.board[rowNum, :].astype(int)
            s = f"|{'|'.join([chars[cell] for cell in row])}|"
            print(s)

    def isFull(self):
        return np.min(self.board) > 0

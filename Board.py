import copy
import time
import cv2
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
            return False, (col, -1)
        row_num = (self.size if (np.max(col) == 0) else (col != 0).argmax(axis=0)) - 1
        self.board[row_num][col_num] = player
        return True, (col_num, row_num)

    def remove_top_token(self, col_num):
        col = self.board[:, col_num]
        row_num = (self.size if (np.max(col) == 0) else (col != 0).argmax(axis=0))
        self.board[row_num][col_num] = 0
        return True

    def check_win(self, player):
        return self.get_connected_occurences([player] * 4) > 0

    def check_any_winner(self):
        for player in [1, 2]:
            if self.check_win(player):
                return True, player
        return False, None

    def get_connected_occurences(self, arr_to_find, pos=None):
        """ check if a player has 4 in a row"""
        if pos is None:
            board = self.board
        else:
            x, y = pos
            x_start = max(0, x - 3)
            x_end = min(self.size, x + 4)
            y_start = max(0, y - 3)
            y_end = min(self.size, y + 4)
            board = self.board[y_start:y_end, x_start:x_end]
            x, y = self.size - y, x

        mat_to_find = np.asarray(arr_to_find)
        occurences = 0
        # This happens to be faster than apply_along_axis
        for x in board:
            occurences += count_arr_occurence(x, mat_to_find)
        for x in board.T:
            occurences += count_arr_occurence(x, mat_to_find)
        rot_board = np.rot90(board, k=1)
        if pos is None:
            for k in range(-3, 4):
                diag = np.diag(board, k=k)
                diag_t = np.diag(rot_board, k=k)
                occurences += count_arr_occurence(diag, mat_to_find)
                occurences += count_arr_occurence(diag_t, mat_to_find)
        else:
            for k in range(-1, 1):
                diag = np.diag(board, k=k)
                diag_t = np.diag(rot_board, k=k)
                occurences += count_arr_occurence(diag, mat_to_find)
                occurences += count_arr_occurence(diag_t, mat_to_find)
        return occurences

    def prt_board(self):
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

    def show_board(self):
        board_img = np.zeros((700, 700, 3)) + 255
        for col in range(self.size):
            board_img = cv2.line(board_img, (0, col * 100), (700, col * 100), color=(0, 0, 0), thickness=5)
            for row in range(self.size):
                board_img = cv2.line(board_img, (row * 100, 0), (row * 100, 700), color=(0, 0, 0), thickness=5)
                val = self.board[row][col]
                if val > 0:
                    color = (0, 0, 255) if val == 1 else (255, 0, 0)
                    board_img = cv2.circle(board_img, (col * 100 + 50, row * 100 + 50), radius=50, color=color,
                                           thickness=-1)
        cv2.imshow("board", board_img)

    def read_from_str(self, board_str):
        self.reset_board()
        for row_num, row in enumerate(board_str.split("\n")):
            row = row.strip()
            for col_num, col in enumerate(row[1:-1].split("|")):
                if col == " ":
                    value = 0
                elif col == "X":
                    value = 1
                elif col == "O":
                    value = 2
                self.board[row_num][col_num] = value

    def reset_board(self):
        self.board = np.zeros((self.size, self.size))

    def is_full(self):
        return np.min(self.board) > 0

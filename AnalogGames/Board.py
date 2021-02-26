# coding:UTF-8

import numpy as np
from Exceptions import *

"""
n * n　のマス目を作成できます
オセロ・将棋・チェス・囲碁などに使用できます
"""


class Board(object):
    def _range_check(self, row, col):
        """
        よく使うrowとcolの値が範囲内であることを確認できます

        :param row:
        :param col:
        :return:
        """
        if row not in range(self.size) or col not in range(self.size):
            raise PieceIndexError("row:{} col:{}", format(row, col))

    def pop(self, destination):
        """
        指定した地点の駒を成ります
        厳密に言えば先手の駒なら駒番号を+10 後手の駒なら-10します

        :param row: 盤面の最上段を0としたインデックス　言い換えればY軸
        :param col: 盤面の最左列を0としたインデックス　言い換えればX軸

        :raise PieceIndexError 指定座標が範囲外であることを意味します
        :raise NoPieceError 指定座標に駒が存在しないことを意味します
        :raise PromotedAlreadyError 指定座標の駒がすでに成っていることを意味します

        :return obj:
            取り出した駒番号　成り駒は絶対値が-10されます
            後手の駒である場合、負の値であることに注意してください
        """
        row, col = destination

        self._range_check(row, col)

        piece_num = self.array[row][col]

        if piece_num == 0:
            raise NoPieceError("row:{} col:{}", format(row, col))

        self.array[row][col] = 0

    def drop(self, destination, obj):
        """駒や石などをを任意の場所に置きます

        :param row:
        :param col:
        :param obj:
        :return:
        """
        row, col = destination

        piece_num = self.array[row][col]

        self._range_check(row, col)

        if piece_num != 0:
            raise PieceExistsError("row:{} col:{}", format(row, col))

        self.array[row][col] = obj

    def move(self, source, destination):
        """駒を任意の場所に移動させます

        :param r_src:移動元のrow
        :param c_src:移動元のcol
        :param r_dst:移動先のrow
        :param c_dst:移動先のcol

        """
        r_src, c_src = source
        r_dst, c_dst = destination
        piece_num_src = self.array[r_src][c_src]
        piece_num_dst = self.array[r_dst][c_dst]

        self._range_check(r_src, c_src)

        if piece_num_src == 0:
            raise PieceNotFoundError("row:{} col:{}", format(r_src, c_src))

        # 移動先に駒がないことの確認
        if r_dst not in range(9) or c_dst not in range(9):
            raise PieceIndexError("row:{} col:{}", format(r_dst, c_dst))
        if piece_num_dst != 0:
            raise PieceExistsError("row:{} col:{}", format(r_dst, c_dst))

        # コマの移動処理
        self.array[r_dst][c_dst] = piece_num_src
        self.array[r_src][c_src] = 0

        return

    def __init__(self, size):
        """
        :param size:盤面のサイズを定義します
        オセロやチェスなら8 将棋なら9　などを指定できます
        """

        self.size = size
        self.array = np.zeros(dtype="int8", shape=(size, size))

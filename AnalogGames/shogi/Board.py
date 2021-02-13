# coding:UTF-8

import numpy as np
from piece_dictionary import en_to_num, num_to_en
from Exceptions import *


class _Field(object):
    """
    81マスの盤面を表現したクラス
    :parameter self._array:list<list<int>>
        9*9の二次元配列には整数が入っています
        駒は整数で表現されています

        docstring上では"駒番号"と呼ばれます

        空白は0

        先手の駒番号
            歩兵:1
            桂馬:2
            香車:3
            銀将:4
            金将:5
            角行:6
            飛車:7
            王将:8

            と:11
            成桂:12
            成香:13
            成銀:14
            龍馬(角成):16
            龍王(飛成):17



        後手の駒番号
            歩兵:-1
            桂馬:-2
            香車:-3
            銀将:-4
            金将:-5
            角行:-6
            飛車:-7
            王将:-8

            と:  -11
            成桂: -12
            成香: -13
            成銀: -14
            龍馬: -16
            龍王: -17



    """

    def promotion(self, row, col):
        """
        指定した地点の駒を成ります
        厳密に言えば先手の駒なら駒番号を+10 後手の駒なら-10します

        :param row: 盤面の最上段を0としたインデックス　言い換えればY軸
        :param col: 盤面の最左列を0としたインデックス　言い換えればX軸

        :raise PieceIndexError 指定座標が範囲外であることを意味します
        :raise NoPieceError 指定座標に駒が存在しないことを意味します
        :raise PromotedAlreadyError 指定座標の駒がすでに成っていることを意味します
        """

        piece_num = self._array[row][col]

        if row not in range(9) or col not in range(9):
            raise PieceIndexError("row:{} col:{}", format(row, col))

        if piece_num == 0:
            raise NoPieceError("row:{} col:{}", format(row, col))

        if abs(piece_num) > 10:
            raise PromotedAlreadyError("row:{} col:{}".format(row, col))

        # 成りの処理
        if piece_num > 0:
            self._array[row][col] += 10
        else:
            self._array[row][col] -= 10

    def pop(self, row, col) -> int:
        """
        指定した地点の駒を成ります
        厳密に言えば先手の駒なら駒番号を+10 後手の駒なら-10します

        :param row: 盤面の最上段を0としたインデックス　言い換えればY軸
        :param col: 盤面の最左列を0としたインデックス　言い換えればX軸

        :raise PieceIndexError 指定座標が範囲外であることを意味します
        :raise NoPieceError 指定座標に駒が存在しないことを意味します
        :raise PromotedAlreadyError 指定座標の駒がすでに成っていることを意味します

        :return piece_num:
            取り出した駒番号　成り駒は絶対値が-10されます
            後手の駒である場合、負の値であることに注意してください
        """

        piece_num = self._array[row][col]

        if row not in range(9) or col not in range(9):
            raise PieceIndexError("row:{} col:{}", format(row, col))

        if piece_num == 0:
            raise NoPieceError("row:{} col:{}", format(row, col))

        self._array[row][col] = 0

        # 成駒を不成の状態に戻す
        if abs(piece_num) > 10:
            if piece_num > 0:
                piece_num -= 10
            else:
                piece_num += 10

        return piece_num

    def drop(self, row, col, drop_piece_num):
        """駒を任意の場所に置きます

        :param row:
        :param col:
        :param drop_piece_num:置く駒番号を指定します
        :return:
        """

        piece_num = self._array[row][col]

        if row not in range(9) or col not in range(9):
            raise PieceIndexError("row:{} col:{}", format(row, col))

        if piece_num != 0:
            raise PieceExistsError("row:{} col:{}", format(row, col))

        self._array[row][col] = drop_piece_num

    def move(self, r_src, c_src, r_dst, c_dst):
        """駒を任意の場所に移動させます

        :param r_src:移動元のrow
        :param c_src:移動元のcol
        :param r_dst:移動先のrow
        :param c_dst:移動先のcol

        """
        piece_num_src = self._array[r_src][c_src]
        piece_num_dst = self._array[r_dst][c_dst]

        # 移動先に駒がないことの確認
        if r_src not in range(9) or c_src not in range(9):
            raise PieceIndexError("row:{} col:{}", format(r_src, c_src))
        if piece_num_src == 0:
            raise PieceNotFoundError("row:{} col:{}", format(r_src, c_src))

        # 移動先に駒がないことの確認
        if r_dst not in range(9) or c_dst not in range(9):
            raise PieceIndexError("row:{} col:{}", format(r_dst, c_dst))
        if piece_num_dst != 0:
            raise PieceExistsError("row:{} col:{}", format(r_dst, c_dst))

        # コマの移動処理
        self._array[r_dst][c_dst] = piece_num_src
        self._array[r_src][c_src] = 0

        return

    def __init__(self, sfen_head: str = ""):
        """
        :param sfen_head: sfen形式の文字列の前半の盤面を意味する部分　分割処理は呼び出し元が担当する
        """
        self._array = np.zeros(dtype="int8", shape=(9, 9))


class _PieceStand(object):
    def get_piece_count(self, piece_num):
        return self.array[piece_num - 1]

    def decrease(self, piece_num, amount=1):
        if self.array[piece_num - 1] < amount:
            raise NoPieceError("piece_num:{}".format(piece_num))

        self.array[piece_num - 1] -= 1

    def increase(self, piece_num, amount=1):
        self.array[piece_num - 1] += amount

    def __init__(self, sfen_stand: str):
        self.array = np.zeros(dtype="int8", shape=7)
        amount = 1

        for char in sfen_stand:
            if char.isalpha():
                self.array[en_to_num[char] - 1] += amount
                amount = 1
            else:
                amount = int(char)


class Board(object):
    def is_regal(self):
        pass

    def _action(self, act_type="", sr=-1, sc=-1, dr=-1, dc=-1, p_num=-1, p_flag=False):
        """移動するための関数です　呼び出し時にはキーワード引数を使用してください

        短い変数の意味はFieldクラスのdocstringを参照してください

        :param act_type:moveで移動を意味しています、dropで打ちを意味しています

        :param sr: src_rowの意
        :param sc:src_colの意

        :param dr:dst_rowの意
        :param dc:dst_colの意

        :param p_num:piece_numの意
        :param p_flag:Trueにすると成ります　act_typeがmoveであるかの判定をしません

        :return:
        """
        pass

    def action_kif(self, action):
        """
        :param action:kif形式の動き部分をサポートします
        入力例１　移動先座標と移動元座標のみのデータ
        ７六歩(77)

        入力例２　kif形式の位置行をそのまま入れるパターンでも可能です（手数・時間の部分は無視されます）
        55 ２九飛(24)        ( 0:00/00:00:02)

        入力例




        :return:
        """
        pass

    def show(self):
        pass

    def __init__(self, sfen, validation=True):
        """
        :param sfen:
        :param validation:Falseの場合、指し手や局面の合法チェックをしません、
        """

        title, field, turn, hand, cnt = list(sfen.split(" "))

        # 持ち駒要素を分割
        w = ""
        b = ""
        for i in range(len(hand) - 1, 0, -1):
            if hand[i].isupper():
                w = hand[:i + 1]
                b = hand[i + 1:]
                break

        self.turn = turn
        self.move_count = int(cnt)
        self.validation = validation

        self.field = _Field(field)
        self.hand_w = _PieceStand(w)
        self.hand_b = _PieceStand(b)

    pass


if __name__ == '__main__':
    sfen = ["sfen l3k1g1+B/2g2g3/p2sb3p/2p1p1+S2/1r1S1p3/2P1P4/P2GnP2P/K2P+p4/LN5RL b SNL4Pn2p 102",
            "sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1",
            "sfen lr2k1b1l/2sg2g2/p4snpp/2pNp2P1/3S1pS2/1PPGP4/P4P2P/2GB1+p3/LNK4RL w 4Pn 62"
            ]

    b = Board(sfen=sfen[0])

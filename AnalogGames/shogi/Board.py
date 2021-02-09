# coding:UTF-8


class _PieceIndexError(Exception):
    """
    指定座標が範囲外であることを意味します
    """
    pass


class _NoPieceError(Exception):
    """
    指定座標に駒が存在しないことを意味します
    """
    pass


class _PromotedAlreadyError(Exception):
    """
    指定座標の駒がすでに成っていることを意味します
    """
    pass


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
        :param col: 盤面の最上段を0としたインデックス　言い換えればX軸

        :raise PieceIndexError 指定座標が範囲外であることを意味します
        :raise NoPieceError 指定座標に駒が存在しないことを意味します
        :raise PromotedAlreadyError 指定座標の駒がすでに成っていることを意味します
        """

        if row not in range(9) or col not in range(9):
            raise _PieceIndexError("row:{} col:{}", format(row, col))

        piece_num = self._array[row][col]

        if abs(piece_num) > 10:
            raise _PromotedAlreadyError("row:{} col:{}".format(row, col))

        return

    def pop(self) -> int:
        pass

    def drop(self, row, col):
        """
        :param row:
        :param col:
        :return:
        """
        pass

    def move(self, row, col):
        pass

    def __init__(self, sfen_head: str = ""):
        """
        :param sfen_head: sfen形式の文字列の前半の盤面を意味する部分　分割処理は呼び出し元が担当する
        """
        self._array = [[0 for i in range(9)] for j in range(9)]


class _PieceStand(object):
    pass


class Board(object):
    def __init__(self):
        hand_w = _PieceStand()
        hand_b = _PieceStand()

    pass

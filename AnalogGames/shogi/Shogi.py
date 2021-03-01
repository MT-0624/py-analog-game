# coding:UTF-8

import sys

sys.path.append("../")

import numpy as np
import re

from Board import Board
from piece_dictionary import \
    en_to_num, num_to_en, fmt_destination, fmt_source, fmt_piece, str2int, piece_kanji2num, kanji_piece_to_num
from Exceptions import *


class _Field(Board):
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

    def show(self):
        # 盤面出力
        grid = "".join(["+---" for i in range(9)]) + "+"

        print(grid)
        for row in range(9):
            for col in range(9):
                num = self.array[row][col]

                if num == 0:
                    txt = "  "
                else:
                    txt = num_to_en[num]

                print("|{:^3s}".format(txt), end="")
            else:
                print("|")
                print(grid)

    def get_piece_num(self, coordination):
        row, col = coordination
        return self.array[row][col]

    def flip(self, source):
        """
        指定した地点の駒を裏表回転させます
        成ったり成りを戻したりできます

        :param source:

        :raise PieceIndexError 指定座標が範囲外であることを意味します
        :raise NoPieceError 指定座標に駒が存在しないことを意味します
        :raise PromotedAlreadyError 指定座標の駒がすでに成っていることを意味します
        """

        row, col = source

        self._range_check(row, col)

        piece_num = self.array[row][col]

        if piece_num == 0:
            raise NoPieceError("row:{} col:{}", format(row, col))
        if piece_num in (5, 8):
            raise Exception("InflippablePiece row:{} col:{} piece_num:{}".format(row, col, piece_num))

        if abs(piece_num) > 10:
            # 戻しの処理
            if piece_num > 0:
                self.array[row][col] -= 10
            else:
                self.array[row][col] += 10

        else:
            # 成りの処理
            if piece_num > 0:
                self.array[row][col] += 10
            else:
                self.array[row][col] -= 10

        return self.array[row][col]

    def __init__(self, sfen_head: str = ""):
        """
        :param sfen_head: sfen形式の文字列の前半の盤面を意味する部分　分割処理は呼び出し元が担当する
        """
        super().__init__(size=9)

        rows = sfen_head.split("/")

        for i, row in enumerate(rows):
            j = 0
            promo = False
            for char in row:
                if char.isnumeric():
                    j += int(char) - 1
                elif char == "+":
                    promo = True
                    continue
                else:
                    p_num = en_to_num[char]
                    if promo:
                        if p_num > 0:
                            p_num += 10
                        else:
                            p_num -= 10

                    self.array[i][j] = p_num

                    promo = False

                j += 1


class _PieceStand(object):
    def show(self):
        output = []
        for i in range(1, 8):
            amount = self.get_amount(i)
            if amount == 0:
                continue
            output.append("{}x{}".format(num_to_en[i], amount))

        if len(output) == 0:
            print("無し")
        else:
            print(" ".join(output))

    def get_amount(self, piece_name):
        """
        :param piece_name:駒番号　正負関係なく絶対値で検索するのでどちらでも可能
        :return amount:駒の数量
        """

        amount = self.array[abs(piece_name) - 1]
        return amount

    def decrease(self, piece_num, amount=1):
        if self.array[piece_num - 1] < amount:
            raise NoPieceError("piece_num:{}".format(piece_num))

        self.array[piece_num - 1] -= 1

    def increase(self, piece_num, amount=1):
        piece_num = abs(piece_num)
        self.array[piece_num - 1] += amount

    def __init__(self, sfen_stand: str):
        self.array = np.zeros(dtype="int8", shape=7)
        amount = 1

        for char in sfen_stand:
            if char.isalpha():
                piece_index = abs(en_to_num[char]) - 1
                self.array[piece_index] += amount
                amount = 1
            else:
                amount = int(char)


class ShogiBoard(object):
    def is_regal(self):
        pass

    def put(self, destination: tuple, p_num):
        if self.turn == 1:
            self.field.drop(destination, p_num)
            self.hand_white.decrease(p_num)
        else:
            self.field.drop(destination, p_num * -1)
            self.hand_black.decrease(p_num)

        self._last_move = destination
        self.turn *= -1

    def move(self, source: tuple, destination: tuple, p_flag=False):
        """移動するための関数です　呼び出し時にはキーワード引数を使用してください

        短い変数の意味はFieldクラスのdocstringを参照してください

        :param source:
        :param destination:
        :param p_flag:Trueにすると成ります　act_typeがmoveであるかの判定をしません

        :return:
        """

        # 駒があれば取る処理
        if abs(self.field.get_piece_num(destination)) > 10:
            self.field.flip(destination)

        take_piece = self.field.get_piece_num(destination)

        if take_piece != 0:
            # 取る駒が敵のものであることをチェック
            if np.sign(take_piece) == self.turn:
                raise FriendlyFireError(take_piece)

            if self.turn == 1:
                self.hand_white.increase(self.field.pop(destination))
            if self.turn == -1:
                self.hand_black.increase(self.field.pop(destination))

        moving_piece = self.field.get_piece_num(source)

        self.field.move(source=source, destination=destination)

        # 必要に応じて成る
        if p_flag:
            self.field.flip(destination)

        self._last_move = destination
        self.turn *= -1

    def action_kif(self, txt):
        """
        :param txt:kif形式の動き部分をサポートします
        入力例１　移動先座標と移動元座標のみのデータ
        ７六歩(77)

        入力例２　kif形式の位置行をそのまま入れるパターンでも可能です（手数・時間の部分は無視されます）
        55 ２九飛(24)        ( 0:00/00:00:02)

        入力例
        :return:
        """
        import pdb
        if "打" in txt:
            piece_obj = fmt_piece.search(txt).group()
            assert piece_obj is not None
            piece_obj = kanji_piece_to_num[piece_obj]

            dest_text = fmt_destination.search(txt).group()
            assert dest_text is not None
            destination = (str2int(dest_text[1]) - 1, 9 - str2int(dest_text[0]))
            self.put(destination, p_num=piece_obj)
        else:
            if fmt_destination.search(txt) is None:
                if "同" in txt:
                    destination = self._last_move
                else:
                    raise ValueError(txt)
            else:
                dest_text = fmt_destination.search(txt).group()
                destination = (str2int(dest_text[1]) - 1, 9 - str2int(dest_text[0]))

            if fmt_source.search(txt):
                src_text = fmt_source.search(txt).group()
                source = (int(src_text[2]) - 1, 9 - int(src_text[1]))
            else:
                raise SyntaxError(txt)

            piece_obj = fmt_piece.search(txt)
            assert piece_obj is not None

            piece_ind = piece_obj.start()

            promote = False

            if "成" in txt:
                promote_ind = txt.index("成")

                if piece_ind < promote_ind:
                    promote = True

            self.move(source=source, destination=destination, p_flag=promote)

    def show(self, turn_label="【手番】"):
        splitter = "-" * 40
        print(splitter)
        print("後手持駒", end="")
        if self.turn == -1:
            print(turn_label)
        else:
            print()

        self.hand_black.show()
        self.field.show()
        self.hand_white.show()

        print("先手持駒", end="")
        if self.turn == 1:
            print(turn_label)
        else:
            print()
        print(splitter)

    def __init__(self, sfen, validation=True):
        """
        :param sfen:
        :param validation:
        """

        # sfen形式は先頭に”sfen”と書いてある場合とない場合がある
        if sfen[:4] == "sfen":
            sfen_title, sfen_field, sfen_turn, hand, cnt = list(sfen.split(" "))
            del sfen_title
        else:
            sfen_field, sfen_turn, hand, cnt = list(sfen.split(" "))

        # 持ち駒要素を分割
        txt_w = ""
        txt_b = ""

        # 末尾から検索し、先後の持ち駒文字列を分割する
        for i in range(len(hand) - 1, -1, -1):
            if hand[i].isupper():
                txt_w = hand[:i + 1]
                txt_b = hand[i + 1:]
                break
        else:
            txt_b = hand

        self.turn = 1 if sfen_turn == "b" else -1
        self.move_count = int(cnt)
        self.regal_check_flag = validation

        # なにもない場合kif形式はハイフンが書かれているので除去
        if txt_b == "-":
            txt_b = ""

        self.field = _Field(sfen_field)
        self._last_move = (int(), int())  # 同　○　と表記されているときにこの変数を移動先にする

        self.hand_white = _PieceStand(txt_w)
        self.hand_black = _PieceStand(txt_b)


if __name__ == '__main__':
    # sfen形式を引数にShogiBoardオブジェクトを作成できます
    sample_board = ShogiBoard("sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1")

    # 盤面の表示
    sample_board.show()
    sample_board.show(turn_label="●")  # 任意のマークで手番を示すオプションあり。デフォルトは"【手番】"

    move1 = "７六歩(77)"  # kif形式の動きをサポートしています。
    sample_board.action_kif(move1)

    # kif形式の中で必要な値のみ取得するのでその他記号は無視されます
    move2 = "   2 ８四歩(83)        ( 0:00/00:00:00)"
    sample_board.action_kif(move2)

    sample_board.show()

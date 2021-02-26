# coding:UTF-8

import re

number_txt_and_int = {}  # 棋譜から座標を得るために使用

for i, kanji_num in enumerate("一二三四五六七八九"):
    number_txt_and_int[kanji_num] = i + 1
    number_txt_and_int[i + 1] = kanji_num

for i, kanji_num in enumerate("１２３４５６７８９"):
    number_txt_and_int[kanji_num] = i + 1
    number_txt_and_int[i + 1] = kanji_num

promotable = [1, 2, 3, 4, 6, 7]
promotable.extend([i * -1 for i in promotable])  # 後手の成駒

en_to_num = {
    "P": 1,
    "N": 2,
    "L": 3,
    "S": 4,
    "G": 5,
    "B": 6,
    "R": 7,
    "K": 8,

    "p": -1,
    "n": -2,
    "l": -3,
    "s": -4,
    "g": -5,
    "b": -6,
    "r": -7,
    "k": -8
}
num_to_en = dict([(v, k) for k, v in en_to_num.items()])

# 成駒も辞書に追加する
promo_dict = dict()

for num, eng in num_to_en.items():
    if num in promotable:
        if num > 0:
            promo_dict[num + 10] = "+" + eng
        else:
            promo_dict[num - 10] = "+" + eng

fmt_destination = re.compile("[１２３４５６７８９][一二三四五六七八九]")
fmt_piece = re.compile("[歩と桂香銀金角飛馬龍王玉]")
fmt_source = re.compile("[(][1-9][1-9][)]")

num_to_en.update(promo_dict)

del promo_dict


def piece_name_to_num(piece_txt: str) -> int:
    if piece_txt.isalpha():
        return en_to_num[piece_txt]
    else:
        pass


jp_num_kanji = dict((i + 1, s) for i, s in enumerate("一二三四五六七八九"))
jp_num_kanji.update(dict((s, i + 1) for i, s in enumerate("一二三四五六七八九")))

jp_num_fullcamel = dict((i + 1, s) for i, s in enumerate("１２３４５６７８９"))
jp_num_fullcamel.update(dict((s, i + 1) for i, s in enumerate("１２３４５６７８９")))

kanji_piece_to_num = {}

for i, jp in zip([1, 10, 2, 3, 4, 5, 6, 7, 16, 17, 8, 8], "歩と桂香銀金角飛馬龍王玉"):
    kanji_piece_to_num[jp] = i


def piece_kanji2num(value, sign: int, promoted=False):
    p_num = kanji_piece_to_num[value]
    p_num *= sign
    if promoted:
        p_num = 10 * sign

    return p_num


def str2int(value):
    """
    漢数字及び全角数字とintを相互変換します

    :param value:
    :return:valueがintなら
    """

    if type(value) == str:
        if value in jp_num_fullcamel.keys():
            return jp_num_fullcamel[value]

        if value in jp_num_kanji.keys():
            return jp_num_kanji[value]

        raise KeyError(value)

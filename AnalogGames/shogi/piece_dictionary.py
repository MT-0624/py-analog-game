# coding:UTF-8

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

# coding:UTF-8

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


num_to_en.update(promo_dict)

del promo_dict
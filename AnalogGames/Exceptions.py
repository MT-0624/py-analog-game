# coding:UTF-8

class PieceIndexError(Exception):
    """
    指定座標が範囲外であることを意味します
    """
    pass


class FriendlyFireError(Exception):
    """
    取ろうとした駒が味方のものであるときに挙げます
    """
    pass


class NoPieceError(Exception):
    """
    指定座標に駒が存在しないことを意味します
    """
    pass


class PieceExistsError(Exception):
    """
    指定座標に駒が存在することを意味します
    """
    pass


class PieceNotFoundError(Exception):
    """
    指定座標に駒が存在しないことを意味します
    """
    pass


class PromotedAlreadyError(Exception):
    """
    指定座標の駒がすでに成っていることを意味します
    """
    pass


class ilegalBoardError(Exception):
    """
    局面が以下のルールに則っていないことを意味します

    二歩　同じ列に歩が2枚ある
    自殺手・王手放置　相手の手番でありながら自玉に王手がかかっている
    膠着　奥への桂馬不成などルール上身動きができない駒がある場合
    """

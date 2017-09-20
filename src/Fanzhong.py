# -*- coding: utf-8 -*-
import numpy as np
import constants
import abc
from Hand import Hand


class FanZhong:
    def __init__(self):
        pass

    @property
    def fanshu(self):
        """
        fanshu should be a length 2 * 2 list as [[bimenyiman, bimenputong], [kaimenyiman, kaimenputong]]
        :return:
        """
        raise NotImplementedError

    @property
    def chinese_name(self):
        """
        Chinese Name of the FanZhong
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        """
        Judge whether the provided hand set satisfy the Fanzhong.
        :param _hand: Hand Class Object
        :param _expression: We assume that the _expression has already been re-formatted as a dictionary with 'kezi',
        'shunzi' and 'quetou'. Otherwise it will lead to repeat of coding.
        :return:
        """


class GuoShi(FanZhong):
    fanshu = [[1, 0], [0, 0]]
    chinese_name = u'国士无双'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if set(_hand.in_hand + [_hand.new_tile]) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        set(_hand.in_hand) != {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47}:
            return True
        else:
            return False


class GuoShiShiSanMian(FanZhong):
    fanshu = [[2, 0], [0, 0]]
    chinese_name = u'国士无双十三面待'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if set(_hand.in_hand) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        _hand.new_tile in [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]:
            return True
        else:
            return False


class QiDui(FanZhong):
    fanshu = [[0, 2], [0, 0]]
    chinese_name = u'七对子'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        _list_pai = _hand.in_hand + [_hand.new_tile]
        _list_pai.sort()
        if [_list_pai[x] for x in range(0, 13, 2)] == [_list_pai[x] for x in range(1, 14, 2)] and len(
                set(_list_pai)) == 7:
            return True
        else:
            return False


class SiGangZi(FanZhong):
    fanshu = [[2, 0], [2, 0]]
    chinese_name = u'四杠子'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_hand.fulu) == 4:
            for i in range(4):
                if _hand.fulu[i].name != 'Ming_Gang' and _hand.fulu[i].name != 'An_Gang':
                    return False

            return True

        return False


class SanGangZi(FanZhong):
    fanshu = [[0, 2], [0, 2]]
    chinese_name = u'三杠子'

    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_hand.fulu) >= 3:
            count_of_gangs = 0
            for i in range(len(_hand.fulu)):
                if _hand.fulu[i].name == 'Ming_Gang' or _hand.fulu[i].name == 'An_Gang':
                    count_of_gangs += 1

            if count_of_gangs == 3:
                return True

        return False


class LiangBeiKou(FanZhong):
    fanshu = [[0, 3], [0, 0]]
    chinese_name = u'两盃口'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_hand.fulu) == 0:
            if len(_expression['shunzi']) == 4:
                if _expression['shunzi'][0] == _expression['shunzi'][1] and _expression['shunzi'][2] == \
                        _expression['shunzi'][3]:
                    return True

        return False


class PingHe(FanZhong):
    fanshu = [[0, 1], [0, 0]]
    chinese_name = u'平和'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo, fu):
        if len(_hand.fulu) == 0:
            if (fu == 20 and is_zimo) or (fu == 30 and not is_zimo):
                return True

        return False


class SanSe(FanZhong):
    fanshu = [[0, 2], [0, 1]]
    chinese_name = u'三色同顺'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['shunzi']) >= 3:
            shunzi_start = [shunzi[0] for shunzi in _expression['shunzi']]
            if set([shunzi_start[0] + x for x in range(0, 30, 10)]).issubset(shunzi_start) or set(
                    [shunzi_start[1] + x for x in range(0, 30, 10)]).issubset(shunzi_start):
                return True

        return False


class YiQi(FanZhong):
    fanshu = [[0, 2], [0, 1]]
    chinese_name = u'一气通贯'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['shunzi']) >= 3:
            shunzi_start = [shunzi[0] for shunzi in _expression['shunzi']]
            if set([shunzi_start[0] + x for x in range(0, 9, 3)]).issubset(shunzi_start) or set(
                    [shunzi_start[1] + x for x in range(0, 9, 3)]).issubset(shunzi_start):
                return True

        return False


class YiBeiKou(FanZhong):
    fanshu = [[0, 1], [0, 0]]
    chinese_name = u'一盃口'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if is_close:
            if len(_expression['shunzi']) >= 2:
                shunzi_start = [shunzi[0] for shunzi in _expression['shunzi']]
                if len(set(shunzi_start)) < len(shunzi_start):
                    if len(shunzi_start) == 4:
                        if shunzi_start[0] == shunzi_start[1] and shunzi_start[2] == shunzi_start[3]:
                            return False

                    return True

        return False


class DaSiXi(FanZhong):
    fanshu = [[2, 0], [2, 0]]
    chinese_name = u'大四喜'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['kezi']) == 4:
            kezi_start = [kezi[0] for kezi in _expression['kezi']]
            if set(kezi_start) == {41, 42, 43, 44}:
                return True

        return False


class SiAnKe(FanZhong):
    fanshu = [[1, 0], [0, 0]]
    chinese_name = u'四暗刻'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['kezi']) == 4 and is_zimo and is_close:
            if _hand.new_tile not in _expression['quetou']:
                return True

        return False


class SiAnKeDanQi(FanZhong):
    fanshu = [[2, 0], [0, 0]]
    chinese_name = u'四暗刻单骑'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['kezi']) == 4 and is_close:
            if _hand.new_tile in _expression['quetou']:
                return True

        return False


class ZiYiSe(FanZhong):
    fanshu = [[1, 0], [1, 0]]
    chinese_name = u'字一色'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if set(_hand.in_hand + [_hand.new_tile]).issubset({41, 42, 43, 44, 45, 46, 47}):
            return True
        else:
            return False


class QingLaoTou(FanZhong):
    fanshu = [[1, 0], [1, 0]]
    chinese_name = u'清老头'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if set(_hand.in_hand + [_hand.new_tile]).issubset({11, 19, 21, 29, 31, 39}):
            return True
        else:
            return False


class DuiDuiHe(FanZhong):
    fanshu = [[0, 2], [0, 2]]
    chinese_name = u'对对和'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['kezi']) == 4:
            if not is_close or (not is_zimo and _hand.new_tile not in _expression['quetou'][0]):
                if not ZiYiSe.judge(_hand, _expression, is_close, is_zimo) and QingLaoTou.judge(_hand, _expression,
                                                                                                is_close, is_zimo):
                    return True

        return False


class HunLaoTou(FanZhong):
    fanshu = [[0, 2], [0, 2]]
    chinese_name = u'混老头'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if set(_hand.in_hand + [_hand.new_tile]).issubset({11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47}):
            if not set(_hand.in_hand + [_hand.new_tile]).issubset({11, 19, 21, 29, 31, 39}) and not set(
                            _hand.in_hand + [_hand.new_tile]).issubset({41, 42, 43, 44, 45, 46, 47}):
                return True

        return False


class DaQiXing(FanZhong):
    fanshu = [[1, 0], [0, 0]]
    chinese_name = u'大七星'

    def judge(cls, _hand, _expression, is_close, is_zimo):
        if set(_hand.in_hand + [_hand.new_tile]) == {41, 42, 43, 44, 45, 46, 47}:
            return True

        else:
            return False


class DaSanYuan(FanZhong):
    fanshu = [[1, 0], [1, 0]]
    chinese_name = u'大三元'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['kezi']) >= 3:
            kezi_start = [kezi[0] for kezi in _expression['kezi']]
            if {45, 46, 47}.issubset(set(kezi_start)):
                return True

        return False


class XiaoSiXi(FanZhong):
    fanshu = [[1, 0], [1, 0]]
    chinese_name = u'小四喜'

    @classmethod
    def judge(cls, _hand, _expression, is_close, is_zimo):
        if len(_expression['kezi']) >= 3:
            kezi_start = [kezi[0] for kezi in _expression['kezi']]
            if kezi_start != [41, 42, 43, 44] and set(kezi_start + _expression['quetou'][0]) == {41, 42, 43, 44}:
                if not DaQiXing.judge(_hand, _expression, is_close, is_zimo):
                    return True

        return False

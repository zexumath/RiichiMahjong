import numpy as np
from Game import Player
import constants
import abc
from Hand import Hand


class FanZhong:
    @property
    def fanshu(self):
        '''
        fanshu should be a length 2 * 2 list as [[bimenyiman, bimenputong], [kaimenyiman, kaimenputong]]
        :return:
        '''
        raise NotImplementedError

    @property
    def chinese_name(self):
        '''
        Chinese Name of the FanZhong
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def judge(self, _hand, _expression):
        '''
        Judge whether the provided pai set satisfy the Fanzhong.
        :param _hand: Hand Class Object
        :return:
        '''


class GuoShi(FanZhong):
    fanshu = [[1, 0], [0, 0]]
    chinese_name = u'国士无双'

    @classmethod
    def judge(cls, _hand, _expression):
        if set(_hand.in_hand + [_hand.new_tile]) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        set(_hand.in_hand) != {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47}:
            return True
        else:
            return False


class GuoShiShiSanMian(FanZhong):
    fanshu = [[2, 0], [0, 0]]
    chinese_name = u'国士无双十三面待'

    @classmethod
    def judge(self, _hand, _expression):
        if set(_hand.in_hand) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        _hand.new_tile in [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]:
            return True
        else:
            return False


class QiDui(FanZhong):
    fanshu = [[0, 2], [0, 0]]
    chinese_name = u'七对子'

    @classmethod
    def judge(self, _hand, _expression):
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

    def judge(self, _hand, _expression):
        if len(_hand.fulu) == 4:
            for i in range(4):
                if _hand.fulu[i].name != 'Ming_Gang' and _hand.fulu[i].name != 'An_Gang':
                    return False

        return False


class SanGangZi(FanZhong):
    fanshu = [[0, 2], [0, 2]]
    chinese_name = u'三杠子'

    def judge(self, _hand, _expression):
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

    def judge(self, _hand, _expression):
        '''
        :param _hand:
        :param _expression: We assume that the _expression has already been re-formatted as a dictionary with 'kezi',
        'shunzi' and 'quetou'. Otherwise it will lead to repeat of coding.
        :return:
        '''
        if len(_hand.fulu) == 0:
            if len(_expression['shunzi']) == 4:
                if _expression['shunzi'][0] == _expression['shunzi'][1] and _expression['shunzi'][2] == \
                        _expression['shunzi'][3]:
                    return True

            return False

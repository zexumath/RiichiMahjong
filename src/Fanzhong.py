import numpy as np
from src.mahjong import player
import constants
import abc


class FanZhong:
    @property
    def fanshu(self):
        '''
        fanshu should be a length 2 * 2 list as [[bimenyiman, bimenputong], [kaimenyiman, kaimenputong]]
        :return:
        '''
        raise NotImplementedError

    @abc.abstractmethod
    def judge(self, _pai):
        '''
        Judge whether the provided pai set satisfy the Fanzhong.
        :param _pai:
        :return:
        '''

class GuoShi(FanZhong):
    fanshu = [[1, 0], [None, None]]

    @classmethod
    def judge(cls, _pai):
        if set(_pai[0] + _pai[1]) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        set(_pai[0]) != {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47}:
            return True
        else:
            return False

class GuoShiShiSanMian(FanZhong):
    fanshu = [[2, 0], [None, None]]

    @classmethod
    def judge(self, _pai):
        if set(_pai[0]) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        _pai[1][0] in [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]:
            return True
        else:
            return False

class QiDui(FanZhong):
    fanshu = [[0, 2], [None, None]]

    @classmethod
    def judge(self, _pai):
        _list_pai = _pai[0] + _pai[1]
        _list_pai.sort()
        if [_list_pai[x] for x in range(0,13,2)] == [_list_pai[x] for x in range(1,14,2)] and len(set(_list_pai)) == 7:
            return True
        else:
            return False



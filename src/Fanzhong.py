import numpy as np
from src.Mahjong import player
import abc


class Fanzhong:
    @property
    def fanshu(self):
        raise NotImplementedError

    @abc.abstractmethod
    def judge(self, _pai):
        '''
        Judge whether the provided pai set satisfy the Fanzhong.
        :param _pai:
        :return:
        '''

class Guoshi(Fanzhong):
    fanshu = [1, 0]

    def judge(self, _pai):
        if set(_pai[0] + _pai[1]) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        set(_pai[0]) != {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47}:
            return True
        else:
            return False


class Guoshishisanmian(Fanzhong):
    fanshu = [2, 0]
    def judge(self, _pai):
        if set(_pai[0]) == {11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47} and \
                        _pai[1][0] in [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]:
            return True
        else:
            return False



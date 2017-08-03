# -*- coding: utf-8 -*-
# MyLibrary.py

import random, math
from constants import *
from Hand import Hand
from Util import Util
import time
from Fanzhong import FanZhong, PingHe

class Player(object):
    def __init__(self, name='AI'):
        #need to be in Hand class
        #self.mopai = []
        #self.hand = []
        self.name = name
        self.hand = Hand()
        self.chi = []
        self.peng = []
        self.mgang = []
        self.agang = []
        self.hand.fulu = []
        self.ontable = []

        self.dropped = []
        self.is_close = True
        self.riichi = 0
        self.zimo = False
        self.rongpai = 0
        self.fu = {}
        self.yi = {}
        self.exp = {}
        self.dedian = 0
        #以下两个每局不用初始化
        self.money = MONEY_START
        self.position = -1

        self.gangTag = False
        self.analysisTag = False
        self.rongflag = False
        self.lingshang = False
        self.tingflag = False
        self.isclose = True
        self.kaimen = False

    def newset_init(self):
        #need to be in Hand class
        #self.mopai = []
        #self.hand = []
        self.hand = Hand()
        self.chi = []
        self.peng = []
        self.mgang = []
        self.agang = []
        self.hand.fulu = []
        self.ontable = []

        self.dropped = []
        self.isclose = True
        self.riichi = False
        self.zimo = False
        self.rongpai = 0
        self.fu = {}
        self.yi = {}
        self.exp = {}
        self.dedian = 0
        self.rongflag = False
        self.lingshang = False
        self.tingflag = False
        self.gangTag = False
        self.analysisTag = False
        self.isclose = True
        self.kaimen = False

    def drop(self, tileindex):
        if self.riichi > 0:
            if tileindex == len(self.hand.in_hand):
                self.dropped.append(self.hand.new_tile)
                self.hand.new_tile = None
                return self.dropped[-1]
            else:
                return False
        elif self.kaimen:
            self.dropped.append(self.hand.in_hand[tileindex])
            self.hand.in_hand.remove(self.hand.in_hand[tileindex])
            self.hand.in_hand.sort()
            self.kaimen = False
            return self.dropped[-1]
        else:
            if tileindex == len(self.hand.in_hand):
                self.dropped.append(self.hand.new_tile)
                self.hand.new_tile = None
                return self.dropped[-1]
            else:
                self.dropped.append(self.hand.in_hand[tileindex])
                self.hand.in_hand[tileindex] = self.hand.new_tile
                self.hand.in_hand.sort()
                self.hand.new_tile = None
                return self.dropped[-1]

    def gang(self, tileindex):
        if self.riichi > 0:
            if tileindex == len(self.hand.in_hand) + 1:
                if self.keyigang(self.hand.new_tile):
                    self.hand.fulu.append([self.hand.new_tile] * 4)
                    self.hand.in_hand.remove(self.hand.new_tile)
                    self.hand.in_hand.remove(self.hand.new_tile)
                    self.hand.in_hand.remove(self.hand.new_tile)
                    return True
                else:
                    return False
            else:
                # TODO: Here we assume the only clickable tile for gang after
                #      riichi is called is the new tile.
                return False
        else:
            if tileindex == len(self.hand.in_hand) + 1:
                if self.keyigang(self.hand.new_tile):
                    self.hand.fulu.append([self.hand.new_tile] * 4)
                    self.hand.in_hand.remove(self.hand.new_tile)
                    self.hand.in_hand.remove(self.hand.new_tile)
                    self.hand.in_hand.remove(self.hand.new_tile)
                    return True
                else:
                    return False
            else:
                if self.keyigang(self.hand.in_hand[tileindex]):
                    self.hand.fulu.append([self.hand.in_hand[tileindex]] * 4)
                    gangpai = self.hand.in_hand[tileindex]
                    self.hand.in_hand.append(self.hand.new_tile)
                    self.hand.in_hand.remove(gangpai)
                    self.hand.in_hand.remove(gangpai)
                    self.hand.in_hand.remove(gangpai)
                    self.hand.in_hand.remove(gangpai)
                    self.hand.in_hand.sort()
                    return True
                else:
                    return False

    def keyigang(self, _pai):
        tmp = self.hand.in_hand + [self.hand.new_tile]
        if tmp.count(_pai) == 4:
            return True
        else:
            return False

    def chipai(self, chipai):
        raise NotImplementedError

    def pengpai(self, pengpai):
        if self.riichi > 0:
            return False
        else:
            self.hand.fulu.append([pengpai] * 3)
            self.hand.in_hand.append(pengpai)
            self.hand.in_hand.remove(pengpai)
            self.hand.in_hand.remove(pengpai)
            self.hand.in_hand.remove(pengpai)
            self.hand.in_hand.sort()
            return True

    def calcfu(self, quan, oya):
        # TODO: Move all constants into constants.py
        (exp, flag) = self.exp, self.rongflag
        if flag == False:
            self.fu = {1: 0}
        else:
            res = 20
            self.fu = {}.fromkeys(exp.keys(), 0)
            # mingke
            for kezi in self.peng:
                tmp = kezi[0]
                if Util.isyao(tmp):
                    res += 4
                else:
                    res += 2
            # gang
            for a in self.hand.fulu:
                tmp = a[0]
                if Util.isyao(tmp):
                    res += 32
                else:
                    res += 16
            for a in self.mgang:
                tmp = a[0]
                if Util.isyao(tmp):
                    res += 16
                else:
                    res += 8
            for k, v in exp.items():
                if len(v) == 7 or len(v) == 13:
                    self.fu[k] = 25
                    continue
                for tmp in v:
                    if len(tmp) == 2: break
                self.fu[k] += res
                tmp1, tmp2 = tmp[0] // 10, tmp[0] % 10
                if tmp1 == 4:
                    if tmp2 == quan % 4 + 1:
                        self.fu[k] += 2
                    if tmp2 == (self.position - oya) % 4 + 1:
                        self.fu[k] += 2
                    if tmp2 >= 5:
                        self.fu[k] += 2
                for zuhe in v:
                    if len(zuhe) == 2:
                        continue
                    elif zuhe[1] == zuhe[0]:
                        if self.zimo > 0 or self.rongpai != zuhe[0]:
                            if Util.isyao(zuhe[0]):
                                self.fu[k] += 8
                            else:
                                self.fu[k] += 4
                        else:
                            tag = 0
                            if self.rongpai == zuhe[0]:
                                for tmp in v:
                                    if self.rongpai in tmp and tmp != zuhe:
                                        tag = 1
                            if tag == 0:
                                if Util.isyao(zuhe[0]):
                                    self.fu[k] += 4
                                else:
                                    self.fu[k] += 2
                            else:
                                if Util.isyao(zuhe[0]):
                                    self.fu[k] += 8
                                else:
                                    self.fu[k] += 4
                if self.fu[k] == 20 and self.is_close:
                    tag = 0
                    for zuhe in v:
                        if len(zuhe) == 3 and zuhe[0] != zuhe[1] and self.rongpai in zuhe:
                            if Util.is_liangmian(zuhe, self.rongpai):
                                self.fu[k] = 20
                                tag = 1
                                break
                            else:
                                self.fu[k] = 22
                                tag = 1
                    if tag == 0:
                        self.fu[k] = 22
                    if self.zimo == 0:
                        self.fu[k] += 10
                    elif self.fu[k] != 20:
                        self.fu[k] += 2
                else:
                    for zuhe in v:
                        if len(zuhe) == 2 and zuhe[0] == self.rongpai:
                            self.fu[k] += 2
                            break
                        if len(zuhe) == 3 and zuhe[0] != zuhe[1] and self.rongpai in zuhe:
                            if Util.is_liangmian(zuhe, self.rongpai):
                                continue
                            else:
                                self.fu[k] += 2
                                break
                    if self.zimo != 0:
                        self.fu[k] += 2
                    elif self.is_close:
                        self.fu[k] += 10

    def calcyi(self, quan, oya):
        exp, flag = self.exp, self.rongflag
        if flag == False:
            self.yi = {1: [[0], [0]]}
        else:
            self.yi = {}.fromkeys(exp.keys(), 0)
            for key in exp.keys():
                self.yi[key] = [[0], [0]]
            tmp = len(self.hand.fulu) + len(self.mgang)
            if tmp == 4:
                self.yi = {1: [[0], [1, u'四杠子']]}
            elif tmp == 3:
                self.yi[1][0][0] += 2
                self.yi[1][0].append(u'三杠子')
            for k, v in exp.items():
                if len(v) == 13:
                    for index in range(13):
                        if len(v[index]) == 2: break
                    if v[index][0] == self.rongpai:
                        self.yi[1][1][0] += 2
                        self.yi[1][1].append(u'国士无双十三面待')
                    else:
                        self.yi[1][1][0] += 1
                        self.yi[1][1].append(u'国士无双')
                    return
                kezi = []
                shunzi = []
                quetou = []
                for tmp in v:
                    if len(tmp) == 2:
                        quetou.append(tmp)
                    elif tmp[0] == tmp[1]:
                        kezi.append(tmp)
                    else:
                        shunzi.append(tmp)
                if len(quetou) == 7:
                    self.yi[k][0][0] += 2
                    self.yi[k][0].append(u'七对子')
                for tmp in self.hand.fulu + self.mgang:
                    kezi.append(tmp[:-1])
                for tmp in self.peng:
                    kezi.append(tmp)
                for tmp in self.chi:
                    shunzi.append(tmp)
                a, b = len(kezi), len(shunzi)
                kezi.sort()
                shunzi.sort()
                if [a, b] == [0, 4]:
                    if self.is_close:
                        if shunzi[1] == shunzi[0] and shunzi[3] == shunzi[2]:
                            self.yi[k][0][0] += 3
                            self.yi[k][0].append(u'两盃口')
                        if PingHe.judge(self.hand, v, self.zimo, self.fu[k]):
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'平和')
                        # if self.fu[k] == 20 and self.zimo > 0:
                        #     self.yi[k][0][0] += 1
                        #     self.yi[k][0].append(u'平和')
                        # elif self.fu[k] == 30 and self.zimo == 0:
                        #     self.yi[k][0][0] += 1
                        #     self.yi[k][0].append(u'平和')
                if b >= 3:
                    if self.sanse(shunzi):  ###
                        if self.is_close:
                            self.yi[k][0][0] += 2
                        else:
                            self.yi[k][0][0] += 1
                        self.yi[k][0].append(u'三色同顺')
                    elif self.yiqi(shunzi):  ###
                        if self.is_close:
                            self.yi[k][0][0] += 2
                        else:
                            self.yi[k][0][0] += 1
                        self.yi[k][0].append(u'一气通贯')
                if b >= 2 and self.is_close and u'两盃口' not in self.yi[k][0]:
                    if self.yibeikou(shunzi):  ###
                        self.yi[k][0][0] += 1
                        self.yi[k][0].append(u'一盃口')
                if a == 4:
                    if self.dasixi(kezi):  ###
                        self.yi[k][1][0] += 2
                        self.yi[k][1].append(u'大四喜')
                    if self.is_close:
                        if self.rongpai in quetou[0]:
                            self.yi[k][1][0] += 2
                            self.yi[k][1].append(u'四暗刻单骑')
                        elif self.zimo > 0:
                            self.yi[k][1][0] += 1
                            self.yi[k][1].append(u'四暗刻')
                    self.yi[k][0][0] += 2
                    self.yi[k][0].append(u'对对和')
                    tmp = self.laotou(kezi, quetou)  ###
                    if tmp == 3:
                        self.yi[k][1][0] += 1
                        self.yi[k][1].append(u'字一色')
                    elif tmp == 2:
                        self.yi[k][1][0] += 1
                        self.yi[k][1].append(u'清老头')
                    elif tmp == 1:
                        self.yi[k][0][0] += 2
                        self.yi[k][0].append(u'混老头')
                if len(quetou) == 7:
                    tmp = self.laotou(kezi, quetou)  ###
                    if tmp == 3:
                        self.yi[k][1][0] += 1
                        self.yi[k][1].append(u'大七星')
                    elif tmp == 1:
                        self.yi[k][0][0] += 2
                        self.yi[k][0].append(u'混老头')
                if a >= 3:
                    if self.dasanyuan(kezi):  ###
                        self.yi[k][1][0] += 1
                        self.yi[k][1].append(u'大三元')
                    elif self.xiaosixi(kezi, quetou):  ###
                        self.yi[k][1][0] += 1
                        self.yi[k][1].append(u'小四喜')
                    if self.sananke(kezi, shunzi, quetou):  ###
                        self.yi[k][0][0] += 2
                        self.yi[k][0].append(u'三暗刻')
                    if self.santongke(kezi):  ###
                        self.yi[k][0][0] += 2
                        self.yi[k][0].append(u'三色同刻')
                if a >= 2:
                    if self.xiaosanyuan(kezi, quetou):  ###
                        self.yi[k][0][0] += 2
                        self.yi[k][0].append(u'小三元')
                for zuhe in kezi:
                    if zuhe[0] // 10 != 4:
                        continue
                    else:
                        if zuhe[0] % 10 == quan % 4 + 1:
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'场风')
                        if zuhe[0] % 10 == (self.position - oya) % 4 + 1:
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'自风')
                        if zuhe[0] % 10 == 7:
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'中')
                        if zuhe[0] % 10 == 5:
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'白')
                        if zuhe[0] % 10 == 6:
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'發')
                if b >= 1:
                    tmp = self.yaojiu(kezi, shunzi, quetou)  ###
                    if tmp == 1:
                        self.yi[k][0].append(u'混全带幺九')
                    elif tmp == 2:
                        self.yi[k][0].append(u'纯全带幺九')
                    self.yi[k][0][0] += tmp
                    if tmp != 0 and self.is_close:
                        self.yi[k][0][0] += 1;
                if self.duanyao(kezi, shunzi, quetou):  ###
                    self.yi[k][0][0] += 1
                    self.yi[k][0].append(u'断幺')
                tmp = self.yise(kezi, shunzi, quetou)  ###
                if tmp == 2:
                    self.yi[k][0].append(u'混一色')
                elif tmp == 5:
                    self.yi[k][0].append(u'清一色')
                    if len(quetou) == 7:
                        if u'断幺' in self.yi[k][0]:
                            self.yi[k][1][0] += 1
                            self.yi[k][1].append(u'大车轮')
                    tmp1 = self.jiulian(kezi, shunzi, quetou)  ###
                    if tmp1 == 1:
                        self.yi[k][1].append(u'九莲宝灯')
                    elif tmp1 == 2:
                        self.yi[k][1].append(u'纯正九莲宝灯')
                    self.yi[k][1][0] += tmp1
                if tmp < 13: self.yi[k][0][0] += tmp
                if tmp != 0 and tmp < 13:
                    if self.is_close: self.yi[k][0][0] += 1
                    if self.lvyise(kezi, shunzi, quetou):
                        self.yi[k][1][0] += 1
                        self.yi[k][1].append(u'绿一色')
                if self.is_close and self.zimo > 0:
                    self.yi[k][0][0] += 1
                    self.yi[k][0].append(u'门清自摸')
                if self.riichi == 1:
                    self.yi[k][0][0] += 2
                    self.yi[k][0].append(u'两立直')
                elif self.riichi > 0:
                    self.yi[k][0][0] += 1
                    self.yi[k][0].append(u'立直')

    def rong(self, _pai, quan, oya):
        self.rongpai = _pai
        _hand = self.hand.in_hand + [_pai]
        _hand.sort()
        self.exp, self.rongflag = self.rong2(_hand)
        if self.rongflag == False:
            return ([0, 0], [0, 0], [u'诈和', 0])
        else:
            self.calcfu(quan, oya)
            self.calcyi(quan, oya)
            maxk, maxyi, maxfan = [0, 0], [0, 0], [0, 0]
            for k, v in self.yi.items():
                for i in range(2):
                    if v[i][0] > maxyi[i]:
                        maxk[i], maxyi[i], maxfan[i] = k, v[i][0], v[i][1:]
            if maxyi == [0, 0]:
                return ([0, 0], [0, 0], [u'诈和', 0])
            else:
                if maxk[0] in self.fu.keys():
                    a = self.fu[maxk[0]]
                else:
                    a = 0
                if maxk[1] in self.fu.keys():
                    b = self.fu[maxk[1]]
                else:
                    b = 0
                return ([a, b], maxyi, maxfan)

    def rong2(self, _hand):
        wan = []
        bing = []
        tiao = []
        zi = []
        hand = []
        expres = {}
        flagres = False
        for tmp in _hand:
            if tmp < 20:
                wan.append(tmp)
            elif tmp < 30:
                bing.append(tmp)
            elif tmp < 40:
                tiao.append(tmp)
            else:
                zi.append(tmp)
        a, b, c, d = [len(wan), len(bing), len(tiao), len(zi)]
        tmp = sorted([a % 3, b % 3, c % 3, d % 3])
        if tmp == [0, 0, 0, 2]:
            (flag, tmp1) = self.isqidui(_hand)
            if flag == False:
                pass
            else:
                expres[1] = tmp1
                flagres = False
            for l, _list in zip([a, b, c, d], [wan, bing, tiao, zi]):
                if l < 8:
                    (exp, flag) = Util.explain(_list)
                    if flag == False:
                        return (expres, flagres)
                    else:
                        flagres = True
                        hand = hand + exp[1]
            l = max(a, b, c, d)
            if l >= 8:
                _list = [wan, bing, tiao, zi][[a, b, c, d].index(l)]
                (exp, flag) = Util.explain(_list)
                if flag == False:
                    return (expres, flagres)
                else:
                    for key, value in exp.items():
                        exp[key] += hand
                    if len(expres) == 1:
                        exp[key + 1] = expres[1]
                    return (exp, True)
            else:
                expres[len(expres) + 1] = hand
                return (expres, flagres)
        else:
            (flag, tmp) = self.isqidui(_hand)
            if flag == False:
                pass
            else:
                return ({1: tmp}, True)
            (tmp, r) = self.isguoshi(_hand)
            if tmp > 0:
                gs = [[11], [19], [21], [29], [31], [39], [41], [42], [43], [44], [45], [46], [47]]
                gs.remove([r])
                gs.append([r, r])
                gs.sort()
                return ({1: gs}, True)
            return ({}, False)

   #  def explain(self, _list):
        # exp = {}
        # flag = False
        # test = len(_list)
        # if test % 3 == 1: return ({}, False)
        # if test == 0:
            # exp[1] = []
            # return (exp, True)
        # if _list[0] // 10 == 4:
            # if test % 3 == 0:
                # num = _list.count(_list[0])
                # if num != 3:
                    # return ({}, False)
                # else:
                    # (exp1, flag1) = Util.explain(_list[3:])
                    # if flag1 == False:
                        # return ({}, False)
                    # else:
                        # exp1[1].append(_list[:3])
                        # exp[1] = exp1[1]
                        # return (exp, True)
            # elif test % 3 == 2:
                # num = _list.count(_list[0])
                # if num != 2 and num != 3:
                    # return ({}, False)
                # else:
                    # (exp1, flag1) = Util.explain(_list[num:])
                    # if flag1 == False:
                        # return ({}, False)
                    # else:
                        # exp1[1].append(_list[:num])
                        # exp[1] = exp1[1]
                        # return (exp, True)
#         else:
            # if test % 3 == 0:
                # (_sz, _rs, issz) = Util.shunzi(_list)
                # if issz:
                    # (exp1, flag1) = Util.explain(_rs)
                    # if flag1 == False:
                        # pass
                    # else:
                        # flag = True
                        # for key, value in exp1.items():
                            # value.append(_sz)
                            # exp[key] = value
                # if Util.findSame(_list, 3):
                    # (exp1, flag1) = Util.explain(_list[3:])
                    # if flag1 == False:
                        # return ({}, False)
                    # else:
                        # flag = True
                        # tmp = len(exp)
                        # for key, value in exp1.items():
                            # value.append(_list[:3])
                            # exp[tmp + key] = value
                # return (exp, flag)
            # elif test % 3 == 2:
                # add = _list[0] // 10
                # ptou = 3 - (sum(_list) - 20 * add) % 3 + 10 * add
                # for tou in [ptou, ptou + 3, ptou + 6]:
                    # num = _list.count(tou)
                    # if num >= 2:
                        # i = _list.index(tou)
                        # (exp1, flag1) = Util.explain(_list[:i] + _list[i + 2:])
                        # if flag1 == False:
                            # continue
                        # else:
                            # flag = True
                            # tmp = len(exp)
                            # for key, value in exp1.items():
                                # value.append(_list[i:i + 2])
                                # exp[tmp + key] = value
                # return (exp, flag)

    def isqidui(self, _list):
        tmp1 = _list[0]
        res = []
        for r in range(1, 14):
            if r % 2 == 1 and _list[r] == tmp1:
                res.append([tmp1, tmp1])
                continue
            elif r % 2 == 0 and _list[r] != tmp1:
                tmp1 = _list[r]
            else:
                return (False, [])
        return (True, res)

    def isguoshi(self, _list):
        if _list[0] == _list[1]:
            tmp = _list[1:]
            r = _list[0]
        else:
            for i in range(1, 14):
                if _list[i] == _list[i - 1]:
                    break
            r = _list[i]
            _list.remove(_list[i])
            tmp = _list
        if tmp == [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]:
            if r == self.rongpai:
                return (2, r)
            else:
                return (1, r)
        else:
            return (0, 0)

    def sanse(self, shunzi):
        l = len(shunzi)
        tmp1 = [0] * l
        a = [0] * l
        for i in range(l):
            a[i], tmp1[i] = shunzi[i][0] // 10, shunzi[i][0] % 10
        if l == 3:
            if a == [1, 2, 3] and tmp1[0] == tmp1[1] == tmp1[2]: return True
        else:
            if a == [1, 1, 2, 3]:
                if tmp1[2] == tmp1[3] and tmp1[2] in tmp1[:2]: return True
            elif a == [1, 2, 2, 3]:
                if tmp1[0] == tmp1[3] and tmp1[0] in tmp1[1:3]: return True
            elif a == [1, 2, 3, 3]:
                if tmp1[0] == tmp1[1] and tmp1[0] in tmp1[2:]: return True
        return False

    def yiqi(self, shunzi):
        l = len(shunzi)
        tmp = [0] * l
        a = [0] * l
        for i in range(l):
            a[i], tmp[i] = shunzi[i][0] // 10, shunzi[i][0] % 10
        if l == 3:
            if tmp == [1, 4, 7] and a[0] == a[1] == a[2]: return True
        else:
            tmp1 = [shunzi[1], shunzi[2], shunzi[3]]
            tmp2 = [shunzi[0], shunzi[2], shunzi[3]]
            tmp3 = [shunzi[0], shunzi[1], shunzi[3]]
            tmp4 = [shunzi[0], shunzi[1], shunzi[2]]
            return self.yiqi(tmp1) or self.yiqi(tmp2) or self.yiqi(tmp3) or self.yiqi(tmp4)
        return False

    def yibeikou(self, shunzi):
        l = len(shunzi)
        tmp = [0] * l
        for i in range(l):
            tmp[i] = shunzi.count(shunzi[i])
        if max(tmp) > 1:
            return True
        else:
            return False

    def dasixi(self, kezi):
        u, a, b, c, d = kezi[0][0] // 10, kezi[0][0] % 10, kezi[1][0] % 10, kezi[2][0] % 10, kezi[3][0] % 10
        if u != 4:
            return False
        elif [a, b, c, d] == [1, 2, 3, 4]:
            return True
        else:
            return False

    def laotou(self, kezi, quetou):
        l, z = 0, 0
        laotou, zipai = [11, 19, 21, 29, 31, 39], [41, 42, 43, 44, 45, 46, 47]
        for zuhe in kezi + quetou:
            if zuhe[0] in zipai:
                z += 1
            elif zuhe[0] in laotou:
                l += 1
            else:
                return 0
        if l == 0:
            return 3
        elif z == 0:
            return 2
        else:
            return 1

    def dasanyuan(self, kezi):
        if kezi[-1][0] == 47 and kezi[-2][0] == 46 and kezi[-3][0] == 45:
            return True
        else:
            return False

    def xiaosixi(self, kezi, quetou):
        test = []
        if quetou[0][0] not in [41, 42, 43, 44]: return False
        for v in kezi + quetou:
            if v[0] // 10 != 4:
                continue
            else:
                test += [v[0]]
        test.sort()
        if test[:4] == [41, 42, 43, 44]:
            return True
        elif test[1:] == [41, 42, 43, 44]:
            return True
        else:
            return False

    def sananke(self, kezi, shunzi, quetou):
        if self.isclose:
            if self.zimo > 0:
                return True
            else:
                _find = 0
                for v in shunzi + quetou:
                    if self.rongpai in v:
                        _find = 1
                        break
                if _find == 1:
                    return True
                elif len(kezi) == 4:
                    return True
                else:
                    return False
        else:
            tmp = len(self.peng) + len(self.mgang)
            if tmp > 1:
                return False
            elif tmp == 1 and len(shunzi) > 0:
                return False
            else:
                if self.zimo > 0 or self.rongpai in quetou[0]:
                    return True
                else:
                    return False

    def santongke(self, kezi):
        l = len(kezi)
        tmp = [0] * l
        tmp1 = [0] * l
        for i in range(l):
            if kezi[i][0] // 10 == 4:
                continue
            else:
                tmp[i] = kezi[i][0] % 10
        for i in range(l):
            tmp1[i] = tmp.count(tmp[i])
        test = max(tmp1)
        if test == 3 and tmp[tmp1.index(3)] != 0:
            return True
        else:
            return False

    def xiaosanyuan(self, kezi, quetou):
        if quetou[0][0] not in [45, 46, 47]:
            return False
        else:
            if kezi[-1][0] in [45, 46, 47] and kezi[-2][0] in [45, 46, 47]:
                return True
            else:
                return False

    def yaojiu(self, kezi, shunzi, quetou):
        l, z = 0, 0
        zipai = range(41, 48)
        laotou = [11, 19, 21, 29, 31, 39]
        for v in shunzi:
            if v[0] % 10 == 1 or v[2] % 10 == 9:
                continue
            else:
                return 0
        for v in kezi + quetou:
            if v[0] in zipai:
                z += 1
            elif v[0] in laotou:
                l += 1
            else:
                return 0
        if z == 0:
            return 2
        else:
            return 1

    def duanyao(self, kezi, shunzi, quetou):
        yao = [11, 19, 21, 29, 31, 39, 41, 42, 43, 44, 45, 46, 47]
        for v in kezi + quetou:
            if v[0] in yao: return False
        for v in shunzi:
            if v[0] % 10 == 1 or v[2] % 10 == 9: return False
        return True

    def yise(self, kezi, shunzi, quetou):
        z = 0
        if len(shunzi) != 0:
            test = shunzi[0][0] // 10
            for v in kezi + shunzi + quetou:
                if v[0] // 10 == test:
                    continue
                elif v[0] // 10 == 4:
                    z += 1
                else:
                    return 0
            if z == 0:
                return 5
            else:
                return 2
        else:
            tmp = 4
            for v in kezi + quetou:
                if v[0] // 10 == 4:
                    z += 1
                elif v[0] // 10 == tmp:
                    continue
                elif tmp == 4:
                    tmp = v[0] // 10
                else:
                    return 0
            if tmp == 4:
                return 13
            elif z == 0:
                return 5
            else:
                return 2

    def jiulian(self, kezi, shunzi, quetou):
        tmp, aim = [], [1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9]
        for v in kezi + shunzi + quetou:
            tmp = tmp + v
        tmp.sort()
        for i in range(len(tmp)):
            tmp[i] = tmp[i] % 10
        rp = self.rongpai % 10
        if tmp.count(1) == 4:
            test = 1
            if tmp[1:] == aim:
                if test == rp:
                    return 2
                else:
                    return 1
            else:
                return 0
        elif tmp.count(9) == 4:
            test = 9
            if tmp[:-1] == aim:
                if test == rp:
                    return 2
                else:
                    return 1
            else:
                return 0
        else:
            for i in range(2, 9):
                if tmp.count(i) >= 2: break
            test = i
            tmp.remove(i)
            if tmp == aim:
                if test == rp:
                    return 2
                else:
                    return 1
            else:
                return 0

    def lvyise(self, kezi, shunzi, quetou):
        lv = [32, 33, 34, 36, 38, 46]
        for v in kezi + quetou:
            if v[0] in lv:
                continue
            else:
                return False
        for v in shunzi:
            if v[0] == 32:
                continue
            else:
                return False
        return True

class AiPlayer(Player):
    def __init__(self, name):
        Player.__init__(self, name)

    #ai策略1：随机打出
    def dapai1(self):
        # print self.position
        # return self.drop(random.randint(0,len(self.hand.in_hand)))
        # for debug
        return self.drop(len(self.hand.in_hand))


class GameTable():
    def __init__(self):
        self.pai = [] #all of the pai
        self.seats = []
        '''
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.player4 = Player()
        '''
        self.user = Player('Player')
        self.ai1 = AiPlayer('AI1')
        self.ai2 = AiPlayer('AI2')
        self.ai3 = AiPlayer('AI3')
        self.__create__()
        self.yama = [] # the remaining pai
        self.quan = -1 #0,1,2,3 represent east, north, west, north quan
        self.ju = 0 #东风圈二局二本场
        self.oya = OYA_START-1 % 4#0,1,2,3 represent east, north, west, north
        self.xun = 0
        self.benchang = 0
        self.lizhibang = 0
        #self.liuju = False #replaced by self.setTag
        self.lastrongplayer = -2 #没有人胡 return -2
        self.turn = -1 #0,1,2,3 represent the turn of draw tiles
        self.setTag = 0
        # self.aidropped = []

        self.on_hold_flag = False
        self.new_drop_tile = None
        self.table_status = WAIT_FOR_SERVE

    def __create__(self):
        for i in range(4):
            start = 10
            #for j in range(TILE_START + 1, TILE_START + TILE_RANGE):
            for j in range(start + 1, start + 30):
                if j % 10 != 0: self.pai.append(j)
            for k in range(41, 48):
                self.pai.append(k)
        #self.seats = [self.player1, self.player2, self.player3, self.player4]
        self.seats = [self.user, self.ai1, self.ai2, self.ai3]
        #random.shuffle(self.seats) #judge the seats: east north west north, seats[0] to call the player seating east
        for i in range(4): #seats position set for players
            self.seats[i].position = i

    def judge_benchang(self): #判断是否是下一本场, 否则切换亲家
        if self.lastrongplayer == self.oya or (self.setTag == END_LIUJU and self.seats[self.oya].tingflag):
            self.benchang += 1
        elif self.setTag == END_LIUJU and not self.seats[self.oya].tingflag:
            self.oya += 1
            self.oya %= 4
            self.benchang += 1
        else:
            self.oya += 1
            self.oya %= 4
            self.benchang = 0

    def newset(self):
        self.judge_benchang()
        # self.aidropped = []
        if self.oya == OYA_START:
            self.quan += 1
            self.quan %= 4
        self.ju = (self.oya - OYA_START) %4
        self.yama = self.pai[:]
        random.shuffle(self.yama)
        #print(self.yama)
        self.dora = [DORA_DEFAULT]
        self.ura = [DORA_DEFAULT-1]
        self.xun = 0

        for i in range(4):
            tmp = (self.oya + i) % NUM_OF_SET_PER_QUAN #摸牌起始位置往下, tmp表示这人的position
            self.seats[tmp].newset_init()

            if i == 0:
                self.seats[tmp].hand.in_hand = self.yama[-4:]+self.yama[-20:-16]+self.yama[-36:-32]+[self.yama[-49]]
            else:
                for j in range(3):
                    self.seats[tmp].hand.in_hand += self.yama[-(i+j*4+1)*4:-(i+j*4)*4]
                self.seats[tmp].hand.in_hand += [self.yama[-49-i]]
            self.seats[tmp].hand.in_hand.sort()
            self.seats[tmp].fu, self.seats[tmp].yi, self.seats[tmp].fan = [0, 0], [0, 0], [0, 0]
            self.seats[tmp].dedian = 0

            #self.seats[tmp].hand.new_set_init(self.yama, tmp, self.oya)
        self.yama = self.yama[:-52]
        self.turn = self.oya #draw tiles from oya
        self.setTag = 0 #reset setTag
        self.on_hold_flag = False
        self.table_status = WAIT_FOR_SERVE

    def serve(self):
        #serve tiles for player at position self.turn
        self.seats[self.turn].lingshang = False
        #if len(self.yama) == MIN_TILES_IN_YAMA or self.xun >= MAX_XUN:
        if len(self.yama) == MIN_TILES_IN_YAMA: #要考虑ai摸牌时候流局，改成<=
            self.setTag = END_LIUJU
            # return 0
        else:
            tmp = self.yama.pop()
            # self.seats[self.turn].hand.new_tile.append(tmp)

            self.seats[self.turn].hand.new_tile = tmp
            # self.xun = int(self.xun + 1)
            if self.turn == self.oya:
                self.xun += 1

            self.seats[self.turn].lingshang = False
            if self.turn !=0: self.on_hold()
            self.table_status = WAIT_FOR_DROP
            # return tmp

    def gangserve(self):
        self.seats[self.turn].lingshang = True
        self.seats[self.turn].hand.new_tile = self.yama[0]
        self.yama = self.yama[1:]
        self.dora.append(self.dora[-1] + 2)
        self.ura.append(self.ura[-1] + 2)
        for i in range(len(self.dora)):
            self.dora[i] -= 1
            self.ura[i]  -= 1
        self.seats[self.turn].gangTag = False

    def jiesuan(self, _pai, turn):
        # TODO: dedian like 8000,12000 etc are readable.
        # print _pai
        # print self.user.hand.in_hand
        # print turn, self.user.position
        if turn == self.user.position:
            self.user.zimo = 1
        else:
            self.user.zimo = 0
        self.user.fu, self.user.yi, self.user.fan = self.user.rong(_pai, self.quan, self.oya)
        if self.user.fu == [0, 0]:
            self.user.dedian = 0
            return
        if len(self.yama) == MIN_TILES_IN_YAMA:
            if self.user.zimo == 1:
                if u'岭上开花' not in self.user.fan[0]:
                    self.user.yi[0] += 1
                    self.user.fan[0] += [u'海底捞月']
            else:
                self.user.yi[0] += 1
                self.user.fan[0] += [u'河底捞鱼']
        if self.user.yi != [0, 0]:
            if self.user.yi[1] != 0:
                if self.user.position == self.oya:
                    self.user.dedian = 48000 * self.user.yi[1]
                else:
                    self.user.dedian = 32000 * self.user.yi[1]
            else:
                tmp = self.user.hand.in_hand + [self.user.rongpai]
                for gang in self.user.agang:
                    tmp = tmp + gang
                for gang in self.user.mgang:
                    tmp = tmp + gang

                if self.xun - self.user.riichi == 1 and self.user.riichi > 0:
                    self.user.yi[0] += 1
                    self.user.fan[0] += [u'一發']
                numdora = 0
                for dora in self.dora:
                    numdora += tmp.count(Util.nextpai(self.yama[dora]))
                self.user.yi[0] += numdora
                if numdora != 0: self.user.fan[0] += ['Dora ' + str(numdora)]
                if self.user.riichi > 0:
                    numura = 0
                    for ura in self.ura:
                        numura += tmp.count(Util.nextpai(self.yama[ura]))
                    self.user.yi[0] += numura
                    if numura != 0: self.user.fan[0] += ['Ura ' + str(numura)]
                if self.user.fu[0] != 25:
                    self.user.fu[0] = int(math.ceil(self.user.fu[0] / 10.) * 10)
                self.user.dedian = 0
                jbd = self.user.fu[0] * 4 * pow(2, self.user.yi[0])
            #     if self.user.yi[0] == 0:
            #         self.user.dedian = -8000
            #     elif jbd < 2000:
            #         if self.user.position == self.oya:
            #             self.user.dedian = math.ceil(jbd * 6 / 100) * 100
            #         else:
            #             self.user.dedian = math.ceil(jbd * 4 / 100) * 100
            #     else:
            #         if self.user.yi[0] <= 5:
            #             self.user.dedian = 8000
            #         elif self.user.yi[0] <= 7:
            #             self.user.dedian = 12000
            #         elif self.user.yi[0] <= 10:
            #             self.user.dedian = 16000
            #         elif self.user.yi[0] <= 12:
            #             self.user.dedian = 24000
            #         elif self.user.yi[0] >= 13:
            #             self.user.dedian = 32000
            #         if self.user.position == self.oya: self.user.dedian = self.user.dedian * 1.5
            # # self.user.money += int(self.user.dedian) + self.lizhibang * 1000
            self.transfer_money(0, jbd)

    def transfer_money(self, rong_player, jibendian):
        if self.seats[rong_player].yi[1] !=0:
            jbd1 = 8000  * self.seats[rong_player].yi[1]
            jbd2 = jbd1 * 2
            jbd4 = jbd1 * 4
            jbd6 = jbd1 * 6
        elif jibendian < 2000:
            jbd1 = int(math.ceil(jibendian * 1 / 100.0)) * 100
            jbd2 = int(math.ceil(jibendian * 2 / 100.0)) * 100
            jbd4 = int(math.ceil(jibendian * 4 / 100.0)) * 100
            jbd6 = int(math.ceil(jibendian * 6 / 100.0)) * 100
        else:
            if self.seats[rong_player].yi[0] <=5:
                jbd1 = 2000
            elif self.seats[rong_player].yi[0]<=7:
                jbd1 = 3000
            elif self.seats[rong_player].yi[0]<=10:
                jbd1 = 4000
            elif self.seats[rong_player].yi[0]<=12:
                jbd1 = 6000
            elif self.seats[rong_player].yi[0]>=13:
                jbd1 = 8000
            jbd2 = jbd1 * 2
            jbd4 = jbd1 * 4
            jbd6 = jbd1 * 6
        # print self.seats[rong_player].zimo
        if self.seats[rong_player].zimo:
            if self.oya == rong_player:
                for player in self.seats:
                    if player.position != rong_player:
                        player.money -= jbd2
                    else:
                        player.dedian = jbd2 * 3
                        player.money += player.dedian
            else:
                for player in self.seats:
                    if player.position != rong_player:
                        if player.position == self.oya:
                            player.money -= jbd2
                        else:
                            player.money -= jbd1
                    else:
                        player.dedian = jbd2 + jbd1*2
                        player.money += player.dedian
        else:
            if rong_player == self.oya:
                self.seats[self.turn].money -= jbd6
                self.seats[rong_player].dedian = jbd6
                self.seats[rong_player].money += self.seats[rong_player].dedian
            else:
                self.seats[self.turn].money -= jbd4
                self.seats[rong_player].dedian = jbd4
                self.seats[rong_player].money += self.seats[rong_player].dedian

        self.seats[rong_player].money += 1000 * self.lizhibang
        self.lizhibang = 0
        # print self.turn
        # print rong_player
        # print self.seats[rong_player].dedian
        # print jibendian
        #TODO: not implementing multiple rongs at the same time.

    def setComplete(self):
        return self.setTag != 0

    def waitingResponse(self):
        return self.table_status == WAIT_FOR_RESPONSE

    def action_respond(self, button_pressed):
        #TODO: not implementing chi, gang
        if button_pressed == 'peng':
            self.menu_peng(self.new_drop_tile) #TODOXU
            self.table_status = WAIT_FOR_SERVE
        elif button_pressed == 'cancel':
            self.table_status = WAIT_FOR_SERVE
        elif button_pressed == 'rong':
            self.menu_rong(self.new_drop_tile, self.turn)
            #TODO: implement for jiesuan when not closed

    def menu_respond(self, button_pressed):
        if button_pressed == 'rong':
            if self.turn == 0:
                self.menu_rong(self.user.hand.new_tile)
            elif self.table_status == NO_RESPONSE:
                self.menu_rong(self.new_drop_tile, self.turn)
        elif self.table_status == NO_RESPONSE:
            self.next_step()
        elif button_pressed == 'riichi':
            self.menu_riichi()
        elif button_pressed == 'gang':
            self.menu_gang()
        elif button_pressed == 'analysis':
            self.menu_analysis()
        elif button_pressed == 'cheat':
            self.menu_cheat()

    def tile_respond(self, tile_pressed):
        if self.user.riichi == WAIT_FOR_RIICHI_PAI:
            # This is a status of waiting for riichi
            self.new_drop_tile = self.user.drop(tile_pressed)
            if self.new_drop_tile:
                self.user.riichi = self.xun
                self.tile_dropped_respond()
                # self.serve()
                # self.tile_ai_drop()
        elif self.user.gangTag == False:
            self.new_drop_tile = self.user.drop(tile_pressed)
            if self.new_drop_tile:
                self.tile_dropped_respond()
                # self.serve()
                # self.tile_ai_drop()
        else:
            gangtmp = self.user.gang(tile_pressed)
            if gangtmp:
                self.tile_gang_respond()
                self.gangserve()
                # self.tile_ai_drop()
            else:
                self.user.gangTag = False
        #print(self.yama)
        #print(self.seats[1].hand.new_tile)
        #print(self.seats[2].hand.new_tile)
        #print(self.seats[3].hand.new_tile)

    def tile_gang_respond(self):
        raise NotImplementedError

    def tile_dropped_respond(self):
        if Util.keyipeng(self.user.hand.in_hand, self.new_drop_tile) and self.user.riichi == 0 and self.turn != 0:
            self.table_status = WAIT_FOR_RESPONSE
        else:
            self.table_status = NO_RESPONSE
        if self.turn == 0:
            #TODO: Assume now AI cannot respond to tiles
            self.next_step()
            # self.next_step()
        # self.turn +=1
        # self.turn %=4
        # #TODO: Implement the respond of waiting for chi,peng,gang,rong from other players.
        # self.serve()

    # def tile_ai_drop(self):
        # if self.turn != self.user.position:
            # self.seats[self.turn].dapai1()
            # self.tile_dropped_respond()

    def menu_rong(self, _pai, turn=0):
        self.user.rongTag = True
        self.user.analysisTag = False
        self.setTag = END_RONG
        self.lastrongplayer = 0 # currently only allowing player rong.
        self.jiesuan(_pai, turn)

    def menu_riichi(self):
        if self.user.riichi == 0:
            self.user.riichi = WAIT_FOR_RIICHI_PAI
            self.user.money -= 1000
            self.lizhibang += 1

    def menu_gang(self):
        if len(self.yama) > MIN_TILES_IN_YAMA: self.user.gangTag = True

    def menu_analysis(self):
        self.user.analysisTag = not self.user.analysisTag

    def menu_clear(self):
        self.user.rongTag = False
        self.user.gangTag = False

    def menu_cheat(self):
        if self.turn !=0: return
        xiangtingshu, MINexp = self.user.hand.chaifen2(self.user.hand.in_hand)
        yxz = MINexp[len(MINexp)]
        random.shuffle(yxz)
        for pai in yxz:
            if pai in self.yama[14:]:
                self.yama[self.yama.index(pai)] = self.user.hand.new_tile
                self.user.hand.new_tile = pai
                return

    def menu_peng(self, _pai, turn=0): #TODOXU
        self.user.kaimen = True
        self.user.pengpai(_pai) # currently only allowing user peng.
        self.seats[self.turn].dropped.pop()
        self.turn = 0

    def tagclear(self):
        self.user.rongTag = False
        self.user.gangTag = False

    def on_hold(self):
        self.on_hold_flag = True

    def off_hold(self):
        self.on_hold_flag = False

    def next_step(self):
        if self.table_status == WAIT_FOR_SERVE:
            self.turn +=1
            self.turn %=4
            self.serve()
            self.table_status = WAIT_FOR_DROP
        elif self.table_status == WAIT_FOR_DROP:
            if self.turn != 0 :
                self.new_drop_tile = self.seats[self.turn].dapai1()
                self.tile_dropped_respond()
            else:
                # Wait for player decision. Implemented by using other methods.
                pass
        elif self.table_status == NO_RESPONSE:
            self.table_status = WAIT_FOR_SERVE
            self.next_step()


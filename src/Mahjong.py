# -*- coding: utf-8 -*-

import math
import random


class game():
    def __init__(self):
        self.pai = []
        self.create()
        self.user = player()
        self.quan = 0
        self.oya = -1
        self.xun = 0
        self.benchang = 0
        self.lizhibang = 0

    def create(self):
        for i in range(4):
            start = 30
            for j in range(start + 1, start + 10):
                if j % 10 != 0: self.pai.append(j)
            #for k in range(41, 48):
            #    self.pai.append(k)

    def newset(self):
        self.oya += 1
        self.quan, self.oya = self.quan + self.oya // 4, self.oya % 4
        self.yama = self.pai[:]
        random.shuffle(self.yama)
        self.dora = [5]
        self.ura = []
        self.xun = 0
        tmp = self.user.money
        self.user.__init__()
        self.user.money = tmp
        self.user.hand, self.yama = self.yama[-13:], self.yama[:-13]
        self.user.hand.sort()
        self.fu, self.yi, self.fan = [0, 0], [0, 0], [0, 0]
        self.dedian = 0

    def serve(self):
        if len(self.yama) == 14 or self.xun >= 30:
            return 0
        else:
            pai = self.yama.pop()
            self.xun = int(self.xun + 1)
            self.user.lingshang = 0
            return pai

    def nextpai(self, _pai):
        m, n = _pai // 10, _pai % 10
        if m == 4:
            if n == 4:
                return 41
            elif n == 7:
                return 45
            else:
                return _pai + 1
        else:
            return m * 10 + n % 9 + 1

    def gang(self, _pai, _gangpai):
        tmp = self.user.hand + [_pai]
        n = tmp.count(_gangpai)
        if n < 4:
            return False
        else:
            if len(self.yama) > 14:
                tmp.remove(_gangpai)
                tmp.remove(_gangpai)
                tmp.remove(_gangpai)
                tmp.remove(_gangpai)
                tmp.sort()
                self.user.hand = tmp
                self.user.agang += [[_gangpai] * 4]
                self.xun += 0.5
                return True
            else:
                return False

    def jiesuan(self, _pai):
        self.user.zimo = 1
        self.fu, self.yi, self.fan = self.user.rong(_pai, self.quan, self.oya)
        if len(self.yama) == 14:
            if self.user.zimo == 1:
                if u'岭上开花' not in self.fan[0]:
                    self.yi[0] += 1
                    self.fan[0] += [u'海底捞月']
            else:
                self.yi[0] += 1
                self.fan[0] += [u'河底捞鱼']
        if self.yi != [0, 0]:
            if self.yi[1] != 0:
                if self.user.position == self.oya:
                    self.dedian = 48000 * self.yi[1]
                else:
                    self.dedian = 32000 * self.yi[1]
            else:
                tmp = self.user.hand + [self.user.rongpai]
                if self.xun - self.user.riichi == 1 and self.user.riichi > 0:
                    self.yi[0] += 1
                    self.fan[0] += [u'一發']
                tmpk = 0
                numdora = 0
                for dora in self.dora:
                    numdora += tmp.count(self.nextpai(self.yama[dora]))
                    self.ura.append(dora - 1)
                    tmpk += 2
                self.yi[0] += numdora
                if numdora != 0: self.fan[0] += ['Dora ' + str(numdora)]
                if self.user.riichi > 0:
                    numura = 0
                    for ura in self.ura:
                        numura += tmp.count(self.nextpai(self.yama[ura]))
                    self.yi[0] += numura
                    if numura != 0: self.fan[0] += ['Ura ' + str(numura)]
                if self.fu[0] != 25:
                    self.fu[0] = int(math.ceil(self.fu[0] / 10.) * 10)
                self.dedian = 0
                self.jbd = self.fu[0] * 4 * pow(2, self.yi[0])
                if self.yi[0] == 0:
                    self.dedian = -8000
                elif self.jbd < 2000:
                    if self.user.position == self.oya:
                        self.dedian = math.ceil(self.jbd * 6 / 100) * 100
                    else:
                        self.dedian = math.ceil(self.jbd * 4 / 100) * 100
                else:
                    if self.yi[0] <= 5:
                        self.dedian = 8000
                    elif self.yi[0] <= 7:
                        self.dedian = 12000
                    elif self.yi[0] <= 10:
                        self.dedian = 16000
                    elif self.yi[0] <= 12:
                        self.dedian = 24000
                    elif self.yi[0] >= 13:
                        self.dedian = 32000
                    if self.user.position == self.oya: self.dedian = self.dedian * 1.5
            self.user.money += int(self.dedian) + self.lizhibang * 1000
            self.lizhibang = 0


class player():
    def __init__(self):
        self.hand = []
        self.drop = []
        self.isclose = True
        self.riichi = 0
        self.zimo = 0
        self.money = 100000
        self.position = 0
        self.chi = []
        self.peng = []
        self.mgang = []
        self.agang = []
        self.rongpai = 0
        self.fu = {}
        self.yi = {}
        self.exp = {}
        self.rongflag = 0
        self.lingshang = 0

    def keyigang(self, _pai):
        return True

    def calcfu(self, quan, oya):
        (exp, flag) = self.exp, self.rongflag
        if flag == False:
            self.fu = {1: 0}
        else:
            res = 20
            self.fu = {}.fromkeys(exp.keys(), 0)
            # mingke
            for kezi in self.peng:
                tmp = kezi[0]
                if self.isyao(tmp):
                    res += 4
                else:
                    res += 2
            # gang
            for a in self.agang:
                tmp = a[0]
                if self.isyao(tmp):
                    res += 32
                else:
                    res += 16
            for a in self.mgang:
                tmp = a[0]
                if self.isyao(tmp):
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
                            if self.isyao(zuhe[0]):
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
                                if self.isyao(zuhe[0]):
                                    self.fu[k] += 4
                                else:
                                    self.fu[k] += 2
                            else:
                                if self.isyao(zuhe[0]):
                                    self.fu[k] += 8
                                else:
                                    self.fu[k] += 4
                if self.fu[k] == 20 and self.isclose:
                    tag = 0
                    for zuhe in v:
                        if len(zuhe) == 3 and zuhe[0] != zuhe[1] and self.rongpai in zuhe:
                            if self.isliangmian(zuhe, self.rongpai):
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
                            if self.isliangmian(zuhe, self.rongpai):
                                continue
                            else:
                                self.fu[k] += 2
                                break
                    if self.zimo != 0:
                        self.fu[k] += 2
                    elif self.isclose:
                        self.fu[k] += 10

    def calcyi(self, quan, oya):
        exp, flag = self.exp, self.rongflag
        if flag == False:
            self.yi = {1: [[0], [0]]}
        else:
            self.yi = {}.fromkeys(exp.keys(), 0)
            for key in exp.keys():
                self.yi[key] = [[0], [0]]
            tmp = len(self.agang) + len(self.mgang)
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
                for tmp in self.agang + self.mgang:
                    kezi.append(tmp[:-1])
                for tmp in self.peng:
                    kezi.append(tmp)
                for tmp in self.chi:
                    shunzi.append(tmp)
                a, b = len(kezi), len(shunzi)
                kezi.sort()
                shunzi.sort()
                if [a, b] == [0, 4]:
                    if self.isclose:
                        if shunzi[1] == shunzi[0] and shunzi[3] == shunzi[2]:
                            self.yi[k][0][0] += 3
                            self.yi[k][0].append(u'两盃口')
                        if self.fu[k] == 20 and self.zimo > 0:
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'平和')
                        elif self.fu[k] == 30 and self.zimo == 0:
                            self.yi[k][0][0] += 1
                            self.yi[k][0].append(u'平和')
                if b >= 3:
                    if self.sanse(shunzi):  ###
                        if self.isclose:
                            self.yi[k][0][0] += 2
                        else:
                            self.yi[k][0][0] += 1
                        self.yi[k][0].append(u'三色同顺')
                    elif self.yiqi(shunzi):  ###
                        if self.isclose:
                            self.yi[k][0][0] += 2
                        else:
                            self.yi[k][0][0] += 1
                        self.yi[k][0].append(u'一气通贯')
                if b >= 2 and self.isclose and u'两盃口' not in self.yi[k][0]:
                    if self.yibeikou(shunzi):  ###
                        self.yi[k][0][0] += 1
                        self.yi[k][0].append(u'一盃口')
                if a == 4:
                    if self.dasixi(kezi):  ###
                        self.yi[k][1][0] += 2
                        self.yi[k][1].append(u'大四喜')
                    if self.isclose:
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
                    if tmp != 0 and self.isclose:
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
                    if self.isclose: self.yi[k][0][0] += 1
                    if self.lvyise(kezi, shunzi, quetou):
                        self.yi[k][1][0] += 1
                        self.yi[k][1].append(u'绿一色')
                if self.isclose and self.zimo > 0:
                    self.yi[k][0][0] += 1
                    self.yi[k][0].append(u'门清自摸')
                if self.riichi == 1:
                    self.yi[k][0][0] += 2
                    self.yi[k][0].append(u'两立直')
                elif self.riichi > 0:
                    self.yi[k][0][0] += 1
                    self.yi[k][0].append(u'立直')

    def findSame(self, _list, num):
        return _list.count(_list[0]) == num

    def isliangmian(self, mianzi, pai):
        if pai in mianzi:
            i = mianzi.index(pai)
            if i == 0 and pai % 10 < 7: return True
            if i == 2 and pai % 10 > 3: return True
            return False
        else:
            return False

    def isyao(self, _pai):
        m, n = _pai // 10, _pai % 10
        if m == 4:
            return True
        elif n == 1 or n == 9:
            return True
        else:
            return False

    def shunzi(self, _list):
        _sz = None
        _rs = None
        issz = False
        tmp = _list[0]
        (m, n) = tmp // 10, tmp % 10
        if m == 4 or n > 7:
            pass
        elif tmp + 1 in _list and tmp + 2 in _list:
            _rs = _list[:]
            _sz = [tmp, tmp + 1, tmp + 2]
            issz = True
            for value in _sz:
                _rs.remove(value)
        return (_sz, _rs, issz)

    def rong(self, _pai, quan, oya):
        self.rongpai = _pai
        _hand = self.hand + [_pai]
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
                    (exp, flag) = self.explain(_list)
                    if flag == False:
                        return (expres, flagres)
                    else:
                        flagres = True
                        hand = hand + exp[1]
            l = max(a, b, c, d)
            if l >= 8:
                _list = [wan, bing, tiao, zi][[a, b, c, d].index(l)]
                (exp, flag) = self.explain(_list)
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

    def explain(self, _list):
        exp = {}
        flag = False
        test = len(_list)
        if test % 3 == 1: return ({}, False)
        if test == 0:
            exp[1] = []
            return (exp, True)
        if _list[0] // 10 == 4:
            if test % 3 == 0:
                num = _list.count(_list[0])
                if num != 3:
                    return ({}, False)
                else:
                    (exp1, flag1) = self.explain(_list[3:])
                    if flag1 == False:
                        return ({}, False)
                    else:
                        exp1[1].append(_list[:3])
                        exp[1] = exp1[1]
                        return (exp, True)
            elif test % 3 == 2:
                num = _list.count(_list[0])
                if num != 2 and num != 3:
                    return ({}, False)
                else:
                    (exp1, flag1) = self.explain(_list[num:])
                    if flag1 == False:
                        return ({}, False)
                    else:
                        exp1[1].append(_list[:num])
                        exp[1] = exp1[1]
                        return (exp, True)
        else:
            if test % 3 == 0:
                (_sz, _rs, issz) = self.shunzi(_list)
                if issz:
                    (exp1, flag1) = self.explain(_rs)
                    if flag1 == False:
                        pass
                    else:
                        flag = True
                        for key, value in exp1.items():
                            value.append(_sz)
                            exp[key] = value
                if self.findSame(_list, 3):
                    (exp1, flag1) = self.explain(_list[3:])
                    if flag1 == False:
                        return ({}, False)
                    else:
                        flag = True
                        tmp = len(exp)
                        for key, value in exp1.items():
                            value.append(_list[:3])
                            exp[tmp + key] = value
                return (exp, flag)
            elif test % 3 == 2:
                add = _list[0] // 10
                ptou = 3 - (sum(_list) - 20 * add) % 3 + 10 * add
                for tou in [ptou, ptou + 3, ptou + 6]:
                    num = _list.count(tou)
                    if num >= 2:
                        i = _list.index(tou)
                        (exp1, flag1) = self.explain(_list[:i] + _list[i + 2:])
                        if flag1 == False:
                            continue
                        else:
                            flag = True
                            tmp = len(exp)
                            for key, value in exp1.items():
                                value.append(_list[i:i + 2])
                                exp[tmp + key] = value
                return (exp, flag)

    def xiangting(self, exp):
        m = 0
        d = 0
        q = 0
        yxz = []
        danzhangtmp = []
        duizitmp = []
        for value in exp:
            tmp = len(value)
            if tmp == 3:
                m += 1
            elif tmp == 2 and value[0] == value[1]:
                q += 1
                duizitmp.append(value)
            elif tmp == 2:
                d += 1
                yxz += self.youxiaozhang(value)
            else:
                danzhangtmp.append(value)
        sumup = m + d + q
        if m == 4:
            if q == 1:
                return (-1, [])
            restmp = []
            for key in danzhangtmp:
                restmp += key
            return (0, restmp)
        if sumup <= 3:
            for pai in danzhangtmp:
                yxz += self.youxiaozhang2(pai)
            for pai in duizitmp:
                yxz += [pai[0]]
        elif sumup == 4:
            if q == 0:
                for pai in danzhangtmp:
                    yxz += pai
            elif q == 1:
                for pai in danzhangtmp:
                    yxz += self.youxiaozhang2(pai)
        else:
            if q == 0:
                for pai in danzhangtmp:
                    yxz += pai
            elif q == 1:
                pass
            else:
                for pai in duizitmp:
                    yxz += [pai[0]]
        if q > 1:
            d = d + q - 1
            q = 1
        if d > 4 - m:
            d = 4 - m
        yxz = sorted(list(set(yxz)))
        return (8 - 2 * m - d - q, yxz)

    def countyxz(self, _list, allyxz):
        result = 0
        for pai in allyxz:
            result += 4 - _list.count(pai)
            return result

    def chaifen2(self, _list):
        exp = self.chaifen1(_list)
        tmp0 = 8
        MINexp = {}
        for key, value in exp.items():
            tmp1, yxz = self.xiangting(value)
            if tmp1 < tmp0:
                MINexp = {1: (value, yxz)}
                tmp0 = tmp1
            elif tmp1 == tmp0:
                MINexp[len(MINexp) + 1] = (value, yxz)
        allyxz = []
        for key, value in MINexp.items():
            MINexp[key] = sorted(value[0], key=lambda x: x[0])
            allyxz += value[1]
        allyxz = list(set(allyxz))
        MINexp[len(MINexp) + 1] = sorted(allyxz)
        return (tmp0, MINexp)

    def chaifen1(self, _list):
        exp = {}

        if len(_list) == 0:
            return exp

        count = _list.count(_list[0])
        _sz, _rs, issz = self.shunzi(_list)

        if issz:
            if _rs == []:
                exp[len(exp) + 1] = [_sz]
            exp1 = self.chaifen1(_rs)
            for key, value in exp1.items():
                exp1[key].append(_sz)
                exp[len(exp) + 1] = exp1[key]
        m, n = _list[0] // 10, _list[0] % 10
        if m == 4 or n == 9:
            pass
        else:
            tmp2 = _list[0] + 1;
            tmp3 = _list[0] + 2;
            if tmp2 in _list:
                _rs = _list[:]
                _rs.remove(_list[0])
                _rs.remove(tmp2)
                _dazi = [_list[0], tmp2]
                if _rs == []:
                    exp[len(exp) + 1] = [_dazi]
                exp1 = self.chaifen1(_rs)
                for key, value in exp1.items():
                    exp1[key].append(_dazi)
                    exp[len(exp) + 1] = exp1[key]
            if tmp3 in _list:
                _rs = _list[:]
                _rs.remove(_list[0])
                _rs.remove(tmp3)
                _dazi = [_list[0], tmp3]
                if _rs == []:
                    exp[len(exp) + 1] = [_dazi]
                exp1 = self.chaifen1(_rs)
                for key, value in exp1.items():
                    exp1[key].append(_dazi)
                    exp[len(exp) + 1] = exp1[key]
        if count >= 3:
            _kezi, _rs = _list[:3], _list[3:]
            if _rs == []:
                exp[len(exp) + 1] = [_kezi]
            exp1 = self.chaifen1(_rs)
            for key, value in exp1.items():
                exp1[key].append(_kezi)
                exp[len(exp) + 1] = exp1[key]
        if count >= 2:
            _duizi, _rs = _list[:2], _list[2:]
            if _rs == []:
                exp[len(exp) + 1] = [_duizi]
            exp1 = self.chaifen1(_rs)
            for key, value in exp1.items():
                exp1[key].append(_duizi)
                exp[len(exp) + 1] = exp1[key]
        _danzhang, _rs = _list[0], _list[1:]
        if _rs == []:
            exp[len(exp) + 1] = [[_danzhang]]
        exp1 = self.chaifen1(_rs)
        for key, value in exp1.items():
            exp1[key].append([_danzhang])
            exp[len(exp) + 1] = exp1[key]
        return exp

    def youxiaozhang(self, dazi):
        n = dazi[0] % 10
        n1 = dazi[1] % 10
        if n == n1:
            return [dazi[0]]
        if n == n1 - 2:
            return [dazi[0] + 1]
        if n == n1 - 1:
            if n == 1:
                return [dazi[1] + 1]
            elif n1 == 9:
                return [dazi[0] - 1]
            else:
                return [dazi[0] - 1, dazi[1] + 1]

    def youxiaozhang2(self, danpai):
        m, n = danpai[0] // 10, danpai[0] % 10
        if m == 4:
            return danpai
        else:
            if n == 1:
                return [danpai[0] + i for i in range(3)]
            elif n == 2:
                return [danpai[0] + i - 1 for i in range(4)]
            elif n == 8:
                return [danpai[0] + i - 2 for i in range(4)]
            elif n == 9:
                return [danpai[0] + i - 2 for i in range(3)]
            else:
                return [danpai[0] + i - 2 for i in range(5)]

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


def readpai(str="123456789m112p3s"):
    list = []
    tmplist = []
    for pai in str:
        if pai == 'm':
            tmplist = [key + 10 for key in tmplist]
            list += tmplist
            tmplist = []
        elif pai == 'p':
            tmplist = [key + 20 for key in tmplist]
            list += tmplist
            tmplist = []
        elif pai == 's':
            tmplist = [key + 30 for key in tmplist]
            list += tmplist
            tmplist = []
        elif pai == 'z':
            tmplist = [key + 40 for key in tmplist]
            list += tmplist
            tmplist = []
        else:
            tmplist += [int(pai)]

    if len(list) >= 14:
        list = list[:14]
    list.sort()
    return list


def main():
    _game = game()
    while 1:
        _l = readpai(raw_input('Please enter your pai: '))
        xiangtingshu, MINexp = _game.user.chaifen2(_l)
        print xiangtingshu
        for key, value in MINexp.items():
            print value
        '''
    _game.user.isclose = True
    _game.user.agang = []
    _game.user.exp, _game.user.rongflag = _game.user.rong2(_l)
    _game.user.rongpai = 16
    _l.remove(_game.user.rongpai)
    _game.user.hand = _l
    _game.user.zimo = 1
    print _game.user.exp
    _game.user.calcfu(0,0)
    print _game.user.fu
    _game.user.calcyi(0,0)
    print _game.user.yi
    '''


main()
'''
_game = game()
_l = [42,42,42,43,43,43,44,44,44,45,45]
_game.user.isclose = True
_game.user.agang = [[41]*4]
_game.user.exp, _game.user.rongflag = _game.user.rong2(_l)
print _game.user.exp
_game.user.rongpai = 45
_l.remove(_game.user.rongpai)
_game.user.hand = _l
_game.user.zimo = 1
_game.user.calcfu(0,0)
print _game.user.fu
_game.user.calcyi(0,0)
print _game.user.yi
'''

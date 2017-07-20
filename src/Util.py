from constants import *


class Util:
    @classmethod
    def findSame(cls, _list, num):
        return _list.count(_list[0]) == num

    @classmethod
    def is_liangmian(cls, mianzi, pai):
        if pai in mianzi:
            i = mianzi.index(pai)
            if i == 0 and pai % 10 < 7: return True
            if i == 2 and pai % 10 > 3: return True
            return False
        else:
            return False

    @classmethod
    def isyao(cls, _pai):
        m, n = _pai // 10, _pai % 10
        if m == 4 or n == 1 or n == 9:
            return True
        else:
            return False

    @classmethod
    def shunzi(cls, _list):
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
        return _sz, _rs, issz

    @classmethod
    def explain(cls, _list):
        """
        Split the _list (as a representative of tiles of one kind) into Shunzi/Kezi/Duizi
        :param _list:
        :return:
        Split as combination of Mianzi and at most one Duizi. Return a flag showing whether we can do that.
        """
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
                    (exp1, flag1) = cls.explain(_list[3:])
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
                    (exp1, flag1) = cls.explain(_list[num:])
                    if flag1 == False:
                        return ({}, False)
                    else:
                        exp1[1].append(_list[:num])
                        exp[1] = exp1[1]
                        return (exp, True)
        else:
            if test % 3 == 0:
                (_sz, _rs, issz) = cls.shunzi(_list)
                if issz:
                    (exp1, flag1) = cls.explain(_rs)
                    if flag1 == False:
                        pass
                    else:
                        flag = True
                        for key, value in exp1.items():
                            value.append(_sz)
                            exp[key] = value
                if cls.findSame(_list, 3):
                    (exp1, flag1) = cls.explain(_list[3:])
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
                        (exp1, flag1) = cls.explain(_list[:i] + _list[i + 2:])
                        if flag1 == False:
                            continue
                        else:
                            flag = True
                            tmp = len(exp)
                            for key, value in exp1.items():
                                value.append(_list[i:i + 2])
                                exp[tmp + key] = value
                return (exp, flag)

    @classmethod
    def chaifen1(cls, _list):
        """
        Completely split the tiles in hand into Mianzi, Dazi, and singular tiles. Utility function to get best split.
        :param _list:
        :return:
        """
        exp = {}
        if len(_list) == 0:
            return exp
        count = _list.count(_list[0])
        _sz, _rs, issz = cls.shunzi(_list)
        if issz:
            if _rs == []:
                exp[len(exp) + 1] = [_sz]
            exp1 = cls.chaifen1(_rs)
            for key, value in exp1.items():
                exp1[key].append(_sz)
                exp[len(exp) + 1] = exp1[key]
        m, n = _list[0] // 10, _list[0] % 10
        if m == 4 or n == 9:
            pass
        else:
            tmp2 = _list[0] + 1
            tmp3 = _list[0] + 2
            if tmp2 in _list:
                _rs = _list[:]
                _rs.remove(_list[0])
                _rs.remove(tmp2)
                _dazi = [_list[0], tmp2]
                if _rs == []:
                    exp[len(exp) + 1] = [_dazi]
                exp1 = cls.chaifen1(_rs)
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
                exp1 = cls.chaifen1(_rs)
                for key, value in exp1.items():
                    exp1[key].append(_dazi)
                    exp[len(exp) + 1] = exp1[key]
        if count >= 3:
            _kezi, _rs = _list[:3], _list[3:]
            if _rs == []:
                exp[len(exp) + 1] = [_kezi]
            exp1 = cls.chaifen1(_rs)
            for key, value in exp1.items():
                exp1[key].append(_kezi)
                exp[len(exp) + 1] = exp1[key]
        if count >= 2:
            _duizi, _rs = _list[:2], _list[2:]
            if _rs == []:
                exp[len(exp) + 1] = [_duizi]
            exp1 = cls.chaifen1(_rs)
            for key, value in exp1.items():
                exp1[key].append(_duizi)
                exp[len(exp) + 1] = exp1[key]
        _danzhang, _rs = _list[0], _list[1:]
        if _rs == []:
            exp[len(exp) + 1] = [[_danzhang]]
        exp1 = cls.chaifen1(_rs)
        for key, value in exp1.items():
            exp1[key].append([_danzhang])
            exp[len(exp) + 1] = exp1[key]
        return exp

    @classmethod
    def youxiaozhang(cls, dazi):
        """
        Get useful tiles based on the pairs given
        :param dazi:
        :return:
        """
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

    @classmethod
    def youxiaozhang2(cls, danpai):
        """
        Get useful tiles around the singular tile.
        :param danpai:
        :return:
        """
        m, n = danpai[0] // 10, danpai[0] % 10
        if m == 4:
            return danpai
        else:
            return [danpai[0] + i - 2 for i in range(5) if
                    (danpai[0] + i - 3) // 10 == danpai[0] // 10 and (danpai[0] + i - 2) // 10 == danpai[0] // 10]

    @classmethod
    def xiangting(cls, exp, number_of_fulu):
        """
        Given the Split the of hand and the number of fulu, calculate number of xiangting and return useful tiles
        :param exp:
        :param number_of_fulu:
        :return:
        """
        m = number_of_fulu
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
                yxz += cls.youxiaozhang(value)
            else:
                danzhangtmp.append(value)
        sumup = m + d + q
        if m == 4:
            if q == 1:
                return -1, []
            restmp = []
            for key in danzhangtmp:
                restmp += key
            return 0, restmp
        if sumup <= 3:
            for pai in danzhangtmp:
                yxz += cls.youxiaozhang2(pai)
            for pai in duizitmp:
                yxz += [pai[0]]
        elif sumup == 4:
            if q == 0:
                for pai in danzhangtmp:
                    yxz += pai
            elif q == 1:
                for pai in danzhangtmp:
                    yxz += cls.youxiaozhang2(pai)
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
        return 8 - 2 * m - d - q, yxz

    @classmethod
    def countyxz(cls, _list, allyxz):
        """
        Count the number of useful tiles
        :param _list:
        :param allyxz: All useful tiles
        :return:
        """
        result = 0
        for pai in allyxz:
            result += 4 - _list.count(pai)
            return result

    @classmethod
    def chaifen2(cls, _list, number_of_fulu):
        """
        Split the tiles in hand optimally in the sense of smallest number of tiles needed to tenpai.
        :param _list:
        :param number_of_fulu: Number of Fulus
        :return:
        """
        exp = cls.chaifen1(_list)
        tmp0 = 8
        MINexp = {}
        for key, value in exp.items():
            tmp1, yxz = cls.xiangting(value, number_of_fulu)
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

        for item in allyxz:
            if _list.count(item) == 4:
                allyxz.remove(item)

        MINexp[len(MINexp) + 1] = sorted(allyxz)
        return (tmp0, MINexp)

    @classmethod
    def str2list(cls, str34):
        """
         This method change a string like '123456789m123s11z' into list.
        """
        list14 = []
        tmplist = []
        for pai in str:
            if pai == 'm':
                tmplist = [key + 10 for key in tmplist]
                list14 += tmplist
                tmplist = []
            elif pai == 'p':
                tmplist = [key + 20 for key in tmplist]
                list14 += tmplist
                tmplist = []
            elif pai == 's':
                tmplist = [key + 30 for key in tmplist]
                list14 += tmplist
                tmplist = []
            elif pai == 'z':
                tmplist = [key + 40 for key in tmplist]
                list14 += tmplist
                tmplist = []
            else:
                tmplist += [int(pai)]

        if len(list14) >=14:
            list14 = list14[:14]
        return list14

    @classmethod
    def list2str(cls, list14):
        """
         This method change a list of pai into string like '123456789m123s11z'.
        """
        str34 = ''
        tmpstr = ''

        #TODO: Now assume input list is not blank.

        pai = list14[0]
        m_old, n = pai // 10, pai % 10
        tmpstr += format(n)
        for pai in list14[1:]:
            m, n = pai // 10, pai % 10
            if m != m_old:
                str34 += tmpstr
                tmpstr = ''
                if   m_old == 1: str34 += 'm'
                elif m_old == 2: str34 += 'p'
                elif m_old == 3: str34 += 's'
                elif m_old == 4: str34 += 'z'
                m_old = m
            tmpstr += format(n)
        str34 += tmpstr
        tmpstr = ''
        if   m == 1: str34 += 'm'
        elif m == 2: str34 += 'p'
        elif m == 3: str34 += 's'
        elif m == 4: str34 += 'z'
        return str34

    @classmethod
    def nextpai(cls, _pai):
        # TODO:  Lots of constants here.
        #       Currently I guess these are already readable.

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



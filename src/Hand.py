from constants import *
from Util import Util


class Hand:
    def __init__(self):
        '''
        fulu1, ..., fulu4: name ('Chi', 'Peng', 'Ming_Gang'); tile, first tile in the fulu: ([11]); From: (0, 1, 2, 3),
        0 for your self and 1, 2, 3 represents the player sitting on the right, opposite and left respectively
        '''
        self.in_hand = []
        self.new_tile = []
        self.fulu = []
        self.exp = {}

    '''
    def new_set_init(self, yama, position, oya_position):
        if position == oya_position:
            self.in_hand = yama[-4:] + yama[-20:-16] + yama[-36:-32] + [yama[-49]]
        else:
            position_to_oya = (position - oya_position) % NUM_OF_SET_PER_QUAN
            pais_to_pick = [yama[-(position_to_oya + j * 4 + 1) * 4:-(position_to_oya + j * 4) * 4] for j in range(3)]
            self.in_hand = [j for i in pais_to_pick for j in i]
            self.in_hand.append(yama[-49 - position_to_oya])


        self.in_hand.sort()
        self.new_tile = []
        self.fulu1 = None
        self.fulu2 = None
        self.fulu3 = None
        self.fulu4 = None
        self.fulu  = []
    '''
    def re_organize_expression(self):
        expressions = {}
        for k, v in self.exp.items():
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

            for tmp in self.fulu:
                if tmp.name == 'Chi':
                    shunzi.append(tmp)
                elif tmp.name == 'Peng':
                    kezi.append(tmp)
                else:
                    kezi.append(tmp[:-1])
            expression = {}
            kezi.sort()
            shunzi.sort()
            expression['kezi'] = kezi
            expression['quetou'] = quetou
            expression['shunzi'] = shunzi
            expressions[k] = expression

        return expressions

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
                yxz += Util.youxiaozhang(value)
            else:
                danzhangtmp.append(value)
        m += len(self.fulu)
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
                yxz += Util.youxiaozhang2(pai)
            for pai in duizitmp:
                yxz += [pai[0]]
        elif sumup == 4:
            if q == 0:
                for pai in danzhangtmp:
                    yxz += pai
            elif q == 1:
                for pai in danzhangtmp:
                    yxz += Util.youxiaozhang2(pai)
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

        for item in allyxz:
            if _list.count(item) == 4:
                allyxz.remove(item)

        MINexp[len(MINexp) + 1] = sorted(allyxz)
        return (tmp0, MINexp)

    def chaifen1(self, _list):
        exp = {}

        if len(_list) == 0:
            return exp

        count = _list.count(_list[0])
        _sz, _rs, issz = Util.shunzi(_list)

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

    def gen_fulu(self, name, tiles, tile_from_position=None, tile_from_other_index=None):
        return self.fulu.append(Fulu(name, tiles, TILE_SIZE))

class Fulu(object):
    '''
    This class is a part of Hand, recording instances of fulu.
    '''
    def __init__(self, name, tiles, tile_from_position=None, tile_from_other_index=None):
        self.name = name
        self.tiles = tiles
        self.tile_from_position = tile_from_position
        self.tile_from_other_index = tile_from_other_index

    def get_tiles(self):
        return self.tiles

    def get_tile_from_others(self):
        if self.tile_from_other_index != None:
            return self.tiles[sefl.tile_from_other_index]
        else:
            return None

    def get_tile_from_whom(self):
        if self.tile_from_other_index != None:
            return self.tile_from_position
        else:
            return None

    def chi_2_jiagang(self):
        self.name = 'Jia_Gang'
        self.tiles.append(self.tiles[0])
        if self.tile_from_other_index == 2:
            self.tile_from_other_index = 3

    def gen_image(self, tiles_figure):
        tile_size_x, tile_size_y = tiles_figure[1][1].get_size()
        if self.name == 'Peng':
            image = pygame.Surface((tile_size_x * 3, tile_size_y))
            for ind in range(3):
                pai = self.tiles[ind]
                m, n = pai // 10, pai % 10
                image.blit(tiles_figure[m][n], (tile_size_x * ind, 0))


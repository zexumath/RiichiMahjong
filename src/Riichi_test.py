# -*- coding: utf-8 -*-
# !/usr/bin/env python
import pygame
import Mahjong
from pygame.locals import *
from sys import exit

'''----------------------------------'''


class Button(object):
    """这个类是一个按钮"""

    def __init__(self, image_filename, position):

        self.position = position
        self.canpress = True
        if type(image_filename) == type(''):
            self.image = pygame.image.load(image_filename)
        else:
            self.image = image_filename

    def render(self, surface):
        x, y = self.position
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2
        surface.blit(self.image, (x, y))

    def is_over(self, point):
        # 如果point在自身范围内，返回True
        point_x, point_y = point
        x, y = self.position
        w, h = self.image.get_size()
        x -= w / 2
        y -= h / 2

        in_x = point_x >= x and point_x < x + w
        in_y = point_y >= y and point_y < y + h
        return in_x and in_y


def genHand(screen, _hand, _pai):
    for p, i in zip(_hand, range(len(_hand))):
        m, n = p // 10, p % 10
        x, y = left + i * tilesize[0], up
        screen.blit(tiles[m][n], (x, y))
    if _pai != 0: screen.blit(tiles[_pai // 10][_pai % 10], (x + 8 + tilesize[0], y))


def genDrop(screen, _drop):
    _x, _y = 80, 180
    for index in range(len(_drop) - 1, -1, -1):
        m, n = index // 6, index % 6
        screen.blit(tiles[_drop[index] // 10][_drop[index] % 10], (_x + tilesize[0] * n, _y + (tilesize[1] - 9) * m))


def genDora(screen, _g):
    font = pygame.font.Font('../res/simsun.ttc', 24)
    dorahint = font.render(u'Dora指示牌', True, (0, 0, 0))
    screen.blit(dorahint, (80, 50))
    w = dorahint.get_width()
    dx = tiles[1][0].get_width()
    # dy = tiles[1][0].get_height()
    _x, _y = 80 + w, 50 + tilesize[1] - 9
    for pai in _g.ura:
        screen.blit(tiles[_g.yama[pai] // 10][_g.yama[pai] % 10], (_x, _y))
        _x += dx
    _x, _y = 80 + w, 50
    for pai in _g.dora:
        screen.blit(tiles[_g.yama[pai] // 10][_g.yama[pai] % 10], (_x, _y))
        _x += dx


def genJiesuan(screen, _g, TAG):
    if TAG == True:
        _x, _y = 500, 50
        font = pygame.font.Font('../res/simsun.ttc', 24)
        index = 1
        if _g.yi[1] == 0:
            index = 0
            ptstr = str(_g.fu[0]) + u'符' + str(_g.yi[0]) + u'番' + str(int(_g.dedian)) + u'点'
        elif _g.yi[1] == 1:
            ptstr = u'役满' + str(int(_g.dedian)) + u'点'
        else:
            ptstr = str(_g.yi[1]) + u'倍役满' + str(int(_g.dedian)) + u'点'
        fufandian = font.render(ptstr, True, (0, 0, 0))
        h = fufandian.get_height()
        for s in _g.fan[index]:
            screen.blit(font.render(s, True, (0, 0, 0)), (_x, _y))
            _y += h
        screen.blit(fufandian, (_x, _y))
    elif TAG == 2:
        font = pygame.font.Font('../res/simsun.ttc', 24)
        screen.blit(font.render(u'流局', True, (0, 0, 0)), (360, 50))


def genInfo(screen, _g):
    font = pygame.font.Font('../res/simsun.ttc', 24)
    ck = ''
    tmp = _g.quan % 4
    if tmp == 0:
        ck += u'東'
    elif tmp == 1:
        ck += u'南'
    elif tmp == 2:
        ck += u'西'
    else:
        ck += u'北'
    ck += str(_g.oya + 1) + u'局0本场 玩家点数' + str(_g.user.money)
    screen.blit(font.render(ck, True, (0, 0, 0)), (80, 20))


def genCPG(screen, _user):
    right = 800 - tilesize[0]
    for g in _user.agang:
        screen.blit(tiles[4][0], (right, up + 20))
        right -= tilesize[0]
        screen.blit(tiles[g[0] // 10][g[0] % 10], (right, up + 20))
        right -= tilesize[0]
        screen.blit(tiles[g[0] // 10][g[0] % 10], (right, up + 20))
        right -= tilesize[0]
        screen.blit(tiles[4][0], (right, up + 20))
        right -= tilesize[0]


# 生成tiles图片
tiles = {}
tilesize = (41, 64)
tiles[1], tiles[2], tiles[3], tiles[4] = [], [], [], []
path = '../res/tiles/'
for lei in range(1, 5):
    if lei != 4:
        i = 10
    else:
        i = 8
    for x in range(i):
        tmp = pygame.image.load(path + str(lei) + str(x) + '.png')
        tiles[lei].append(pygame.transform.scale(tmp.subsurface((23, 0), (82, 128)), tilesize))
left = 50
up = 500


def run():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    font = pygame.font.Font('../res/simsun.ttc', 64)
    _x, _y, _h = 33, 33, 63
    menu = {}
    menu['rong'] = Button(font.render(u'和', True, (0, 0, 0)), (_x, _y))
    menu['riichi'] = Button(font.render(u'立', True, (0, 0, 0)), (_x, _y + _h))
    menu['gang'] = Button(font.render(u'杠', True, (0, 0, 0)), (_x, _y + _h * 2))

    _g = Mahjong.game()
    _g.newset()
    _pai = _g.serve()

    TAG = False
    GANGTAG = 0
    while True:
        button_pressed = None
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                for button_name, button in menu.items():
                    if button.is_over(event.pos):
                        button_pressed = button_name
                        break
                if TAG == True or TAG == 2:
                    _g.newset()
                    _pai = _g.serve()
                    TAG = False
                    GANGTAG = 0
                elif TAG == False:
                    if button_pressed == 'rong':
                        TAG = True
                        _g.jiesuan(_pai)
                        button_pressed = None
                    elif button_pressed == 'riichi' and _g.user.riichi == 0:
                        _g.user.riichi = -1
                        _g.user.money -= 1000
                        _g.lizhibang += 1
                        button_pressed = None
                    elif button_pressed == 'gang':
                        GANGTAG = 1
                        button_pressed = None
                    # 以下讨论出牌问题
                    x, y = event.pos
                    x -= left
                    y -= up
                    if 0 < y and y < tilesize[1]:
                        if 0 < x and x < tilesize[0] * len(_g.user.hand):
                            if _g.user.riichi > 0:
                                pass
                            elif _g.user.riichi == -1:
                                _g.user.riichi = _g.xun
                                i = x // tilesize[0]
                                _g.user.drop.append(_g.user.hand[i])
                                _g.user.hand[i] = _pai
                                _g.user.hand.sort()
                                _pai = _g.serve()
                            elif GANGTAG == 1:
                                i = x // tilesize[0]
                                tmp = _g.gang(_pai, _g.user.hand[i])
                                if tmp:
                                    _pai, _g.yama = _g.yama[0], _g.yama[1:]
                                    for i in range(len(_g.dora)): _g.dora[i] -= 1
                                    _g.dora += [_g.dora[-1] + 2]
                                GANGTAG = 0
                            else:
                                i = x // tilesize[0]
                                _g.user.drop.append(_g.user.hand[i])
                                _g.user.hand[i] = _pai
                                _g.user.hand.sort()
                                _pai = _g.serve()
                        elif (x - 8) // tilesize[0] - len(_g.user.hand) == 0:
                            if _g.user.riichi == -1:
                                _g.user.riichi = _g.xun
                                _g.user.drop.append(_pai)
                                _pai = _g.serve()
                            elif GANGTAG == 1:
                                if _g.user.riichi > 0 and _g.user.keyigang(_pai):
                                    _g.gang(_pai, _pai)
                                    _pai, _g.yama = _g.yama[0], _g.yama[1:]
                                    for i in range(len(_g.dora)): _g.dora[i] -= 1
                                    _g.dora += [_g.dora[-1] + 2]
                                    GANGTAG = 0
                                else:
                                    tmp = _g.gang(_pai, _pai)
                                    if tmp:
                                        _pai, _g.yama = _g.yama[0], _g.yama[1:]
                                        for i in range(len(_g.dora)): _g.dora[i] -= 1
                                        _g.dora += [_g.dora[-1] + 2]
                                    GANGTAG = 0
                            else:
                                _g.user.drop.append(_pai)
                                _pai = _g.serve()
                        if _pai == 0: TAG = 2

            screen.fill((255, 255, 255))
            genDora(screen, _g)
            genHand(screen, _g.user.hand, _pai)
            genCPG(screen, _g.user)
            genDrop(screen, _g.user.drop)
            for button in menu.values():
                button.render(screen)
            genInfo(screen, _g)
            genJiesuan(screen, _g, TAG)
            pygame.display.set_caption('Mahjong')
            pygame.display.update()


if __name__ == "__main__":
    run()

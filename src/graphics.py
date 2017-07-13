# -*- coding: utf-8 -*-
# !/usr/bin/env python
import pygame
import mahjong
from pygame.locals import *
from sys import exit

WHITE = ( 255, 255, 255 )
'''----------------------------------'''


class Botton(object):
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


class Screen(object):
    """
    This class is totally for graphics. Main usage would be Screen.show().
    """
    windowWidth = 800
    windowHeight = 600
    windowSize = (windowWidth,windowHeight)

    def __init__(self, _game):
        self._display_surf = pygame.display.set_mode( self.windowSize, 0, 32 )
        self._game = _game
        self.font = pygame.font.Font('../res/simsun.ttc', 24)
        self.initMenu()
        self.initTiles()

    def show(self):
        self._display_surf.fill(WHITE)

        self.genStat()
        self.genMenu()
        # self.genPaishan()
        self.genPlayer()
        self.genAnalysis(not self._game.user.analysisTag)
        pygame.display.update()

    def initMenu(self):
        font = pygame.font.Font('../res/simsun.ttc', 32)

        _x,_y,_h = 17,17,31
        self.menu = {}
        self.menu['rong']        = Botton(font.render(u'和', True, (0, 0, 0)), (_x, _y))
        self.menu['riichi']      = Botton(font.render(u'立', True, (0, 0, 0)), (_x, _y + _h))
        self.menu['gang']        = Botton(font.render(u'杠', True, (0, 0, 0)), (_x, _y + _h * 2))
        self.menu['analysis']    = Botton(font.render(u'理', True, (0, 0, 0)), (_x, _y + _h * 3))

    def initTiles(self):
        self.tiles = {}
        self.tilesize = (41, 64)
        self.tiles[1], self.tiles[2], self.tiles[3], self.tiles[4] = [], [], [], []
        path = '../res/tiles/'
        for lei in range(1, 5):
            if lei != 4:
                i = 10
            else:
                i = 8
            for x in range(i):
                tmp = pygame.image.load(path + str(lei) + str(x) + '.png')
                self.tiles[lei].append(pygame.transform.scale(tmp.subsurface((23, 0), (82, 128)), self.tilesize))

    def genMenu(self):
        for button in self.menu.values():
            button.render(self._display_surf)

    def buttonPressed(self, event):
        for button_name, button in self.menu.items():
            if button.is_over(event.pos):
                button_pressed = button_name
                break
        return button_pressed

    def genStat(self):
        MIDDLE_OF_SCREEN = ( 0.5 * self.windowWidth, 0.5 * self.windowHeight )
        changkuang = ''
        tmp = self._game.quan % 4
        if tmp == 0:
            changkuang += u'東'
        elif tmp == 1:
            changkuang += u'南'
        elif tmp == 2:
            changkuang += u'西'
        else:
            changkuang += u'北'
        changkuang += str(self._game.oya + 1) + u'局0本场'
        dianshu = u'玩家点数' + str(self._game.user.money)
        ck = self.font.render(changkuang, True, (0, 0, 0))
        ds = self.font.render(dianshu   , True, (0, 0, 0))
        h_ck = ck.get_height()
        self._display_surf.blit(ck, MIDDLE_OF_SCREEN )
        self._display_surf.blit(ds, (0.5 * self.windowWidth, 0.5 * self.windowHeight + h_ck) )

    def genPlayer(self):
        _hand = self._game.user.hand
        _pai  = self._game.user.mopai
        left = 50
        up = 500
        for p, i in zip(_hand, range(len(_hand))):
            m, n = p // 10, p % 10
            x, y = left + i * self.tilesize[0], up
            self._display_surf.blit(self.tiles[m][n], (x, y))

        self._display_surf.blit(self.tiles[_pai // 10][_pai % 10], (x + 8 + self.tilesize[0], y))

        # show angang
        # TODO: change to show chi peng gang
        right = self.windowWidth - self.tilesize[0]
        for g in self._game.user.agang:
            self._display_surf.blit(self.tiles[4][0], (right, up + 20))
            right -= self.tilesize[0]
            self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, up + 20))
            right -= self.tilesize[0]
            self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, up + 20))
            right -= self.tilesize[0]
            self._display_surf.blit(self.tiles[4][0], (right, up + 20))
            right -= self.tilesize[0]

        # show drops
        # TODO: move constants to top of file
        DROP_POSx, DROP_POSy = 80, 180

        for index in range(len(self._game.user.drop) - 1, -1, -1):
            m, n = index // 6, index % 6
            tile_tmp = self._game.user.drop[index]
            self._display_surf.blit( self.tiles[tile_tmp // 10][tile_tmp % 10], \
                                    (DROP_POSx + self.tilesize[0] * n, \
                                     DROP_POSy + (self.tilesize[1] -9) * m) )

    def genAnalysis(self, AnalysisTag):
        if AnalysisTag == True:
            ANALYSISx, ANALYSISy = 500, 50
            font = self.font
            xiangtingshu, MINexp = self._game.user.chaifen2(self._game.user.hand)
            yxz = MINexp[len(MINexp)]
            ptstr = str(xiangtingshu) + u'向听'
            analysis = font.render(ptstr, True, (0, 0, 0))
            h = analysis.get_height()
            self._display_surf.blit(analysis, (ANALYSISx, ANALYSISy))
            ANALYSISy += h
            for index in range(len(yxz) -1, -1, -1):
                m, n = index //6, index % 6
                self._display_surf.blit( self.tiles[yxz[index] // 10][yxz[index] % 10], \
                                        (ANALYSISx + self.tilesize[0] * n, \
                                         ANALYSISy + (self.tilesize[1] -9) * m))


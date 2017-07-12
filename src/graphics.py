# -*- coding: utf-8 -*-
# !/usr/bin/env python
import pygame
import mahjong
from pygame.locals import *
from sys import exit

WHITE = ( 255, 255, 255 )
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

    def show(self):
        self._display_surf.fill(WHITE)

        self.genStat()
        # self.genPaishan()
        # self.genPlayer()

        pygame.display.update()


    def genStat(self):
        MIDDLE_OF_SCREEN = ( 0.5 * self.windowWidth, 0.5 * self.windowHeight )
        ck = ''
        tmp = self._game.quan % 4
        if tmp == 0:
            ck += u'東'
        elif tmp == 1:
            ck += u'南'
        elif tmp == 2:
            ck += u'西'
        else:
            ck += u'北'
        ck += str(self._game.oya + 1) + u'局0本场\n玩家点数' + str(self._game.user.money)
        self._display_surf.blit(self.font.render(ck, True, (0, 0, 0)), MIDDLE_OF_SCREEN )



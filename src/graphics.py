# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from constants import *
from pygame.locals import *

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

    def __init__(self, _game):
        self._display_surf = pygame.display.set_mode( WINDOW_SIZE, 0, 32 )
        self._game = _game
        self.font = pygame.font.Font('../res/simsun.ttc', FONT_SIZE)
        self.initMenu()
        self.initTiles()

    def show(self):
        self._display_surf.fill(WHITE)

        self.genStat()
        self.genMenu()
        # self.genPaishan()
        self.genPlayer()
        self.genAnalysis()
        self.genJiesuan()
        pygame.display.update()

    def initMenu(self):
        font = pygame.font.Font('../res/simsun.ttc', FONT_SIZE_MENU)

        _x,_y,_h = FONT_SIZE_MENU/2+1,FONT_SIZE_MENU/2+1,FONT_SIZE_MENU-1
        self.menu = {}
        self.menu['rong']        = Botton(font.render(u'和', True, BLACK), (_x, _y))
        self.menu['riichi']      = Botton(font.render(u'立', True, BLACK), (_x, _y + _h))
        self.menu['gang']        = Botton(font.render(u'杠', True, BLACK), (_x, _y + _h * 2))
        self.menu['analysis']    = Botton(font.render(u'理', True, BLACK), (_x, _y + _h * 3))

    def initTiles(self):
        self.tiles = {}
        self.tiles[1], self.tiles[2], self.tiles[3], self.tiles[4] = [], [], [], []
        path = '../res/tiles/'
        for lei in range(1, 5):
            if lei != 4:
                tilemax = 10
            else:
                tilemax = 8
            for x in range(tilemax):
                tmp = pygame.image.load(path + str(lei) + str(x) + '.png')
                self.tiles[lei].append( \
                    pygame.transform.scale(tmp.subsurface((TILE_FIGURE_BLANK_ON_BOTH_SIDES, 0), \
                                                         (TILE_FIGURE_SIZEx - 2 * TILE_FIGURE_BLANK_ON_BOTH_SIDES, TILE_FIGURE_SIZEy)), TILE_SIZE))

    def genMenu(self):
        for button in self.menu.values():
            button.render(self._display_surf)

    def buttonPressed(self, event):
        button_pressed = None
        for button_name, button in self.menu.items():
            if button.is_over(event.pos):
                button_pressed = button_name
                break
        return button_pressed

    def tilePressed(self,event):
        # return the tile index
        tile_pressed = None
        x, y = event.pos
        x -= HAND_POSx
        y -= HAND_POSy
        if 0 < y and y < TILE_SIZEy:
            if 0 < x and x < TILE_SIZEx * len(self._game.user.hand):
                index = x // TILE_SIZEx
                return index
            elif (x - HAND_GAP) // TILE_SIZEx == len(self._game.user.hand):
                return len(self._game.user.hand) +1

        return tile_pressed


    def genStat(self):
        changkuang = ''
        tmp = self._game.quan % NUM_OF_SET_PER_QUAN
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
        ck = self.font.render(changkuang, True, BLACK)
        ds = self.font.render(dianshu   , True, BLACK)
        h_ck = ck.get_height()
        self._display_surf.blit(ck, STAT_POS )
        self._display_surf.blit(ds, (STAT_POS[0], STAT_POS[1] + h_ck) )

    def genPlayer(self):
        _hand = self._game.user.hand
        _pai  = self._game.user.mopai
        for p, i in zip(_hand, range(len(_hand))):
            m, n = p // 10, p % 10
            x, y = HAND_POSx + i * TILE_SIZEx, HAND_POSy
            self._display_surf.blit(self.tiles[m][n], (x, y))

        self._display_surf.blit(self.tiles[_pai // 10][_pai % 10], (x + HAND_GAP + TILE_SIZEx, y))

        # show angang
        # TODO: change to show chi peng gang
        right = WINDOW_WIDTH - TILE_SIZEx
        for g in self._game.user.agang:
            self._display_surf.blit(self.tiles[4][0], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx
            self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx
            self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx
            self._display_surf.blit(self.tiles[4][0], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx

        # show drops

        for index in range(len(self._game.user.dropped) - 1, -1, -1):
            m, n = index // MAX_DROP_A_LINE, index % MAX_DROP_A_LINE
            tile_tmp = self._game.user.dropped[index]
            self._display_surf.blit( self.tiles[tile_tmp // 10][tile_tmp % 10], \
                                    (DROP_POSx + TILE_SIZEx * n, \
                                     DROP_POSy + (TILE_SIZEy - TILE_SIZE_BLANK) * m) )


    def genAnalysis(self):
        if self._game.user.analysisTag == True:
            font = self.font
            xiangtingshu, MINexp = self._game.user.chaifen2(self._game.user.hand)
            yxz = MINexp[len(MINexp)]
            ptstr = str(xiangtingshu) + u'向听'
            analysis = font.render(ptstr, True, BLACK)
            h = analysis.get_height()

            self._display_surf.blit(analysis, (ANALYSIS_POSx, ANALYSIS_POSy))
            # ANALYSIS_POSy += h
            for index in range(len(yxz) -1, -1, -1):
                m, n = index // MAX_DROP_A_LINE, index % MAX_DROP_A_LINE
                self._display_surf.blit( self.tiles[yxz[index] // 10][yxz[index] % 10], \
                                        (ANALYSIS_POSx + TILE_SIZEx * n, \
                                         ANALYSIS_POSy + h + (TILE_SIZEy - TILE_SIZE_BLANK) * m))

    def genJiesuan(self):
        if self._game.setTag == True:
            font = pygame.font.Font('../res/simsun.ttc', JIESUAN_FONT)
            index = 1
            if self._game.yi[1] == 0:
                index = 0
                ptstr = str(self._game.fu[0]) + u'符' + str(self._game.yi[0]) + u'番' + str(int(self._game.dedian)) + u'点'
            elif self._game.yi[1] == 1:
                ptstr = u'役满' + str(int(self._game.dedian)) + u'点'
            else:
                ptstr = str(self._game.yi[1]) + u'倍役满' + str(int(self._game.dedian)) + u'点'
            fufandian = font.render(ptstr, True, BLACK)
            h = fufandian.get_height()
            fanzhongcount = 0
            for s in self._game.fan[index]:
                self._display_surf.blit(font.render(s, True, BLACK), (JIESUAN_POSx, JIESUAN_POSy + h * fanzhongcount))
                fanzhongcount += 1
            self._display_surf.blit(fufandian, (JIESUAN_POSx, JIESUAN_POSy + h * fanzhongcount))
        elif self._game.setTag == END_LIUJU:
            font = pygame.font.Font('../res/simsun.ttc', JIESUAN_FONT)
            self._display_surf.blit(font.render(u'流局', True, BLACK), JIESUAN_POS)

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from constants import *
from pygame.locals import *
from Util import Util

class Botton(object):

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
        self.genYama14()
        self.genPlayer()
        self.genAnalysis()
        self.genJiesuan()
        pygame.display.update()

    def initMenu(self):
        font = pygame.font.Font('../res/simsun.ttc', FONT_SIZE_MENU)

        _h = FONT_SIZE_MENU  + MENU_GAP

        self.menu = {}
        self.menu['rong']        = Botton(font.render(u'和', True, BLACK, GRAY), (MENU_POSx , MENU_POSy ))
        self.menu['riichi']      = Botton(font.render(u'立', True, BLACK, GRAY), (MENU_POSx + _h, MENU_POSy ))
        self.menu['gang']        = Botton(font.render(u'杠', True, BLACK, GRAY), (MENU_POSx + _h * 2, MENU_POSy ))
        self.menu['analysis']    = Botton(font.render(u'理', True, BLACK, GRAY), (MENU_POSx + _h * 3, MENU_POSy ))

    def initTiles(self):
        self.tiles = {}
        self.tiles[1], self.tiles[2], self.tiles[3], self.tiles[4] = [], [], [], []
        self.tiles_small = {}
        self.tiles_small[1], self.tiles_small[2], self.tiles_small[3], self.tiles_small[4] = [], [], [], []
        path = '../res/tiles/'
        for lei in range(1, 5):
            if lei != 4:
                tilemax = 10
            else:
                tilemax = 8
            for x in range(tilemax):
                tmp = pygame.image.load(path + str(lei) + str(x) + '.png')
                self.tiles[lei].append( \
                    pygame.transform.smoothscale(tmp.subsurface((TILE_FIGURE_BLANK_ON_BOTH_SIDES, 0), \
                                                         (TILE_FIGURE_SIZEx - 2 * TILE_FIGURE_BLANK_ON_BOTH_SIDES, TILE_FIGURE_SIZEy)), TILE_SIZE))
                self.tiles_small[lei].append( \
                    pygame.transform.smoothscale(tmp.subsurface((TILE_FIGURE_BLANK_ON_BOTH_SIDES, 0), \
                                                         (TILE_FIGURE_SIZEx - 2 * TILE_FIGURE_BLANK_ON_BOTH_SIDES, TILE_FIGURE_SIZEy)), TILE_SIZE_SMALL))

    def rotateTile(self, tilefigure, position):
        if position == 0:
            return
        elif position == 1:
            rotate_angle = 90
        elif position == 2:
            rotate_angle = 180
        elif position == 3:
            rotate_angle = 270
        elif position >3:
            rotate_angle = position
        return pygame.transform.rotate(tilefigure, rotate_angle)

    def rotateTileInside(self, tilefigure):
        """
        This function rotates the inside of the tile so that is shows properly on the screen.
        The default input tilefigure is in the upright position (original file in the /res/tiles/).
        Currently this function is useless, as the tile figure is not with pure background.
        """
        tileinside = tilefigure.subsurface(TILE_INSIDE_POS, TILE_INSIDE_SIZE)
        tilefigure_out = tilefigure.copy()
        tilefigure_out.blit(pygame.transform.rotate(tileinside, 180), TILE_INSIDE_POS)
        return tilefigure_out

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
            if 0 < x and x < TILE_SIZEx * len(self._game.user.hand.in_hand):
                index = x // TILE_SIZEx
                return index
            elif (x - HAND_GAP) // TILE_SIZEx == len(self._game.user.hand.in_hand):
                return len(self._game.user.hand.in_hand) +1

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

    def genYama14(self):
        tile_backside = self.rotateTile(self.tiles_small[4][0], 180)
        dora_number = len(self._game.dora)
        for ind in range(6,-1,-1):
            self._display_surf.blit(tile_backside, \
                                    ( YAMA_POSx + ind * TILE_SIZE_SMALL[0], YAMA_POSy + TILE_SIZE_SMALL_BLANK ) )
            if 5 - dora_number<= ind and ind <=4 :
                pai_tmp = self._game.yama[self._game.dora[4 - ind]]
                m, n = pai_tmp //10, pai_tmp % 10
                self._display_surf.blit( self.rotateTile(self.tiles_small[m][n],180), \
                                        ( YAMA_POSx + ind * TILE_SIZE_SMALL[0], YAMA_POSy ) )
                if self._game.setTag == True:
                    pai_tmp = self._game.yama[self._game.ura[4 - ind]]
                    m, n = pai_tmp // 10, pai_tmp % 10
                    self._display_surf.blit(self.rotateTile(self.tiles_small[m][n],180),
                                            (YAMA_POSx + ind * TILE_SIZE_SMALL[0], YAMA_POSy + TILE_SIZE_SMALL[1] ) )

            else:
                self._display_surf.blit( tile_backside, \
                                        ( YAMA_POSx + ind * TILE_SIZE_SMALL[0], YAMA_POSy ) )

    def genPlayer(self):
        _hand = self._game.user.hand.in_hand
        _pai  = self._game.user.hand.new_tile
        for p, i in zip(_hand, range(len(_hand))):
            m, n = p // 10, p % 10
            x, y = HAND_POSx + i * TILE_SIZEx, HAND_POSy
            self._display_surf.blit(self.tiles[m][n], (x, y))
        
        if _pai:
            self._display_surf.blit(self.tiles[_pai // 10][_pai % 10], (x + HAND_GAP + TILE_SIZEx, y))

        # show angang
        # TODO: change to show chi peng gang
        right = WINDOW_WIDTH - TILE_SIZEx
        for g in self._game.user.hand.fulu:
            self._display_surf.blit(self.tiles[4][0], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx
            self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx
            self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx
            self._display_surf.blit(self.tiles[4][0], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            right -= TILE_SIZEx

        # show drops
        # Now the drooped tiles are shown using small ones
        for index in range(len(self._game.user.dropped) - 1, -1, -1):
            m, n = index // MAX_DROP_A_LINE, index % MAX_DROP_A_LINE
            tile_tmp = self._game.user.dropped[index]
            self._display_surf.blit( self.tiles_small[tile_tmp // 10][tile_tmp % 10], \
                                    (DROP_POSx + TILE_SIZE_SMALL[0] * n, \
                                     DROP_POSy + (TILE_SIZE_SMALL[1] - TILE_SIZE_SMALL_BLANK) * m) )

    def genAnalysis(self):
        if self._game.user.analysisTag == True:
            font = self.font
            xiangtingshu, MINexp = self._game.user.hand.chaifen2(self._game.user.hand.in_hand)
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
            self._game.user.analysisTag = False
            font = pygame.font.Font('../res/simsun.ttc', JIESUAN_FONT)
            self._display_surf.blit(font.render(u'流局', True, BLACK), JIESUAN_POS)

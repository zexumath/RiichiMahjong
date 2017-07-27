# !/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import numpy as np
from constants import *

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
        self.allSprite = pygame.sprite.OrderedUpdates()

        self.jiesuansprite = Jiesuan()
        self.analysissprite = Analysis()
        self.playerhandsprite = HandSprite()
        self.playerdropsprite = DropSprite()
        self.all_hand_sprite = [self.playerhandsprite]
        self.all_drop_sprite = [self.playerdropsprite]
        for ind in range(1,4):
            self.all_hand_sprite.append(HandSprite())
            self.all_drop_sprite.append(DropSprite())

    def show(self):
        self._display_surf.fill(WHITE)
        self.genStat()
        self.genMenu()
        self.genYama14()
        self.genPlayer()
        self.genAI()
        self.genAnalysis()
        self.genJiesuan()
        self.allSprite.draw(self._display_surf)
        pygame.display.flip()

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
        x -= HAND_REGION_POS[0][0] + HAND_POS_REL_X
        y -= HAND_REGION_POS[0][1] + HAND_POS_REL_Y
        if 0 < y and y < TILE_SIZEy:
            if 0 < x and x < TILE_SIZEx * len(self._game.user.hand.in_hand):
                index = x // TILE_SIZEx
                return index
            elif (x - HAND_GAP) // TILE_SIZEx == len(self._game.user.hand.in_hand):
                return len(self._game.user.hand.in_hand)
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
        changkuang += str(self._game.ju + 1) + u'局0本场'
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
        # _hand = self._game.user.hand.in_hand
        # _pai  = self._game.user.hand.new_tile
        # for p, i in zip(_hand, range(len(_hand))):
            # m, n = p // 10, p % 10
            # x, y = HAND_POSx + i * TILE_SIZEx, HAND_POSy
            # self._display_surf.blit(self.tiles[m][n], (x, y))

        # if _pai:
            # self._display_surf.blit(self.tiles[_pai // 10][_pai % 10], (x + HAND_GAP + TILE_SIZEx, y))

        # # show angang
        # # TODO: change to show chi peng gang
        # right = WINDOW_WIDTH - TILE_SIZEx
        # for g in self._game.user.hand.fulu:
            # self._display_surf.blit(self.tiles[4][0], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            # right -= TILE_SIZEx
            # self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            # right -= TILE_SIZEx
            # self._display_surf.blit(self.tiles[g[0] // 10][g[0] % 10], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            # right -= TILE_SIZEx
            # self._display_surf.blit(self.tiles[4][0], (right, HAND_POSy + HAND_CHI_PENG_GANG_DIFF))
            # right -= TILE_SIZEx

        self.playerhandsprite.update((HAND_REGION_WIDTH_02, HAND_REGION_HEIGHT), self._game.user, self.tiles)
        self.playerhandsprite.add(self.allSprite)
        # show drops
        # Now the drooped tiles are shown using small ones
        # for index in range(len(self._game.user.dropped) - 1, -1, -1):
            # m, n = index // MAX_DROP_A_LINE, index % MAX_DROP_A_LINE
            # tile_tmp = self._game.user.dropped[index]
            # self._display_surf.blit( self.tiles_small[tile_tmp // 10][tile_tmp % 10], \
                                    # (DROP_POSx + TILE_SIZE_SMALL[0] * n, \
                                     # DROP_POSy + (TILE_SIZE_SMALL[1] - TILE_SIZE_SMALL_BLANK) * m) )
        self.playerdropsprite.update((DROP_REGION_WIDTH, DROP_REGION_HEIGHT), self._game.user, self.tiles_small)
        self.playerdropsprite.add(self.allSprite)

    def genAI(self):
        # for ind in range(1,4):
            # rotate_degree = 90 * ind
            # if ind ==1:
                # # hand_start_pos_x,hand_start_pos_y = AI1_HAND_POSx, AI1_HAND_POSy
                # # hand_dx, hand_dy = 0, -TILE_SIZE_SMALL[0]
                # drop_start_pos_x,drop_start_pos_y = AI1_DROP_POSx, AI1_DROP_POSy
                # drop_dx, drop_dy = TILE_SIZE_SMALL[1] - TILE_SIZE_SMALL_BLANK, -TILE_SIZE_SMALL[0]
            # elif ind ==2:
                # # hand_start_pos_x,hand_start_pos_y = AI2_HAND_POSx, AI2_HAND_POSy
                # # hand_dx, hand_dy = -TILE_SIZE_SMALL[0], 0
                # drop_start_pos_x,drop_start_pos_y = AI2_DROP_POSx, AI2_DROP_POSy
                # drop_dx, drop_dy = -TILE_SIZE_SMALL[0], -TILE_SIZE_SMALL[1] + TILE_SIZE_SMALL_BLANK
            # elif ind ==3:
                # # hand_start_pos_x,hand_start_pos_y = AI3_HAND_POSx, AI3_HAND_POSy
                # # hand_dx, hand_dy = 0, TILE_SIZE_SMALL[0]
                # drop_start_pos_x,drop_start_pos_y = AI3_DROP_POSx, AI3_DROP_POSy
                # drop_dx, drop_dy = -TILE_SIZE_SMALL[1] + TILE_SIZE_SMALL_BLANK, TILE_SIZE_SMALL[0]

            if ind % 2 == 0:
                self.all_hand_sprite[ind].update((HAND_REGION_WIDTH_02, HAND_REGION_HEIGHT),
                                                self._game.seats[ind], self.tiles_small)
            else:
                self.all_hand_sprite[ind].update((HAND_REGION_WIDTH_13, HAND_REGION_HEIGHT),
                                                self._game.seats[ind], self.tiles_small)

            self.all_hand_sprite[ind].add(self.allSprite)

            self.all_drop_sprite[ind].update((DROP_REGION_WIDTH, DROP_REGION_HEIGHT),
                                            self._game.seats[ind], self.tiles_small)
            self.all_drop_sprite[ind].add(self.allSprite)
            # show hand
            # _hand = self._game.seats[ind].hand.in_hand
            # _pai  = self._game.seats[ind].hand.new_tile
            # for p, i in zip(_hand, range(len(_hand))):
                # # print ind
                # # print _hand
                # # print p, i
                # m, n = p // 10, p % 10
                # tilefigure = self.rotateTile(self.tiles_small[m][n], rotate_degree)
                # self._display_surf.blit(tilefigure, (hand_start_pos_x + hand_dx * i,
                                                     # hand_start_pos_y + hand_dy * i))
            # if _pai:
                # m, n = _pai // 10, _pai % 10
                # tilefigure = self.rotateTile(self.tiles_small[m][n], rotate_degree)
                # self._display_surf.blit(tilefigure, (hand_start_pos_x + hand_dx * (i+1) + np.sign(hand_dx) * HAND_GAP,
                                                     # hand_start_pos_y + hand_dy * (i+1) + np.sign(hand_dy) * HAND_GAP))

            # show drop
            # _dropped = self._game.seats[ind].dropped
            # for index in range(len(_dropped) -1, -1, -1):
                # rr, tt = index // MAX_DROP_A_LINE, index % MAX_DROP_A_LINE
                # _pai = _dropped[index]
                # m, n = _pai // 10, _pai % 10
                # tilefigure = self.rotateTile(self.tiles_small[m][n], rotate_degree)
                # if ind ==2:
                    # self._display_surf.blit(tilefigure, (drop_start_pos_x + drop_dx * tt,
                                                         # drop_start_pos_y + drop_dy * rr))
                # else:
                    # self._display_surf.blit(tilefigure, (drop_start_pos_x + drop_dx * rr,
                                                         # drop_start_pos_y + drop_dy * tt))

    def genAnalysis(self):
        if self._game.user.analysisTag == True:
            self.analysissprite.update( ANALYSIS_SIZE, self._game, self.font, self.tiles_small)
            self.analysissprite.add(self.allSprite)
        else:
            self.analysissprite.remove(self.allSprite)
    # def genJiesuan(self):
        # if self._game.setTag == END_RONG:
            # font = pygame.font.Font('../res/simsun.ttc', JIESUAN_FONT)
            # index = 1
            # if self._game.user.yi[1] == 0:
                # index = 0
                # ptstr = str(self._game.user.fu[0]) + u'符' + str(self._game.user.yi[0]) + u'番' + str(int(self._game.user.dedian)) + u'点'
            # elif self._game.user.yi[1] == 1:
                # ptstr = u'役满' + str(int(self._game.user.dedian)) + u'点'
            # else:
                # ptstr = str(self._game.user.yi[1]) + u'倍役满' + str(int(self._game.user.dedian)) + u'点'
            # fufandian = font.render(ptstr, True, BLACK)
            # h = fufandian.get_height()
            # fanzhongcount = 0
            # for s in self._game.user.fan[index]:
                # self._display_surf.blit(font.render(s, True, BLACK), (JIESUAN_POSx, JIESUAN_POSy + h * fanzhongcount))
                # fanzhongcount += 1
            # self._display_surf.blit(fufandian, (JIESUAN_POSx, JIESUAN_POSy + h * fanzhongcount))
        # elif self._game.setTag == END_LIUJU:
            # self._game.user.analysisTag = False
            # font = pygame.font.Font('../res/simsun.ttc', JIESUAN_FONT)
            # self._display_surf.blit(font.render(u'流局', True, BLACK), JIESUAN_POS)

    def genJiesuan(self):
        if self._game.setTag==False:
            # self.jiesuansprite.dirty   = 2
            # self.jiesuansprite.visible = 0
            pass
        else:
            self.jiesuansprite.update( JIESUAN_SIZE, self._game, 0)
            self.jiesuansprite.add(self.allSprite)

    def clear(self):
        self.allSprite.empty()

class Jiesuan(pygame.sprite.DirtySprite):

    def __init__(self, size=(0,0), _game=None, _rong_player=0):
        """
         this class generate one single rectangle showing the information of jiesuan.
         :param size: [width, height] of the rectangle
         :param _game: instance of a gametable class recording game information
         :param: _rong_player: the player who calls for a jiesuan. todo: this could be contained in _game.
        """
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_alpha( HALF_TRANSPARENT )
        self.rect = self.image.get_rect()
        self.rect.x = JIESUAN_POSx
        self.rect.y = JIESUAN_POSy

        if _game==None: return
        else: self.update(_game, _rong_player)

    def update(self, size, _game, _rong_player):
        self.image = pygame.Surface(size)
        self.image.set_alpha( HALF_TRANSPARENT )
        if _game.setTag == END_RONG:
            font = pygame.font.Font('../res/simsun.ttc', JIESUAN_FONT)
            index = 1
            if _game.seats[_rong_player].yi[1] == 0:
                index = 0
                ptstr = str(_game.seats[_rong_player].fu[0]) + u'符' + str(_game.seats[_rong_player].yi[0]) + u'番' + str(int(_game.seats[_rong_player].dedian)) + u'点'
            elif _game.seats[_rong_player].yi[1] == 1:
                ptstr = u'役满' + str(int(_game.seats[_rong_player].dedian)) + u'点'
            else:
                ptstr = str(_game.seats[_rong_player].yi[1]) + u'倍役满' + str(int(_game.seats[_rong_player].dedian)) + u'点'
            fufandian = font.render(ptstr, True, WHITE)
            h = fufandian.get_height()
            fanzhongcount = 0
            for s in _game.seats[_rong_player].fan[index]:
                self.image.blit(font.render(s, True, WHITE), (0, 0 + h * fanzhongcount))
                fanzhongcount += 1
            self.image.blit(fufandian, (0, 0 + h * fanzhongcount))
        elif _game.setTag == END_LIUJU:
            _game.seats[_rong_player].analysisTag = False
            font = pygame.font.Font('../res/simsun.ttc', JIESUAN_FONT)
            self.image.blit(font.render(u'流局', True, WHITE), (0,0) )

class Analysis(pygame.sprite.DirtySprite):

    def __init__(self, size=(0,0), _game=None, font=None):
        """
         This class generates one single rectangle showing the information of analysis.
         :param size: [width, height] of the rectangle
         :param _game: instance of a GameTable class recording game information
        """

        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_alpha( ONE_FOURTH_TRANSPARENT )
        self.rect = self.image.get_rect()
        self.rect.x = ANALYSIS_POSx
        self.rect.y = ANALYSIS_POSy

        if _game!=None:
            self.update(_game, font)

    def update(self, size, _game, font, tiles):
        self.image = pygame.Surface(size)
        self.image.set_alpha( ONE_FOURTH_TRANSPARENT )

        xiangtingshu, MINexp = _game.user.hand.chaifen2(_game.user.hand.in_hand)
        yxz = MINexp[len(MINexp)]
        ptstr = str(xiangtingshu) + u'向听'
        analysis = font.render(ptstr, True, WHITE)
        h = analysis.get_height()

        self.image.blit(analysis, (0, 0))
        for index in range(len(yxz) -1, -1, -1):
            m, n = index // MAX_DROP_A_LINE, index % MAX_DROP_A_LINE
            self.image.blit( tiles[yxz[index] // 10][yxz[index] % 10], \
                                    (TILE_SIZE_SMALL[0] * n, \
                                        h + (TILE_SIZE_SMALL[1] - TILE_SIZE_SMALL_BLANK) * m))

class HandSprite(pygame.sprite.DirtySprite):

    def __init__(self, size=(0,0), _user=None, tiles=None):
        """
         This class generates one single rectangle showing the hand tiles.
         :param size: [width, height] of the rectangle.
         :param _user: instance of a Player class recording player information.
        """

        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_alpha( ONE_FOURTH_TRANSPARENT )
        self.rect = self.image.get_rect()

        if _user!=None:
            self.update(_user, tiles)

    def update(self, size, _user, tiles):
        self.image = pygame.Surface(size)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = HAND_REGION_POS[_user.position]

        _hand = _user.hand.in_hand
        _pai  = _user.hand.new_tile

        tile_size_x, tile_size_y = tiles[1][1].get_size()

        for p, i in zip(_hand, range(len(_hand))):
            m, n = p // 10, p % 10
            x, y = HAND_POS_REL_X + i * tile_size_x, HAND_POS_REL_Y
            self.image.blit(tiles[m][n], (x, y))
        if _pai:
            self.image.blit(tiles[_pai // 10][_pai % 10], (x + HAND_GAP + tile_size_x, y))

        rotate_angle = 90 * _user.position
        # print _user.position
        # print self.rect.x, self.rect.y
        if rotate_angle:
            self.image = pygame.transform.rotate(self.image, rotate_angle)

class DropSprite(pygame.sprite.DirtySprite):

    def __init__(self, size=(0,0), _user=None, tiles=None):
        """
         This class generates one single rectangle showing the dropped tiles.
         :param size: [width, height] of the rectangle.
         :param _user: instance of a Player class recording player information.
        """

        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.set_alpha( ONE_FOURTH_TRANSPARENT )
        self.rect = self.image.get_rect()

        if _user!=None:
            self.update(_user, tiles)

    def update(self, size, _user, tiles):

        self.image = pygame.Surface(size)
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        # pygame.draw.rect(self.image, BLACK, self.rect, 1)
        self.rect.x, self.rect.y = DROP_REGION_POS[_user.position]

        _dropped = _user.dropped

        tile_size_x, tile_size_y = tiles[1][1].get_size()

        x, y = 0, 0

        for index in range(len(_dropped) -1, -1, -1):
            rr, tt = index // MAX_DROP_A_LINE, index % MAX_DROP_A_LINE
            if rr>2:
                rr = 2
                tt = index - rr * MAX_DROP_A_LINE

            _pai = _dropped[index]
            m, n = _pai // 10, _pai % 10
            self.image.blit(tiles[m][n], (x + tt * tile_size_x, y + rr * (tile_size_y-TILE_SIZE_SMALL_BLANK)))

        rotate_angle = 90 * _user.position
        if rotate_angle:
            self.image = pygame.transform.rotate(self.image, rotate_angle)



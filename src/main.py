#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from sys import exit
from pygame.locals import *
import mahjong
import graphics
from constants import *

class RiichiMahjong:

    def __init__(self):
        self._running   = True
        self._game      = None
        self._screen    = None

    def on_init(self):
        pygame.init()
        self._game = mahjong.MahjongGame()
        self._screen = graphics.Screen(self._game)
        self._running = True

    def on_loop(self):
        pass

    def on_event(self,event):
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if self._game.setComplete():
                self._game.newset()
                self._game.user._mopai = self._game.serve()
            else:
                button_pressed = self._screen.buttonPressed(event)
                tile_pressed   = self._screen.tilePressed(event)
                if  button_pressed != None:
                    if button_pressed == 'rong':
                        self._game.menu_rong(self._game.user.mopai)
                    elif button_pressed == 'riichi':
                        self._game.menu_riichi()
                    elif button_pressed == 'gang':
                        self._game.menu_gang()
                    elif button_pressed == 'analysis':
                        self._game.menu_analysis()
                elif tile_pressed != None:
                    if self._game.user.riichi == WAIT_FOR_RIICHI_PAI:
                        # This is a status of waiting for riichi
                        droptmp = self._game.user.drop(tile_pressed)
                        if droptmp:
                            self._game.user.riichi = self._game.xun
                            self._game.serve()
                    elif self._game.user.gangTag == False:
                        droptmp = self._game.user.drop(tile_pressed)
                        if droptmp:
                            self._game.serve()
                    else:
                        gangtmp = self._game.user.gang(tile_pressed)
                        if gangtmp:
                            self._game.gangserve()
                        else:
                            self._game.user.gangTag = False
                else:
                    self._game.tagclear()







    def on_render(self):
        self._screen.show()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            exit()

        self._game.newset()
        self._pai = self._game.serve()

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__" :
    riichiMahjong = RiichiMahjong()
    riichiMahjong.on_execute()


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from sys import exit
from pygame.locals import *
import mahjong
import graphics

WHITE = (255, 255, 255)

class RiichiMahjong:

    windowWidth  = 800
    windowHeight = 600


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
                if self._menu.clicked() == True:
                    """ Do something"""
                elif self._menu.select():
                    pass




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


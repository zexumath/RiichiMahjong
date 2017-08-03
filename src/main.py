#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from sys import exit
from pygame.locals import *
import mahjong
from Game import GameTable
import graphics
from constants import *

class RiichiMahjong:

    def __init__(self):
        self._running   = True
        self._game      = None
        self._screen    = None

    def on_init(self):
        pygame.init()
        self._game = GameTable()
        self._screen = graphics.Screen(self._game)
        self._running = True

    def on_loop(self):
        pass

    def on_event(self,event):
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if self._game.setComplete():
                self._game.newset()
                self._game.serve()
                self._screen.clear()
                # self._game.tile_ai_drop()
                # self._game.user._mopai = self._game.serve()
            else:
                button_pressed = self._screen.buttonPressed(event)
                tile_pressed   = self._screen.tilePressed(event)
                if  button_pressed != None:
                    self._game.menu_respond(button_pressed)
                elif self._game.turn!=0:
                    self._game.next_step()
                elif tile_pressed != None:
                    self._game.tile_respond(tile_pressed)
                else:
                    self._game.tagclear()
        elif event.type == KEYDOWN:
            if event.key == K_RCTRL or event.key == K_LCTRL:
                self._game.next_step()
        else:
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
        self._game.serve()
        # self._game.tile_ai_drop()
        # self._pai = self._game.serve()

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__" :
    riichiMahjong = RiichiMahjong()
    riichiMahjong.on_execute()


# -*- coding: utf-8 -*-
# MyLibrary.py

import random, math
from constants import *

class Player(object):
    def __init__(self):
        #need to be in Hand class
        self.mopai = []
        self.hand = []
        self.chi = []
        self.peng = []
        self.mgang = []
        self.agang = []
        self.ontable = []

        self.dropped = []
        self.isclose = True
        self.riichi = False
        self.zimo = False
        self.rongpai = 0
        self.fu = {}
        self.yi = {}
        self.exp = {}
        self.rongflag = False
        self.lingshang = False
        self.tingflag = False
        #以下两个每局不用初始化
        self.money = MONEY_START
        self.position = -1

    def newset_init(self):
        #need to be in Hand class
        self.mopai = []
        self.hand = []
        self.chi = []
        self.peng = []
        self.mgang = []
        self.agang = []
        self.ontable = []

        self.dropped = []
        self.isclose = True
        self.riichi = False
        self.zimo = False
        self.rongpai = 0
        self.fu = {}
        self.yi = {}
        self.exp = {}
        self.rongflag = False
        self.lingshang = False
        self.tingflag = False

class GameTable():
    def __init__(self):
        self.pai = [] #all of the pai
        self.seats = []
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.player4 = Player()
        self.create()
        self.yama = [] # the remaining pai
        self.quan = 0 #0,1,2,3 represent east, north, west, north quan
        self.ju = 0 #东风圈二局二本场
        self.oya = -1 #0,1,2,3 represent east, north, west, north
        self.xun = 0
        self.benchang = 0
        self.lizhibang = 0
        self.liuju = False
        self.lastrongplayer = -2 #没有人胡 return -2

    def create(self):
        for i in range(4):
            start = 10
            #for j in range(TILE_START + 1, TILE_START + TILE_RANGE):
            for j in range(start + 1, start + 30):
                if j % 10 != 0: self.pai.append(j)
            for k in range(41, 48):
                self.pai.append(k)
        self.seats = [self.player1, self.player2, self.player3, self.player4]
        #random.shuffle(self.seats) #judge the seats: east north west north, seats[0] to call the player seating east
        for i in range(4): #seats position set for players
            self.seats[i].position = i

    def judge_benchang(self): #判断是否是下一本场, 否则切换亲家
        if self.lastrongplayer == self.oya or (self.liuju and self.seats[self.oya].tingflag):
            self.benchang += 1
        else:
            self.oya += 1
            self.benchang = 0

    def newset(self):
        self.judge_benchang()
        self.quan, self.oya = self.quan + self.oya // NUM_OF_SET_PER_QUAN, self.oya % NUM_OF_SET_PER_QUAN
        self.ju = self.oya
        self.yama = self.pai[:]
        random.shuffle(self.yama)
        self.dora = self.yama[DORA_DEFAULT]
        self.ura = []
        self.xun = 0

        for i in range(4):
            tmp = (self.oya + i) % NUM_OF_SET_PER_QUAN #摸牌起始位置往下, tmp表示这人的position
            self.seats[tmp].newset_init()
            if i == 0:
                self.seats[tmp].hand = self.yama[-4:]+self.yama[-20:-16]+self.yama[-36:-32]+[self.yama[-48]]
            else:
                for j in range(3):
                    self.seats[tmp].hand += self.yama[-(i+j*4+1)*4:-(i+j*4)*4]
                self.seats[tmp].hand += [self.yama[-48-i]]
            self.seats[tmp].hand.sort()
            self.seats[tmp].fu, self.seats[tmp].yi, self.seats[tmp].fan = [0, 0], [0, 0], [0, 0]
            self.seats[tmp].dedian = 0
            self.seats[tmp].setTag = 0
        self.yama = self.yama[:-52]

def main():
    _game = GameTable()
    _game.lastrongplayer = 1
    _game.oya = 3
    _game.newset()
    print(_game.benchang)
    print(_game.oya)
    print(_game.yama)
    print(_game.dora)
    print("East player:")
    print(_game.seats[0].hand)
    print(str(_game.player1.position) + ":")
    print(_game.player1.hand)
    print(str(_game.player2.position) + ":")
    print(_game.player2.hand)
    print(str(_game.player3.position) + ":")
    print(_game.player3.hand)
    print(str(_game.player4.position) + ":")
    print(_game.player4.hand)

main()


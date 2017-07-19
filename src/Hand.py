from constants import *
from Util import Util


class Hand:
    def __init__(self):
        '''
        fulu1, ..., fulu4: Name ('Chi', 'Peng', 'Gang'); tile, first tile in the fulu: ([11]); From: (0, 1, 2, 3),
        0 for your self and 1, 2, 3 represents the player sitting on the right, opposite and left respectively
        '''
        self.in_hand = []
        self.new_tile = []
        self.fulu1 = None
        self.fulu2 = None
        self.fulu3 = None
        self.fulu4 = None

    def new_set_init(self, yama, position, oya_position):
        if position == oya_position:
            self.in_hand = yama[-4:] + yama[-20:-16] + yama[-36:-32] + [yama[-49]]
        else:
            position_to_oya = (position - oya_position) % NUM_OF_SET_PER_QUAN
            pais_to_pick = [yama[-(position_to_oya + j * 4 + 1) * 4:-(position_to_oya + j * 4) * 4] for j in range(3)]
            self.in_hand = [j for i in pais_to_pick for j in i]
            self.in_hand.append(yama[-49 - position_to_oya])


        self.in_hand.sort()
        self.new_tile = []
        self.fulu1 = None
        self.fulu2 = None
        self.fulu3 = None
        self.fulu4 = None

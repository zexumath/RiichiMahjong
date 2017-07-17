from constants import *


class Hand:
    def __init__(self):
        self.in_hand = []
        self.new_pai = []
        self.fulu1 = None
        self.fulu2 = None
        self.fulu3 = None
        self.fulu4 = None

    def new_set_init(self, yama, position, oya_position):
        if position == oya_position:
            self.in_hand = yama[-4:] + yama[-20:-16] + yama[-36:-32] + [yama[-48]]
        else:
            position_to_oya = (position - oya_position) % NUM_OF_SET_PER_QUAN
            pais_to_pick = [yama[-(position_to_oya + j * 4 + 1) * 4:-(position_to_oya + j * 4) * 4] for j in range(3)]
            self.in_hand = [j for i in pais_to_pick for j in i]
            self.in_hand.append(yama[-48 - position_to_oya])

        self.in_hand.sort()
        self.new_pai = []
        self.fulu1 = None
        self.fulu2 = None
        self.fulu3 = None
        self.fulu4 = None


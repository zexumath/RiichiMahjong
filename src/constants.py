# -*- coding: utf-8 -*-
import random

NUM_OF_SET_PER_QUAN = 4

USER_POSITION = 0
OYA_START = random.randint(0,3)

# Constants for table status
WAIT_FOR_SERVE = 1
WAIT_FOR_DROP  = 2
WAIT_FOR_RESPONSE = 3
NO_RESPONSE = 4
WAIT_FOR_CHOOSE = 5

WAIT_FOR_RIICHI_PAI = -1
END_RONG  = 1
END_LIUJU = 2

MONEY_START = 25000

MAX_WAIT_SEC = 4

SUOZI_NOMI = True
if SUOZI_NOMI:
    TILE_START = 30
else:
    TILE_START = 10
TILE_RANGE = 40 - TILE_START

DORA_DEFAULT = 5

MIN_TILES_IN_YAMA = 14
MAX_XUN = 19

HALF_TRANSPARENT = 128
ONE_FOURTH_TRANSPARENT = 192
NO_TRANSPARENT = 255
#--------------- Graphics parameters ----------------#

WINDOW_WIDTH  = 1000
WINDOW_HEIGHT = 800
WINDOW_SIZE   = (WINDOW_WIDTH, WINDOW_HEIGHT)
MIDDLE_OF_WINDOW = (0.5 * WINDOW_WIDTH, 0.5 * WINDOW_HEIGHT)

# Tile size
TILE_FIGURE_SIZE = (128,128)
TILE_FIGURE_SIZEx, TILE_FIGURE_SIZEy = TILE_FIGURE_SIZE
TILE_FIGURE_BLANK_ON_BOTH_SIDES = 23
TILE_SIZE = (41, 64)
TILE_SIZEx, TILE_SIZEy = TILE_SIZE
# The blank part of the tile. This is used to make the drop clearer.
TILE_SIZE_BLANK = 9
TILE_INSIDE_TO_LEFT = 2
TILE_INSIDE_TO_BOTTOM = 2
TILE_INSIDE_POS = (TILE_INSIDE_TO_LEFT, TILE_INSIDE_TO_LEFT + TILE_SIZE_BLANK)
TILE_INSIDE_SIZE = (TILE_SIZEx - 2 * TILE_INSIDE_TO_LEFT, \
                    TILE_SIZEy - TILE_SIZE_BLANK - 2 * TILE_INSIDE_TO_BOTTOM)

# Tile size for dropped tiles, dora, other players hands.
TILE_SIZE_SMALL = (36, 56)
TILE_SIZE_SMALL_BLANK = 8

# Position of the table status
# STAT_POS = (100,100)

# Position of the table status
STAT_REGION_WIDTH  = 12 * TILE_SIZE_SMALL[0]
STAT_REGION_HEIGHT = 8 * TILE_SIZE_SMALL[0]
STAT_REGION_POS = ( (WINDOW_WIDTH  - STAT_REGION_WIDTH)  //2,
                    (WINDOW_HEIGHT - STAT_REGION_HEIGHT) //2 )

# Position of the Yama
YAMA_POSx = STAT_REGION_WIDTH //2 - 4 * TILE_SIZE_SMALL[0]
YAMA_POSy = STAT_REGION_HEIGHT - 2 * TILE_SIZE_SMALL[1]
YAMA_NUM_LEFT_POS = YAMA_POSx - 30


# Position of the analysis
ANALYSIS_SIZE = (400, 500)
ANALYSIS_POS  = ( (WINDOW_WIDTH - ANALYSIS_SIZE[0])//2, (WINDOW_HEIGHT - ANALYSIS_SIZE[1])//2 )
ANALYSIS_POSx, ANALYSIS_POSy = ANALYSIS_POS

# Position of the end-of-game jiesuan
JIESUAN_SIZE = (400, 500)
JIESUAN_POS  = ( (WINDOW_WIDTH - JIESUAN_SIZE[0])//2, (WINDOW_HEIGHT - JIESUAN_SIZE[1])//2 )
JIESUAN_POSx, JIESUAN_POSy = JIESUAN_POS
JIESUAN_FONT = 24

# Position of player hand tiles
HAND_DIFF_TO_BOUNDARY = 30
HAND_POS_TO_BOTTOM = HAND_DIFF_TO_BOUNDARY + TILE_SIZEy
HAND_POS_TO_LEFT   = (WINDOW_WIDTH - 14* TILE_SIZEx) // 2

HAND_POSx, HAND_POSy = HAND_POS_TO_LEFT, WINDOW_HEIGHT - HAND_POS_TO_BOTTOM

# Size of the gap between hand and new tile
HAND_GAP = 8

# Size of difference in height between hand and chi,peng,gang etc.
# HAND_CHI_PENG_GANG_DIFF = HAND_DIFF_TO_BOUNDARY //2

# New implementation of hand figure
HAND_REGION_HEIGHT = 80
HAND_REGION_WIDTH_02  = WINDOW_WIDTH  - HAND_REGION_HEIGHT
HAND_REGION_WIDTH_13  = WINDOW_HEIGHT - HAND_REGION_HEIGHT
HAND_POS_REL_X = 80
HAND_POS_REL_Y = 0
HAND_CHI_PENG_GANG_DIFF = (HAND_REGION_HEIGHT - TILE_SIZEy) //2

HAND_REGION_0_X, HAND_REGION_0_Y= HAND_REGION_HEIGHT   , HAND_REGION_WIDTH_13
HAND_REGION_1_X, HAND_REGION_1_Y= HAND_REGION_WIDTH_02 , 0
HAND_REGION_2_X, HAND_REGION_2_Y= 0                    , 0
HAND_REGION_3_X, HAND_REGION_3_Y= 0                    , HAND_REGION_HEIGHT

HAND_REGION_POS = [ [HAND_REGION_0_X, HAND_REGION_0_Y],
                    [HAND_REGION_1_X, HAND_REGION_1_Y],
                    [HAND_REGION_2_X, HAND_REGION_2_Y],
                    [HAND_REGION_3_X, HAND_REGION_3_Y] ]

# # Position used for showing ai hand tiles
# # AI on the right. Position is the upleft corner of the very bottom handtile.
# AI1_HAND_POSx = WINDOW_WIDTH - TILE_SIZE_SMALL[1] - HAND_DIFF_TO_BOUNDARY
# AI1_HAND_POSy = (WINDOW_HEIGHT + 14* TILE_SIZE_SMALL[0]) // 2 - TILE_SIZE_SMALL[0]
# # AI on the top. Position is the upleft corner of the very right handtile.
# AI2_HAND_POSx = (WINDOW_WIDTH + 14 * TILE_SIZE_SMALL[0]) //2 - TILE_SIZE_SMALL[0]
# AI2_HAND_POSy = HAND_DIFF_TO_BOUNDARY
# # AI on the left. Position is the upleft corner of the very top handtile.
# AI3_HAND_POSx = HAND_DIFF_TO_BOUNDARY
# AI3_HAND_POSy = (WINDOW_HEIGHT - 14 * TILE_SIZE_SMALL[0]) //2


# Drops
MAX_DROP_A_LINE = 6
# Position of the dropped tiles of player
DROP_POS_GAP_TO_HAND = 40

# New implementation using DropSprite
DROP_REGION_WIDTH  = 8 * TILE_SIZE_SMALL[0]
DROP_REGION_HEIGHT = 3 * TILE_SIZE_SMALL[1]

DROP_REGION_0_X = (WINDOW_WIDTH - DROP_REGION_WIDTH ) // 2
DROP_REGION_0_Y = (WINDOW_HEIGHT+ STAT_REGION_HEIGHT) // 2

DROP_REGION_1_X = (WINDOW_WIDTH + STAT_REGION_WIDTH ) // 2
DROP_REGION_1_Y = (WINDOW_HEIGHT- DROP_REGION_WIDTH ) // 2

DROP_REGION_2_X = (WINDOW_WIDTH - DROP_REGION_WIDTH ) // 2
DROP_REGION_2_Y = (WINDOW_HEIGHT- STAT_REGION_HEIGHT) // 2 - DROP_REGION_HEIGHT

DROP_REGION_3_X = (WINDOW_WIDTH - STAT_REGION_WIDTH ) // 2 - DROP_REGION_HEIGHT
DROP_REGION_3_Y = DROP_REGION_1_Y

DROP_REGION_POS = [ [DROP_REGION_0_X, DROP_REGION_0_Y],
                    [DROP_REGION_1_X, DROP_REGION_1_Y],
                    [DROP_REGION_2_X, DROP_REGION_2_Y],
                    [DROP_REGION_3_X, DROP_REGION_3_Y] ]

DROP_POS_TO_BOTTOM = 3*(TILE_SIZEy-TILE_SIZE_BLANK) + TILE_SIZE_BLANK + HAND_POS_TO_BOTTOM + DROP_POS_GAP_TO_HAND
DROP_POS_TO_LEFT   = (WINDOW_WIDTH - MAX_DROP_A_LINE*TILE_SIZEx) //2
DROP_POSx, DROP_POSy = DROP_POS_TO_LEFT, WINDOW_HEIGHT - DROP_POS_TO_BOTTOM
# Position of the dropped tiles of AIs
AI1_DROP_POSx = WINDOW_WIDTH - HAND_DIFF_TO_BOUNDARY \
                             - TILE_SIZE_SMALL[1] * 4 \
                             + TILE_SIZE_SMALL_BLANK * 2 \
                             - DROP_POS_GAP_TO_HAND
AI1_DROP_POSy = (WINDOW_HEIGHT + MAX_DROP_A_LINE * TILE_SIZE_SMALL[0] )//2

AI2_DROP_POSx = (WINDOW_WIDTH + MAX_DROP_A_LINE * TILE_SIZE_SMALL[0] )//2 - TILE_SIZE_SMALL[0]
AI2_DROP_POSy =  HAND_DIFF_TO_BOUNDARY \
                + TILE_SIZE_SMALL[1] * 3 \
                - TILE_SIZE_SMALL_BLANK * 2 \
                + DROP_POS_GAP_TO_HAND

AI3_DROP_POSx =  HAND_DIFF_TO_BOUNDARY \
                + TILE_SIZE_SMALL[1] * 3 \
                - TILE_SIZE_SMALL_BLANK * 2 \
                + DROP_POS_GAP_TO_HAND
AI3_DROP_POSy = (WINDOW_HEIGHT - MAX_DROP_A_LINE * TILE_SIZE_SMALL[0]) //2

# Font sizes
FONT_SIZE = 24
FONT_SIZE_MENU = 32

# Menu position is determined by the fontsize of menu now.
MENU_POS = (HAND_POSx  , HAND_POSy - FONT_SIZE_MENU )
MENU_POSx , MENU_POSy = MENU_POS
MENU_GAP = 2

# COLOR
WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
GRAY  = ( 200, 200, 200 )


# Mahjong related
DONG_XI_NAN_BEI = (u'東', u'西', u'南', u'北')

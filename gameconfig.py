#  Game Screen Settings
spriteSize = 16
spriteScale = 4
imageSize = spriteSize * spriteScale

SCREENWIDTH = 16 * imageSize
SCREENHEIGHT = 14 * imageSize

#  HUD Overlay and Game Screen
GAME_SCREEN = (imageSize, imageSize // 2, imageSize * 13, imageSize * 13)
INFO_PANEL_X, INFO_PANEL_Y = SCREENWIDTH - (imageSize * 2), imageSize // 2
STD_ENEMIES = 20

#  Game Screen Borders
SCREEN_BORDER_LEFT = GAME_SCREEN[0]
SCREEN_BORDER_TOP = GAME_SCREEN[1]
SCREEN_BORDER_RIGHT = GAME_SCREEN[2] + SCREEN_BORDER_LEFT
SCREEN_BORDER_BOTTOM = GAME_SCREEN[3] + SCREEN_BORDER_TOP

#  Start Screen
SCREEN_SCROLL_SPEED = 5

#  New stage Timer
TRANSITION_TIMER = 3000

#  FPS settings
FPS = 60

#  Colour Definitions
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (99, 99, 99)
GREEN = (0, 255, 0)

#  Tank Variables
TANK_SPEED = imageSize // spriteSize
TANK_PARALYSIS = 2000
TANK_SPAWNING_TIME = 3000
Pl1_position = (SCREEN_BORDER_LEFT + imageSize//2 * 8, SCREEN_BORDER_TOP + imageSize//2 * 24)
Pl2_position = (SCREEN_BORDER_LEFT + imageSize//2 * 16, SCREEN_BORDER_TOP + imageSize//2 * 24)
Pc1_position = (SCREEN_BORDER_LEFT + imageSize//2 * 12, SCREEN_BORDER_TOP + imageSize//2 * 0)
Pc2_position = (SCREEN_BORDER_LEFT + imageSize//2 * 24, SCREEN_BORDER_TOP + imageSize//2 * 0)
Pc3_position = (SCREEN_BORDER_LEFT + imageSize//2 * 0, SCREEN_BORDER_TOP + imageSize//2 * 0)


#  Spritesheet images and coordinates
SPAWN_STAR = {"star_0": [(spriteSize * 16), (spriteSize * 6), spriteSize, spriteSize],
              "star_1": [(spriteSize * 17), (spriteSize * 6), spriteSize, spriteSize],
              "star_2": [(spriteSize * 18), (spriteSize * 6), spriteSize, spriteSize],
              "star_3": [(spriteSize * 19), (spriteSize * 6), spriteSize, spriteSize]}
SHIELD = {"shield_1": [(spriteSize * 16), (spriteSize * 9), 16, 16],
          "shield_2": [(spriteSize * 17), (spriteSize * 9), 16, 16]}
POWER_UPS = {"shield":       [(16 * 16), (16 * 7), 16, 16],
             "freeze":       [(16 * 17), (16 * 7), 16, 16],
             "fortify":      [(16 * 18), (16 * 7), 16, 16],
             "power":        [(16 * 19), (16 * 7), 16, 16],
             "explosion":    [(16 * 20), (16 * 7), 16, 16],
             "extra_life":   [(16 * 21), (16 * 7), 16, 16],
             "special":      [(16 * 22), (16 * 7), 16, 16]}
SCORE = {"100": [(spriteSize * 18), (spriteSize * 10), 16, 16],
         "200": [(spriteSize * 19), (spriteSize * 10), 16, 16],
         "300": [(spriteSize * 20), (spriteSize * 10), 16, 16],
         "400": [(spriteSize * 21), (spriteSize * 10), 16, 16],
         "500": [(spriteSize * 22), (spriteSize * 10), 16, 16]}
FLAG = {"Phoenix_Alive":        [(16 * 19), (16 * 2), 16, 16],
        "Phoenix_Destroyed":    [(16 * 20), (16 * 2), 16, 16]}
EXPLOSIONS = {"explode_1": [(spriteSize * 16), (spriteSize * 8), 16, 16],
              "explode_2": [(spriteSize * 17), (spriteSize * 8), 16, 16],
              "explode_3": [(spriteSize * 18), (spriteSize * 8), 16, 16],
              "explode_4": [(spriteSize * 19), (spriteSize * 8), 32, 32],
              "explode_5": [(spriteSize * 21), (spriteSize * 8), 32, 32]}
BULLETS = {"Up": [(spriteSize * 20), (spriteSize * 6) + 4, 8, 8],
           "Left": [(spriteSize * 20) + 8, (spriteSize * 6) + 4, 8, 8],
           "Down": [(spriteSize * 21), (spriteSize * 6) + 4, 8, 8],
           "Right": [(spriteSize * 21) + 8, (spriteSize * 6) + 4, 8, 8]}
MAP_TILES = {
    #  Bricks
    432: {"small": [spriteSize * 16, spriteSize * 4, 8, 8],
          "small_right": [(spriteSize * 16) + 12, spriteSize * 4, 4, 8],
          "small_bot": [spriteSize * 17, (spriteSize * 4) + 4, 8, 4],
          "small_left": [(spriteSize * 17) + 8, spriteSize * 4, 4, 8],
          "small_top": [(spriteSize * 18), spriteSize * 4, 8, 4]},
    #  Steel
    482: {"small": [spriteSize * 16, (spriteSize * 4) + 8, 8, 8]},
    #  Forest
    483: {"small": [(spriteSize * 16) + 8, (spriteSize * 4) + 8, 8, 8]},
    #  Ice
    484: {"small": [(spriteSize * 17), (spriteSize * 4) + 8, 8, 8]},
    #  Water
    533: {"small_1": [(spriteSize * 16) + 8, (spriteSize * 5), 8, 8],
          "small_2": [(spriteSize * 17), (spriteSize * 5), 8, 8]}
}
HUD_INFO = {"stage":    [(16 * 20) + 8, (16 * 11), 40, 8],
            "num_0":    [(16 * 20) + 8, (16 * 11) + 8, 8, 8],
            "num_1":    [(16 * 21), (16 * 11) + 8, 8, 8],
            "num_2":    [(16 * 21) + 8, (16 * 11) + 8, 8, 8],
            "num_3":    [(16 * 22), (16 * 11) + 8, 8, 8],
            "num_4":    [(16 * 22) + 8, (16 * 11) + 8, 8, 8],
            "num_5":    [(16 * 20) + 8, (16 * 12), 8, 8],
            "num_6":    [(16 * 21), (16 * 12), 8, 8],
            "num_7":    [(16 * 21) + 8, (16 * 12), 8, 8],
            "num_8":    [(16 * 22), (16 * 12), 8, 8],
            "num_9":    [(16 * 22) + 8, (16 * 12), 8, 8],
            "life":     [(16 * 20), (16 * 12), 8, 8],
            "info_panel": [(16 * 23), (16 * 0), 32, (16 * 15)],
            "grey_square": [(16 * 23), (16 * 0), 8, 8]}
NUMS = {
    0: [0, 0, 8, 8], 1: [8, 0, 8, 8], 2: [16, 0, 8, 8], 3: [24, 0, 8, 8], 4: [32, 0, 8, 8],
    5: [0, 8, 8, 8], 6: [8, 8, 8, 8], 7: [16, 8, 8, 8], 8: [24, 8, 8, 8], 9: [32, 8, 8, 8]}
CONTEXT = {"pause": [(16 * 18), (16 * 11), 40, 8],
           "game_over": [(16 * 18), (16 * 11) + 8, 32, 16]}

ENEMY_TANK_SPAWNS = [(0, 0), (0, 1), (1, 0), (1, 1),    #  Enemy spawn 1
                     (12, 0), (12, 1), (13, 0), (13, 1), #  Enemy spawn 2
                     (24, 0), (24, 1), (25, 0), (25, 1)]	#Enemy Tank Spawn 3
PLAYER_TANK_SPAWNS = [(8, 24), (8, 25), (9, 24), (9, 25),   # player 1 spawn
                      (16, 24), (16, 25), (17, 24), (17, 25)] # player 2 spawn
BASE = [(12, 24), (12, 25), (13, 24), (13, 25)] # base
FORT = [(11, 25), (11, 24), (11, 23), (12, 23), (13, 23), (14, 23), (14, 24), (14, 25)]
FLAG_POSITION = (SCREEN_BORDER_LEFT + imageSize//2 * 12, SCREEN_BORDER_TOP + imageSize//2 * 24)

#  Tank Spawn Criteria
Tank_Criteria = {
    "level_0": {"image": 4, "health": 1, "speed": 0.5, "cooldown": 1, "power": 1, "score": 100},
    "level_1": {"image": 5, "health": 1, "speed": 1, "cooldown": 1, "power": 1, "score": 200},
    "level_2": {"image": 6, "health": 1, "speed": 0.5, "cooldown": 1, "power": 2, "score": 300},
    "level_3": {"image": 7, "health": 4, "speed": 0.5, "cooldown": 1, "power": 2, "score": 400},
}

Tank_spawn_queue = {"queue_0": [90, 10, 0, 0],
                    "queue_1": [80, 20, 0, 0],
                    "queue_2": [70, 30, 0, 0],
                    "queue_3": [60, 30, 10, 0],
                    "queue_4": [50, 30, 20, 0],
                    "queue_5": [40, 30, 30, 0],
                    "queue_6": [30, 30, 30, 10],
                    "queue_7": [20, 30, 30, 20],
                    "queue_8": [10, 30, 30, 30],
                    "queue_9": [10, 20, 40, 30],
                    "queue_10": [10, 10, 50, 30],
                    "queue_11": [0, 10, 50, 40]
}
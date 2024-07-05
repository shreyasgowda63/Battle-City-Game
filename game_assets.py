import pygame
import gameconfig as gc


class GameAssets:
    def __init__(self):
        """Object containing all of the assets for the game"""
        #  Start Screen images
        self.start_screen = self.load_ind_img("start_screen", True, (gc.SCREENWIDTH, gc.SCREENHEIGHT))
        self.start_screen_token = self.load_ind_img("token", True, (gc.imageSize, gc.imageSize))

        #  Loading in the Sprite Sheets
        self.spritesheet = self.load_ind_img("BattleCity")
        self.number_image_black_white = self.load_ind_img("numbers_black_white")
        self.number_image_black_orange = self.load_ind_img("numbers_black_orange")

        #  Images related to the characters
        self.tank_images = self._load_all_tank_images()
        self.bullet_images = self._get_specified_images(self.spritesheet, gc.BULLETS, gc.BLACK)
        self.shield_images = self._get_specified_images(self.spritesheet, gc.SHIELD, gc.BLACK)
        self.spawn_star_images = self._get_specified_images(self.spritesheet, gc.SPAWN_STAR, gc.BLACK)

        #  Game Related Images
        self.power_up_images = self._get_specified_images(self.spritesheet, gc.POWER_UPS, gc.BLACK)
        self.flag = self._get_specified_images(self.spritesheet, gc.FLAG, gc.BLACK)
        self.explosions = self._get_specified_images(self.spritesheet, gc.EXPLOSIONS, gc.BLACK)
        self.score = self._get_specified_images(self.spritesheet, gc.SCORE, gc.BLACK)

        #  Game HUD Images
        self.hud_images = self._get_specified_images(self.spritesheet, gc.HUD_INFO, gc.BLACK, transparent=False)
        self.context = self._get_specified_images(self.spritesheet, gc.CONTEXT, gc.BLACK)

        #  Tile Images
        self.brick_tiles = self._get_specified_images(self.spritesheet, gc.MAP_TILES[432], gc.BLACK)
        self.steel_tiles = self._get_specified_images(self.spritesheet, gc.MAP_TILES[482], gc.BLACK)
        self.forest_tiles = self._get_specified_images(self.spritesheet, gc.MAP_TILES[483], gc.BLACK)
        self.ice_tiles = self._get_specified_images(self.spritesheet, gc.MAP_TILES[484], gc.BLACK)
        self.water_tiles = self._get_specified_images(self.spritesheet, gc.MAP_TILES[533], gc.BLACK)

        #  Number Images
        self.number_black_white = self._get_specified_images(self.number_image_black_white, gc.NUMS, gc.BLACK)
        self.number_black_orange = self._get_specified_images(self.number_image_black_orange, gc.NUMS, gc.BLACK)

        # Score Sheet Images
        self.score_sheet_images = {}
        for image in ["hiScore", "arrow", "player1", "player2", "pts", "stage", "total"]:
            self.score_sheet_images[image] = self.load_ind_img(image)

        #  Game Sounds
        self.game_start_sound = pygame.mixer.Sound("sounds/gamestart.ogg")

        self.movement_sound = pygame.mixer.Sound("sounds/background player.ogg")
        self.movement_sound.set_volume(0.7)
        self.channel_player_movement_sound = pygame.mixer.Channel(0)

        self.enemy_movement_sound = pygame.mixer.Sound("sounds/background.ogg")
        self.enemy_movement_sound.set_volume(0.4)
        self.channel_enemy_movement_sound = pygame.mixer.Channel(1)

        self.fire_sound = pygame.mixer.Sound("sounds/fire.ogg")
        self.fire_sound.set_volume(1)
        self.channel_fire_sound = pygame.mixer.Channel(2)

        self.brick_sound = pygame.mixer.Sound("sounds/brick.ogg")
        self.channel_brick_sound = pygame.mixer.Channel(3)

        self.steel_sound = pygame.mixer.Sound("sounds/steel.ogg")
        self.channel_steel_sound = pygame.mixer.Channel(4)

        self.explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")
        self.channel_explosion_sound = pygame.mixer.Channel(5)

        self.bonus_sound = pygame.mixer.Sound("sounds/bonus.ogg")
        self.channel_bonus_sound = pygame.mixer.Channel(6)

        self.gameover_sound = pygame.mixer.Sound("sounds/gameover.ogg")
        self.channel_gameover_sound = pygame.mixer.Channel(7)

        self.score_sound = pygame.mixer.Sound("sounds/score.ogg")

    #  Loading in the 256 Tank images
    def _load_all_tank_images(self):
        """Get all the Tank images from the spritesheet, and sort them into a dictionary"""
        tank_image_dict = {}
        for tank in range(8):
            tank_image_dict[f"Tank_{tank}"] = {}
            for group in ["Gold", "Silver", "Green", "Special"]:
                tank_image_dict[f"Tank_{tank}"][group] = {}
                for direction in ["Up", "Down", "Left", "Right"]:
                    tank_image_dict[f"Tank_{tank}"][group][direction] = []

        #  Create a new image for each of the tank images
        for row in range(16):
            for col in range(16):
                surface = pygame.Surface((gc.spriteSize, gc.spriteSize))
                surface.fill(gc.BLACK)
                surface.blit(self.spritesheet, (0, 0), (col * gc.spriteSize, row * gc.spriteSize,
                                                        gc.spriteSize, gc.spriteSize))
                surface.set_colorkey(gc.BLACK)
                #  Resize each of the images
                surface = self.scale_image(surface, gc.spriteScale)
                #  Sort the tank image into it's corect level
                tank_level = self._sort_tanks_into_levels(row)
                #  Sort the tank into its correct group
                tank_group = self._sort_tanks_into_groups(row, col)
                #  Sort the tank images into the correct directions
                tank_direction = self._sort_tanks_by_direction(col)
                tank_image_dict[tank_level][tank_group][tank_direction].append(surface)
        return tank_image_dict

    #  Sorting methods for getting tanks into the correct segments of the dictionary
    def scale_image(self, image, scale):
        """Scales the image according to the size passed in"""
        width, height = image.get_size()
        image = pygame.transform.scale(image, (scale * width, scale * height))
        return image

    def _sort_tanks_into_levels(self, row):
        """Sorts the tanks according to the row"""
        tank_levels = {0: "Tank_0", 1: "Tank_1", 2: "Tank_2", 3: "Tank_3",
                       4: "Tank_4", 5: "Tank_5", 6: "Tank_6", 7: "Tank_7"}
        return tank_levels[row % 8]

    def _sort_tanks_into_groups(self, row, col):
        """Sort each tank image into its different colour groups"""
        if 0 <= row <= 7 and 0 <= col <= 7:
            return "Gold"
        elif 8 <= row <= 16 and 0 <= col <= 7:
            return "Green"
        elif 0 <= row <= 7 and 8 <= col <= 16:
            return "Silver"
        else:
            return "Special"

    def _sort_tanks_by_direction(self, col):
        """Returns the current tank image by direction"""
        if col % 8 <= 1: return "Up"
        elif col % 8 <= 3: return "Left"
        elif col % 8 <= 5: return "Down"
        else:
            return "Right"

    #  Load in specified images from the spritesheet
    def _get_specified_images(self, spritesheet, img_coord_dict, color, transparent=True):
        """Add the specified images from the spritesheet as per the coords received from image dictionary"""
        image_dictionary = {}
        for key, pos in img_coord_dict.items():
            image = self.get_image(spritesheet, pos[0], pos[1], pos[2], pos[3], color, transparent)
            image_dictionary.setdefault(key, image)
        return image_dictionary

    def get_image(self, spritesheet, xpos, ypos, width, height, color, transparent=True):
        """Get specified image from spritesheet"""
        surface = pygame.Surface((width, height))
        surface.fill(color)
        surface.blit(spritesheet, (0, 0), (xpos, ypos, width, height))
        if transparent:
            surface.set_colorkey(color)
        surface = self.scale_image(surface, gc.spriteScale)
        return surface

    #  Loading individual images
    def load_ind_img(self, path, scale=False, size=(0, 0)):
        """Loading in of individual images"""
        image = pygame.image.load(f"assets/{path}.png").convert_alpha()
        if scale:
            image = pygame.transform.scale(image, size)
        return image
import pygame
import gameconfig as gc
from characters import Tank, PlayerTank, EnemyTank, SpecialTank
from game_hud import GameHud
from random import choice, shuffle, randint
from tile import BrickTile, SteelTile, ForestTile, IceTile, WaterTile
from fade_animate import Fade
from score_screen import ScoreScreen
from eagle import Eagle
from gameover import GameOver


class Game:
    def __init__(self, main, assets, player1=True, player2=False):
        """The main Game Object when playing"""
        #  Main file
        self.main = main
        self.assets = assets

        #  Object Groups
        self.groups = {"Ice_Tiles": pygame.sprite.Group(),
                       "Water_Tiles": pygame.sprite.Group(),
                       "Player_Tanks": pygame.sprite.Group(),
                       "All_Tanks": pygame.sprite.Group(),
                       "Bullets": pygame.sprite.Group(),
                       "Destructable_Tiles": pygame.sprite.Group(),
                       "Impassable_Tiles": pygame.sprite.Group(),
                       "Eagle": pygame.sprite.GroupSingle(),
                       "Explosion": pygame.sprite.Group(),
                       "Forest_Tiles": pygame.sprite.Group(),
                       "Power_Ups": pygame.sprite.Group(),
                       "Scores": pygame.sprite.Group()}

        #  Player Attributes
        self.top_score = 20000
        self.player1_active = player1
        self.player1_score = 0
        self.player2_active = player2
        self.player2_score = 0

        #  Game HUD
        self.hud = GameHud(self, self.assets)

        #  Level information
        self.level_num = 1
        self.level_complete = False
        self.level_transition_timer = None
        self.data = self.main.levels

        #  Level Fade
        self.fade = Fade(self, self.assets, 10)
        #  Stage Score Screen
        self.scoreScreen = ScoreScreen(self, self.assets)
        #  Game Over
        self.game_over_screen = GameOver(self, self.assets)

        #  Player Objects
        if self.player1_active:
            self.player1 = PlayerTank(self, self.assets, self.groups, gc.Pl1_position, "Up", "Gold", 0)
        if self.player2_active:
            self.player2 = PlayerTank(self, self.assets, self.groups, gc.Pl2_position, "Up", "Green", 0)

        #  Number of Enemy Tanks
        self.enemies = 20
        self.enemy_tank_spawn_timer = gc.TANK_SPAWNING_TIME
        self.enemy_spawn_positions = [gc.Pc1_position, gc.Pc2_position, gc.Pc3_position]

        #  Load the stage
        self.create_new_stage()

        #  Fortify Base Power
        self.fortify = False
        self.fortify_timer = pygame.time.get_ticks()

        #  Game over
        self.end_game = False
        self.game_on = False
        self.game_over = False

    def input(self):
        """Handle inputs for the game when it is running"""
        keypressed = pygame.key.get_pressed()
        if self.player1_active:
            self.player1.input(keypressed)
        if self.player2_active:
            self.player2.input(keypressed)

        #  pygame event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.main.run = False

            #  Keyboard shortcut to quit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.end_game = True

                #   if player1 Tank is active, shoot
                if event.key == pygame.K_SPACE:
                    if self.player1_active:
                        self.player1.shoot()
                #   if player2 Tank is active, shoot
                if event.key == pygame.K_RCTRL:
                    if self.player2_active:
                        self.player2.shoot()

                if event.key == pygame.K_RETURN:
                    Tank(self, self.assets, self.groups, (400, 400), "Down")
                    self.enemies -= 1

    def update(self):
        #  Update the HUD
        self.hud.update()

        if self.game_over_screen.active:
            self.game_over_screen.update()

        if self.fade.fade_active:
            self.fade.update()
            if not self.fade.fade_active:
                for tank in self.groups["All_Tanks"]:
                    tank.spawn_timer = pygame.time.get_ticks()
            return

        if not self.game_over:
            if self.player1_active and self.player2_active:
                if self.player1.game_over and self.player2.game_over and not self.game_over_screen.active:
                    self.groups["All_Tanks"].empty()
                    self.game_over = True
                    self.assets.channel_gameover_sound.play(self.assets.gameover_sound)
                    self.game_over_screen.activate()
                    return
            elif self.player1_active and not self.player2_active and not self.game_over_screen.active:
                if self.player1.game_over:
                    self.groups["All_Tanks"].empty()
                    self.game_over = True
                    self.assets.channel_gameover_sound.play(self.assets.gameover_sound)
                    self.game_over_screen.activate()
                    return
        elif self.game_over and not self.end_game and not self.game_over_screen.active:
            self.stage_transition(True)
            #self.assets.channel_gameover_sound.play(self.assets.gameover_sound)
            return

        if self.fortify:
            if pygame.time.get_ticks() - self.fortify_timer >= 10000:
                self.power_up_fortify(start=False, end=True)
                self.fortify = False

        #if self.player1_active:
        #    self.player1.update()
        #if self.player2_active:
        #    self.player2.update()
        for dictKey in self.groups.keys():
            if dictKey == "Player_Tanks":
                continue
            for item in self.groups[dictKey]:
                item.update()

        self.spawn_enemy_tanks()

        for tank in self.groups["All_Tanks"]:
            if tank.enemy == True and tank.spawning == False:
                self.assets.channel_enemy_movement_sound.play(self.assets.enemy_movement_sound)
                break

        #  Check to see if stage enemies have all been killed
        if self.enemies_killed <= 0 and self.level_complete == False:
            self.level_complete = True
            self.level_transition_timer = pygame.time.get_ticks()

        #  Stage Complete, load next stage
        if self.level_complete:
            if pygame.time.get_ticks() - self.level_transition_timer >= gc.TRANSITION_TIMER:
                self.stage_transition(False)
                #self.level_num += 1
                #self.create_new_stage()

    def draw(self, window):
        """Drawing to the screen"""
        #  Draw HUD
        self.hud.draw(window)

        if self.scoreScreen.active:
            self.scoreScreen.draw(window)
            return
        #if self.player1_active:
        #    self.player1.draw(window)
        #if self.player2_active:
        #    self.player2.draw(window)
        for dictKey in self.groups.keys():
            if dictKey == "Impassable_Tiles":
                continue
            if self.fade.fade_active == True and (dictKey == "All_Tanks" or dictKey == "Player_Tanks"):
                continue
            for item in self.groups[dictKey]:
                item.draw(window)

        if self.fade.fade_active:
            self.fade.draw(window)

        if self.game_over_screen.active:
            self.game_over_screen.draw(window)

    def create_new_stage(self):
        #  Reset the various sprite groups back to Zero
        for key, value in self.groups.items():
            if key == "Player_Tanks":
                continue
            value.empty()

        #  Retrieves the specific level data
        self.current_level_data = self.data.level_data[self.level_num-1]

        #  Number of enemy tanks to spawn in the stage, and this is tracked back to Zero
        #self.enemies = choice([16, 17, 18, 19, 20])
        self.enemies = 5

        #  Track the number of enemies killed back down to zero
        self.enemies_killed = self.enemies

        #  Load in the level Data
        self.load_level_data(self.current_level_data)
        self.eagle = Eagle(self, self.assets, self.groups)
        self.level_complete = False

        self.assets.game_start_sound.play()

        self.fade.level = self.level_num
        self.fade.stage_image = self.fade.create_stage_image()
        self.fade.fade_active = True

        #  Generating the spawn queue for the computer tanks
        self.generate_spawn_queue()
        self.spawn_pos_index = 0
        self.spawn_queue_index = 0
        print(self.spawn_queue)

        if self.player1_active:
            self.player1.new_stage_spawn(gc.Pl1_position)
        if self.player2_active:
            self.player2.new_stage_spawn(gc.Pl2_position)

    def load_level_data(self, level):
        """Load the level Data"""
        self.grid = []
        for i, row in enumerate(level):
            line = []
            for j, tile in enumerate(row):
                pos = (gc.SCREEN_BORDER_LEFT + (j * gc.imageSize // 2),
                       gc.SCREEN_BORDER_TOP + (i * gc.imageSize // 2))
                if int(tile) < 0:
                    line.append("   ")
                elif int(tile) == 432:
                    line.append(f"{tile}")
                    map_tile = BrickTile(pos, self.groups["Destructable_Tiles"], self.assets.brick_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 482:
                    line.append(f"{tile}")
                    map_tile = SteelTile(pos, self.groups["Destructable_Tiles"], self.assets.steel_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                elif int(tile) == 483:
                    line.append(f"{tile}")
                    map_tile = ForestTile(pos, self.groups["Forest_Tiles"], self.assets.forest_tiles)
                elif int(tile) == 484:
                    line.append(f"{tile}")
                    map_tile = IceTile(pos, self.groups["Ice_Tiles"], self.assets.ice_tiles)
                elif int(tile) == 533:
                    line.append(f"{tile}")
                    map_tile = WaterTile(pos, self.groups["Water_Tiles"], self.assets.water_tiles)
                    self.groups["Impassable_Tiles"].add(map_tile)
                else:
                    line.append(f"{tile}")
            self.grid.append(line)
        #for row in self.grid:
        #    print(row)

    def generate_spawn_queue(self):
        """Generate a list of tanks that will be spawning during the level"""
        self.spawn_queue_ratios = gc.Tank_spawn_queue[f"queue_{str((self.level_num - 1 % 36) // 3)}"]
        self.spawn_queue = []

        for lvl, ratio in enumerate(self.spawn_queue_ratios):
            for i in range(int(round(self.enemies * (ratio / 100)))):
                self.spawn_queue.append(f"level_{lvl}")
        shuffle(self.spawn_queue)

    def spawn_enemy_tanks(self):
        """Spawn enemy tanks, each tank spawns as per the queue"""
        if self.enemies == 0:
            return
        if pygame.time.get_ticks() - self.enemy_tank_spawn_timer >= gc.TANK_SPAWNING_TIME:
            position = self.enemy_spawn_positions[self.spawn_pos_index % 3]
            tank_level = gc.Tank_Criteria[self.spawn_queue[self.spawn_queue_index % len(self.spawn_queue)]]["image"]
            special_tank = randint(1, len(self.spawn_queue))
            #SpecialTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level)
            if special_tank == self.spawn_queue_index:
                SpecialTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level)
            else:
                EnemyTank(self, self.assets, self.groups, position, "Down", "Silver", tank_level)
            #  Reset the enemy tank spawn timer
            self.enemy_tank_spawn_timer = pygame.time.get_ticks()
            self.spawn_pos_index += 1
            self.spawn_queue_index += 1
            self.enemies -= 1

    def stage_transition(self, game_over=False):
        if not self.scoreScreen.active:
            self.scoreScreen.timer = pygame.time.get_ticks()
            if self.player1_active:
                self.scoreScreen.p1_score = self.player1_score
                self.scoreScreen.p1_kill_list = sorted(self.player1.score_list)
            if self.player2_active:
                self.scoreScreen.p2_score = self.player2_score
                self.scoreScreen.p2_kill_list = sorted(self.player2.score_list)
            self.scoreScreen.update_basic_info(self.top_score, self.level_num)
        self.scoreScreen.active = True
        self.scoreScreen.update(game_over)

    def change_level(self, p1_score, p2_score):
        self.level_num += 1
        self.level_num = self.level_num % len(self.data.level_data)
        self.player1_score = p1_score
        self.player2_score = p2_score
        self.create_new_stage()

    def power_up_fortify(self, start=True, end=False):
        off_x, off_y = gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_TOP
        positions = [
            (off_x + gc.imageSize // 2 * 11, off_y + gc.imageSize // 2 * 25),
            (off_x + gc.imageSize // 2 * 11, off_y + gc.imageSize // 2 * 24),
            (off_x + gc.imageSize // 2 * 11, off_y + gc.imageSize // 2 * 23),
            (off_x + gc.imageSize // 2 * 12, off_y + gc.imageSize // 2 * 23),
            (off_x + gc.imageSize // 2 * 13, off_y + gc.imageSize // 2 * 23),
            (off_x + gc.imageSize // 2 * 14, off_y + gc.imageSize // 2 * 23),
            (off_x + gc.imageSize // 2 * 14, off_y + gc.imageSize // 2 * 24),
            (off_x + gc.imageSize // 2 * 14, off_y + gc.imageSize // 2 * 25),
        ]
        if start:
            for pos in positions:
                pos_rect = pygame.rect.Rect(pos[0], pos[1], gc.imageSize//2, gc.imageSize//2)
                for rectangle in self.groups["Impassable_Tiles"]:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()
                map_tile = SteelTile(pos, self.groups["Destructable_Tiles"], self.assets.steel_tiles)
                self.groups["Impassable_Tiles"].add(map_tile)
        elif end:
            for pos in positions:
                pos_rect = pygame.rect.Rect(pos[0], pos[1], gc.imageSize // 2, gc.imageSize // 2)
                for rectangle in self.groups["Impassable_Tiles"]:
                    if rectangle.rect.colliderect(pos_rect):
                        rectangle.kill()
                map_tile = BrickTile(pos, self.groups["Destructable_Tiles"], self.assets.brick_tiles)
                self.groups["Impassable_Tiles"].add(map_tile)
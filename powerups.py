import pygame
import random
import gameconfig as gc
from scores import ScoreBanner


class PowerUps(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups):
        super().__init__()
        self.game = game
        self.assets = assets
        self.powerup_images = self.assets.power_up_images

        self.groups = groups
        self.groups["Power_Ups"].add(self)

        self.power_up = self.randomly_select_power_up()
        #self.power_up = "fortify"
        self.power_up_timer = pygame.time.get_ticks()

        self.xPos = random.randint(gc.SCREEN_BORDER_LEFT, gc.SCREEN_BORDER_RIGHT - gc.imageSize)
        self.yPos = random.randint(gc.SCREEN_BORDER_TOP, gc.SCREEN_BORDER_BOTTOM - gc.imageSize)

        self.image = self.powerup_images[self.power_up]
        self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos))

    def randomly_select_power_up(self):
        """Randomly select a power up ability"""
        powerups = list(gc.POWER_UPS.keys())
        selected_powerup = random.choice(powerups)
        return selected_powerup

    def power_up_collected(self):
        ScoreBanner(self.assets, self.groups, self.rect.center, "500")
        self.assets.channel_bonus_sound.play(self.assets.bonus_sound)
        self.kill()

    def shield(self, player):
        """The player tank is protected by a shield for a certain amount of time."""
        player.shield_start = True

    def freeze(self):
        """Freeze all of the currently spawned enemy tanks"""
        for tank in self.groups["All_Tanks"]:
            if tank.enemy:
                tank.paralyze_tank(5000)

    def explosion(self, player):
        """Destroys all enemy Tanks currently spawned"""
        for tank in self.groups["All_Tanks"]:
            if tank.enemy:
                score = tank.score
                player.score_list.append(score)
                tank.destroy_tank()

    def extra_life(self, player):
        """Give the player an extra life"""
        player.lives += 1

    def power(self, player):
        """Increase the bullet speed, and when speed reaches 1.5, increase the bullet limit by 1"""
        player.bullet_speed_modifier += 0.1
        if player.bullet_speed_modifier > 1.5:
            player.bullet_speed_modifier = 1
            player.bullet_limit += 1
        player.bullet_speed = gc.TANK_SPEED * (3 * player.bullet_speed_modifier)

    def special(self, player):
        """Upgrade the3 tank level
        Level 2 - Shot power increased to 2, can destroy a block of bricks in 1 shot
        Level 3 - Shot power increased to 3, can destroy a block of steel in 1 shot
        Level 4 - Tank health increased by 1
        Level 5 and up - Tank becomes amphibious"""
        if player.power >= 4:
            player.amphibious = True
            return
        player.power += 1
        player.tank_level += 1
        if player.tank_level >= 3:
            player.tank_level = 3
            player.tank_health += 1
        player.image = player.tank_images[f"Tank_{player.tank_level}"][player.colour][player.direction][
            player.frame_index]
        player.mask_dict = player.get_various_masks()
        player.mask = player.mask_dict[player.direction]

    def fortify(self):
        """Fortify the Base"""
        self.game.fortify = True
        self.game.fortify_timer = pygame.time.get_ticks()
        self.game.power_up_fortify()

    def update(self):
        if pygame.time.get_ticks() - self.power_up_timer >= 5000:
            self.kill()
        player_tank = pygame.sprite.spritecollideany(self, self.groups["Player_Tanks"])
        if player_tank:
            if player_tank.colour == "Gold":
                self.game.player1_score += 500
            elif player_tank.colour == "Green":
                self.game.player2_score += 500

            if self.power_up == "shield":
                self.shield(player_tank)
            elif self.power_up == "freeze":
                self.freeze()
            elif self.power_up == "explosion":
                self.explosion(player_tank)
            elif self.power_up == "extra_life":
                self.extra_life(player_tank)
            elif self.power_up == "power":
                self.power(player_tank)
            elif self.power_up == "special":
                self.special(player_tank)
            elif self.power_up == "fortify":
                self.fortify()
            print(self.power_up)
            self.power_up_collected()

    def draw(self, window):
        window.blit(self.image, self.rect)
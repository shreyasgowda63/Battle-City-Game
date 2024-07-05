import pygame
from ammunition import Bullet
from explosions import Explosion
from powerups import PowerUps
import random
import gameconfig as gc


class MyRect(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = None
        self.rect = pygame.Rect(x, y, width, height)

class Tank(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups, position, direction, enemy=True, colour="Silver", tank_level=0):
        super().__init__()
        #  Game Object and Assets
        self.game = game
        self.assets = assets
        self.groups = groups

        #  Sprite groups that may interact with tank
        self.tank_group = self.groups["All_Tanks"]
        self.player_group = self.groups["Player_Tanks"]

        #  Add tank object to the sprite group
        self.tank_group.add(self)

        #  Enemy Tank Criteria Dict
        levels = {0: None, 4: "level_0", 5: "level_1", 6: "level_2", 7: "level_3"}
        self.level = levels[tank_level]

        #  Tank Images
        self.tank_images = self.assets.tank_images
        self.spawn_images = self.assets.spawn_star_images

        #  Tank Position and Direction
        self.spawn_pos = position
        self.xPos, self.yPos = self.spawn_pos
        self.direction = direction

        #  Tank Spawning / Active
        self.spawning = True
        self.active = False

        #  Common Tank Attributes
        self.tank_level = tank_level
        self.colour = colour
        self.tank_speed = gc.TANK_SPEED if not self.level else gc.TANK_SPEED * gc.Tank_Criteria[self.level]["speed"]
        self.power = 1 if not self.level else gc.Tank_Criteria[self.level]["power"]
        self.bullet_speed_modifier = 1
        self.bullet_speed = gc.TANK_SPEED * (3 * self.bullet_speed_modifier)
        self.score = 100 if not self.level else gc.Tank_Criteria[self.level]["score"]
        self.enemy = enemy
        self.tank_health = 1 if not self.level else gc.Tank_Criteria[self.level]["health"]

        #  Tank Image, Rectangle, and Frame Index
        self.frame_index = 0
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))
        self.width, self.height = self.image.get_size()

        #  Shoot Cooldowns and Bullet Totals
        self.bullet_limit = 1
        self.bullet_sum = 0
        self.shot_cooldown_time = 500
        self.shot_cooldown = pygame.time.get_ticks()

        #  Tank paralysis
        self.paralyzed = False
        self.paralysis = gc.TANK_PARALYSIS
        self.paralysis_timer = pygame.time.get_ticks()

        #  Amphibious
        self.amphibious = False

        #  Spawn images
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_timer = pygame.time.get_ticks() # Overall spawn timer
        self.spawn_anim_timer = pygame.time.get_ticks()  # Spawn star anim timer

        #  Tank Image Mask Dictionary
        self.mask_dict = self.get_various_masks()
        self.mask = self.mask_dict[self.direction]
        #self.mask_image = self.mask.to_surface()
        self.mask_direction = self.direction

    def input(self):
        pass

    def update(self):
        #  Update the spawning animations
        if self.spawning:
            #  Update the spawning star animations, if the required amount of time has passed.
            if pygame.time.get_ticks() - self.spawn_anim_timer >= 50:
                self.spawn_animation()
            #  if total spawn timer seconds passed, change self.spawning.

            if pygame.time.get_ticks() - self.spawn_timer > 2000:
                colliding_sprites = pygame.sprite.spritecollide(self, self.tank_group, False)
                if len(colliding_sprites) == 1:
                    self.frame_index = 0
                    self.spawning = False
                    self.active = True
                else:
                    self.spawn_star_collision(colliding_sprites)
            return

        if self.paralyzed:
            if pygame.time.get_ticks() - self.paralysis_timer >= self.paralysis:
                self.paralyzed = False

    def draw(self, window):
        #  if tank is spawning in, draw the spawn star
        if self.spawning:
            window.blit(self.spawn_image, self.rect)

        #  If the tank is set to active, draw to screen
        if self.active:
            window.blit(self.image, self.rect)
            #window.blit(self.mask_image, self.rect)
            pygame.draw.rect(window, gc.RED, self.rect, 1)

    #  Tank movement
    def grid_alignment_movement(self, pos):
        if pos % (gc.imageSize//2) != 0:
            if pos % (gc.imageSize // 2) < gc.imageSize // 4:
                pos -= (pos % (gc.imageSize // 4))
            elif pos % (gc.imageSize // 2) > gc.imageSize // 4:
                pos += (gc.imageSize//4) - (pos % (gc.imageSize//4))
            else:
                return pos
        return pos

    def move_tank(self, direction):
        """Move the tank in the passed direction"""
        if self.spawning:
            return

        self.direction = direction

        if self.paralyzed:
            self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
            return

        if direction == "Up":
            self.yPos -= self.tank_speed
            self.xPos = self.grid_alignment_movement(self.xPos)
            if self.yPos < gc.SCREEN_BORDER_TOP:
                self.yPos = gc.SCREEN_BORDER_TOP
        elif direction == "Down":
            self.yPos += self.tank_speed
            self.xPos = self.grid_alignment_movement(self.xPos)
            if self.yPos + self.height > gc.SCREEN_BORDER_BOTTOM:
                self.yPos = gc.SCREEN_BORDER_BOTTOM - self.height
        elif direction == "Left":
            self.xPos -= self.tank_speed
            self.yPos = self.grid_alignment_movement(self.yPos)
            if self.xPos < gc.SCREEN_BORDER_LEFT:
                self.xPos = gc.SCREEN_BORDER_LEFT
        elif direction == "Right":
            self.xPos += self.tank_speed
            self.yPos = self.grid_alignment_movement(self.yPos)
            if self.xPos + self.width > gc.SCREEN_BORDER_RIGHT:
                self.xPos = gc.SCREEN_BORDER_RIGHT - self.width

        #  Update the Tank Rectangle Position
        self.rect.topleft = (self.xPos, self.yPos)
        #  Update the Tank Animation
        self.tank_movement_animation()
        #  Check for tank collisions with other tanks
        self.tank_on_tank_collisions()
        #  Check for tank collisions with obstacles
        self.tank_collisions_with_obstacles()
        #  Check for tank collision with Base
        self.base_collision()

    #  Tank Animations
    def tank_movement_animation(self):
        """update the animation images to simulate the tank moving"""
        self.frame_index += 1
        imagelistlength = len(self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction])
        self.frame_index = self.frame_index % imagelistlength
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        if self.mask_direction != self.direction:
            self.mask_direction = self.direction
            self.mask = self.mask_dict[self.mask_direction]
            #self.mask_image = self.mask.to_surface()

    def spawn_animation(self):
        """Cycle through the spawn star images to simulate a spawning icon"""
        self.frame_index += 1
        self.frame_index = self.frame_index % len(self.spawn_images)
        self.spawn_image = self.spawn_images[f"star_{self.frame_index}"]
        self.spawn_anim_timer = pygame.time.get_ticks()

    def get_various_masks(self):
        """Creates and returns a dictionary of masks for all directions"""
        images = {}
        for direction in ["Up", "Down", "Left", "Right"]:
            image_to_mask = self.tank_images[f"Tank_{self.tank_level}"][self.colour][direction][0]
            images.setdefault(direction, pygame.mask.from_surface(image_to_mask))
        return images

    #  Tank Collisions
    def tank_on_tank_collisions(self):
        """Check if the tank collides with another tank"""
        tank_collision = pygame.sprite.spritecollide(self, self.tank_group, False)
        if len(tank_collision) == 1:
            return

        for tank in tank_collision:
            #  Skip the tank if it is the current object
            if tank == self or tank.spawning == True:
                continue

            if self.direction == "Right":
                if self.rect.right >= tank.rect.left and \
                    self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.right = tank.rect.left
                    self.xPos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= tank.rect.right and \
                    self.rect.bottom > tank.rect.top and self.rect.top < tank.rect.bottom:
                    self.rect.left = tank.rect.right
                    self.xPos = self.rect.x
            elif self.direction == "Up":
                if self.rect.top <= tank.rect.bottom and \
                    self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.top = tank.rect.bottom
                    self.yPos = self.rect.y
            elif self.direction == "Down":
                if self.rect.bottom >= tank.rect.top and \
                    self.rect.left < tank.rect.right and self.rect.right > tank.rect.left:
                    self.rect.bottom = tank.rect.top
                    self.yPos = self.rect.y

    def tank_collisions_with_obstacles(self):
        """Perform collision checks with tank and obstacles"""
        wall_collision = pygame.sprite.spritecollide(self, self.groups["Impassable_Tiles"], False)
        for obstacle in wall_collision:
            if obstacle in self.groups["Water_Tiles"] and self.amphibious == True:
                continue
            if self.direction == "Right":
                if self.rect.right >= obstacle.rect.left:
                    self.rect.right = obstacle.rect.left
                    self.xPos = self.rect.x
            elif self.direction == "Left":
                if self.rect.left <= obstacle.rect.right:
                    self.rect.left = obstacle.rect.right
                    self.xPos = self.rect.x
            elif self.direction == "Down":
                if self.rect.bottom >= obstacle.rect.top:
                    self.rect.bottom = obstacle.rect.top
                    self.yPos = self.rect.y
            elif self.direction == "Up":
                if self.rect.top <= obstacle.rect.bottom:
                    self.rect.top = obstacle.rect.bottom
                    self.yPos = self.rect.y

    def spawn_star_collision(self, colliding_sprites):
        """Fixes infinite spawn bug if two spawn stars are colliding"""
        for tank in colliding_sprites:
            if tank.active:
                return
        for tank in colliding_sprites:
            if tank == self:
                continue
            if self.spawning and tank.spawning:
                self.frame_index = 0
                self.spawning = False
                self.active = True

    def base_collision(self):
        """If base is driven over by a tank"""
        if not self.groups["Eagle"].sprite.active:
            return
        if self.rect.colliderect(self.groups["Eagle"].sprite.rect):
            self.groups["Eagle"].sprite.destroy_base()

    #  Tank Shooting
    def shoot(self):
        if self.bullet_sum >= self.bullet_limit:
            return

        bullet = Bullet(self.groups, self, self.rect.center, self.direction, self.assets)
        self.assets.channel_fire_sound.play(self.assets.fire_sound)
        self.bullet_sum += 1

    #  Actions affecting tanks
    def paralyze_tank(self, paralysis_time):
        """If player tank is hit by player tank, or if the freeze power up is used"""
        self.paralysis = paralysis_time
        self.paralyzed = True
        self.paralysis_timer = pygame.time.get_ticks()

    def destroy_tank(self):
        """Method to damage a tanks health, and if health at zero, destroy the tank"""
        self.tank_health -= 1
        #  If health reaches zero, destroy tank
        if self.tank_health <= 0:
            self.kill()
            Explosion(self.assets, self.groups, self.rect.center, 5, self.score)
            self.assets.channel_explosion_sound.play(self.assets.explosion_sound)
            self.game.enemies_killed -= 1
            return

        if self.tank_health == 3:
            self.colour = "Green"
        elif self.tank_health == 2:
            self.colour = "Gold"
        elif self.tank_health == 1:
            self.colour = "Silver"

class PlayerTank(Tank):
    def __init__(self, game, assets, groups, position, direction, colour, tank_level):
        super().__init__(game, assets, groups, position, direction, False, colour, tank_level)
        self.player_group.add(self)
        #  Player Lives
        self.lives = 1
        #  Player Dead / Game Over
        self.dead = False
        self.game_over = False
        #  Level Score Tracking
        self.score_list = []


        #  Shield
        self.shield_start = True
        self.shield = False
        self.shield_time_limit = 5000
        self.shield_timer = pygame.time.get_ticks()
        self.shield_images = self.assets.shield_images
        self.shield_img_index = 0
        self.shield_anim_timer = pygame.time.get_ticks()
        self.shield_image = self.shield_images[f"shield_{self.shield_img_index + 1}"]
        self.shield_image_rect = self.shield_image.get_rect(topleft=(self.rect.topleft))

        self.movement_sound = self.assets.movement_sound
        self.player_movement_channel = pygame.mixer.Channel(0)

    def input(self, keypressed):
        """Move the player tanks"""
        if self.game_over or self.dead:
            return
        if self.colour == "Gold":
            if keypressed[pygame.K_w]:
                self.move_tank("Up")
            elif keypressed[pygame.K_s]:
                self.move_tank("Down")
            elif keypressed[pygame.K_a]:
                self.move_tank("Left")
            elif keypressed[pygame.K_d]:
                self.move_tank("Right")

        if self.colour == "Green":
            if keypressed[pygame.K_UP]:
                self.move_tank("Up")
            elif keypressed[pygame.K_DOWN]:
                self.move_tank("Down")
            elif keypressed[pygame.K_LEFT]:
                self.move_tank("Left")
            elif keypressed[pygame.K_RIGHT]:
                self.move_tank("Right")

    def update(self):
        if self.game_over:
            return
        #  Tank is done spawning in, startup shield must be activated
        if not self.spawning:
            if self.shield_start:
                self.shield_timer = pygame.time.get_ticks()
                self.shield_start = False
                self.shield = True
            #  Shield is currently active, shield image animations
            if self.shield:
                if pygame.time.get_ticks() - self.shield_anim_timer >= 50:
                    self.shield_img_index += 1
                    self.shield_anim_timer = pygame.time.get_ticks()
                self.shield_img_index = self.shield_img_index % 2
                self.shield_image = self.shield_images[f"shield_{self.shield_img_index + 1}"]
                self.shield_image_rect.topleft = self.rect.topleft
                #  Check if the shield timer has run out
                if pygame.time.get_ticks() - self.shield_time_limit >= self.shield_timer:
                    self.shield = False
        super().update()

    def draw(self, window):
        if self.game_over:
            return
        super().draw(window)
        if self.shield and not self.spawning:
            window.blit(self.shield_image, self.shield_image_rect)

    def move_tank(self, direction):
        if self.spawning:
            return
        self.player_movement_channel.play(self.movement_sound)
        super().move_tank(direction)

    def shoot(self):
        if self.game_over:
            return
        super().shoot()

    def destroy_tank(self):
        if self.shield:
            return
        if self.dead or self.game_over:
            return
        if self.tank_health > 1:
            self.tank_health = 1
            self.tank_level = 0
            self.power = 1
            self.amphibious = False
            self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
            self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos))
            self.mask_dict = self.get_various_masks()
            self.mask = self.mask_dict[self.direction]
            return
        Explosion(self.assets, self.groups, self.rect.center, 5, 0)
        self.assets.channel_explosion_sound.play(self.assets.explosion_sound)
        self.dead = True
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
        self.respawn_tank()

    def new_stage_spawn(self, spawn_pos):
        self.tank_group.add(self)
        self.spawning = True
        self.active = False
        self.shield_start = True
        self.direction = "Up"
        self.xPos, self.yPos = spawn_pos
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect.topleft = (self.xPos, self.yPos)
        self.score_list.clear()

    def respawn_tank(self):
        self.spawning = True
        self.active = False
        self.spawn_timer = pygame.time.get_ticks()
        self.shield_start = True
        self.direction = "Up"
        self.tank_level = 0
        self.power = 1
        self.amphibious = False
        self.bullet_speed_modifier = 1
        self.bullet_speed = gc.TANK_SPEED * (3 * self.bullet_speed_modifier)
        self.bullet_limit = 1
        self.xPos, self.yPos = self.spawn_pos
        self.image = self.tank_images[f"Tank_{self.tank_level}"][self.colour][self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.spawn_pos))
        self.mask_dict = self.get_various_masks()
        self.mask = self.mask_dict[self.direction]
        self.dead = False

class EnemyTank(Tank):
    def __init__(self, game, assets, groups, pos, dir, colour, tank_lvl):
        super().__init__(game, assets, groups, pos, dir, True, colour, tank_lvl)
        self.time_between_shots = random.choice([300, 600, 900])
        self.shot_timer = pygame.time.get_ticks()

        self.dir_rec = {
            "Left": MyRect(self.xPos - (self.width//2), self.yPos, self.width//2, self.height),
            "Right": MyRect(self.xPos + self.width, self.yPos, self.width//2, self.height),
            "Up": MyRect(self.xPos, self.yPos - (self.height//2), self.width, self.height//2),
            "Down": MyRect(self.xPos, self.yPos + self.height, self.width, self.height//2)
        }

        self.move_directions = []
        self.change_direction_timer = pygame.time.get_ticks()
        self.game_screen_rect = MyRect(gc.GAME_SCREEN[0], gc.GAME_SCREEN[1], gc.GAME_SCREEN[2], gc.GAME_SCREEN[3])

    def ai_shooting(self):
        if self.paralyzed:
            return
        if self.bullet_sum < self.bullet_limit:
            if pygame.time.get_ticks() - self.shot_timer >= self.time_between_shots:
                self.shoot()
                self.shot_timer = pygame.time.get_ticks()

    def ai_move(self, direction):
        super().move_tank(direction)
        self.dir_rec["Left"].rect.update(self.xPos - (self.width//2), self.yPos, self.width//2, self.height)
        self.dir_rec["Right"].rect.update(self.xPos + self.width, self.yPos, self.width//2, self.height)
        self.dir_rec["Up"].rect.update(self.xPos, self.yPos - (self.height//2), self.width, self.height//2)
        self.dir_rec["Down"].rect.update(self.xPos, self.yPos + self.height, self.width, self.height//2)

    def ai_move_direction(self):
        directional_list_copy = self.move_directions.copy()
        if pygame.time.get_ticks() - self.change_direction_timer <= 750:
            return

        for key, value in self.dir_rec.items():
            #  Check to make sure the retangle is Within the game screen
            if pygame.Rect.contains(self.game_screen_rect.rect, value):
                #  Check for any collision with impassable tiles
                obst = pygame.sprite.spritecollideany(value, self.groups["Impassable_Tiles"])
                if not obst:
                    #  Check if direction is already in directions list
                    if key not in directional_list_copy:
                        directional_list_copy.append(key)
                elif obst:
                    #  If there is collision, check that rect is contained by obstacle
                    if value.rect.contains(obst.rect) and key in directional_list_copy:
                        directional_list_copy.remove(key)
                    else:
                        if key in directional_list_copy and key != self.direction:
                            directional_list_copy.remove(key)

                tank = pygame.sprite.spritecollideany(value, self.groups["All_Tanks"])
                if tank:
                    if key in directional_list_copy:
                        directional_list_copy.remove(key)
            else:
                if key in directional_list_copy:
                    directional_list_copy.remove(key)

        if self.move_directions != directional_list_copy or (self.direction not in directional_list_copy):
            self.move_directions = directional_list_copy.copy()
            if len(self.move_directions) > 0:
                self.direction = random.choice(self.move_directions)
            self.change_direction_timer = pygame.time.get_ticks()

    def update(self):
        super().update()
        if self.spawning:
            return
        self.ai_move(self.direction)
        self.ai_move_direction()
        self.ai_shooting()

    def draw(self, window):
        super().draw(window)
        for value in self.dir_rec.values():
            pygame.draw.rect(window, gc.GREEN, value.rect, 2)

class SpecialTank(EnemyTank):
    def __init__(self, game, assets, groups, pos, dir, colour, tank_lvl):
        super().__init__(game, assets, groups, pos, dir, colour, tank_lvl)
        self.colour_swap_timer = pygame.time.get_ticks()
        self.special = True

    def update(self):
        """Cause the flashing style to represent a special tank"""
        super().update()
        if self.special:
            if pygame.time.get_ticks() - self.colour_swap_timer >= 100:
                self.colour = "Special" if self.colour == "Silver" else "Silver"
                self.colour_swap_timer = pygame.time.get_ticks()

    def destroy_tank(self):
        if self.special:
            self.special = False
            #  Generate the special power up
            print("Power Up Activated")
            PowerUps(self.game, self.assets, self.groups)
        super().destroy_tank()
import pygame
from explosions import Explosion
import gameconfig as gc


class Eagle(pygame.sprite.Sprite):
    def __init__(self, game, assets, groups):
        super().__init__()
        self.game = game
        self.assets = assets
        self.group = groups
        self.group["Eagle"].add(self)

        self.active = True
        self.timer = pygame.time.get_ticks()

        self.image = self.assets.flag["Phoenix_Alive"]
        self.rect = self.image.get_rect(topleft=(gc.FLAG_POSITION))

    def update(self):
        if not self.active and (pygame.time.get_ticks() - self.timer >= 750):
            if self.game.player1_active:
                self.game.player1.game_over = True
            if self.game.player2_active:
                self.game.player2.game_over = True

    def draw(self, window):
        window.blit(self.image, self.rect)

    def destroy_base(self):
        """Sets this object to be inactive"""
        self.active = False
        self.image = self.assets.flag["Phoenix_Destroyed"]
        Explosion(self.assets, self.group, self.rect.center, 5, 0)
        self.assets.channel_explosion_sound.play(self.assets.explosion_sound)
        self.timer = pygame.time.get_ticks()
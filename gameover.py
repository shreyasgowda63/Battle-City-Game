import pygame
import gameconfig as gc


class GameOver:
    def __init__(self, game, assets):
        self.game = game
        self.assets = assets

        self.game_over_image = self.assets.context["game_over"]
        self.game_over_rect = self.game_over_image.get_rect()
        self.g_width, self.g_height = self.game_over_image.get_size()
        self.game_over_rect.center = (gc.SCREENWIDTH//2 - self.g_width//2, gc.SCREENHEIGHT + self.g_height)

        self.timer = pygame.time.get_ticks()
        self.active = False

    def activate(self):
        self.active = True
        self.timer = pygame.time.get_ticks()

    def update(self):
        if self.game_over_rect.y > gc.SCREENHEIGHT//4 - self.g_height//2:
            self.game_over_rect.y -= 10
        elif self.game_over_rect.y < gc.SCREENHEIGHT//4 - self.g_height//2:
            self.game_over_rect.y = gc.SCREENHEIGHT//4 - self.g_height//2
            self.timer = pygame.time.get_ticks()

        if self.game_over_rect.y == gc.SCREENHEIGHT//4 - self.g_height//2:
            if pygame.time.get_ticks() - self.timer >= 3000:
                self.active = False
                self.game.stage_transition(True)

    def draw(self, window):
        window.blit(self.game_over_image, self.game_over_rect)
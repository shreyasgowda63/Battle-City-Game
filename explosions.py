import pygame
from scores import ScoreBanner

class Explosion(pygame.sprite.Sprite):
    def __init__(self, assets, group, pos, explode_type=1, score=100):
        super().__init__()
        self.assets = assets
        self.group = group
        self.explosion_group = self.group["Explosion"]
        self.explosion_group.add(self)

        self.score = score

        self.pos = pos
        self.explode_type = explode_type
        self.frame_index = 1
        self.images = self.assets.explosions
        self.image = self.images["explode_1"]
        self.rect = self.image.get_rect(center=self.pos)

        self.anim_timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.anim_timer >= 100:
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
                if self.score == 0:
                    return
                ScoreBanner(self.assets, self.group, self.rect.center, self.score)
            if self.explode_type == 1 and self.frame_index > 3:
                self.kill()
            self.anim_timer = pygame.time.get_ticks()
            self.image = self.images[f"explode_{self.frame_index}"]
            self.rect = self.image.get_rect(center=self.pos)

    def draw(self, window):
        window.blit(self.image, self.rect)
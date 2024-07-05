import pygame

class ScoreBanner(pygame.sprite.Sprite):
    def __init__(self, assets, group, pos, score):
        super().__init__()
        self.assets = assets
        self.group = group
        self.group["Scores"].add(self)
        self.pos = pos
        self.score = str(score)

        self.images = self.assets.score
        self.image = self.images[self.score]
        self.rect = self.image.get_rect(center=self.pos)
        self.timer = pygame.time.get_ticks()

    def update(self):
        self.rect.y -= 1
        if pygame.time.get_ticks() - self.timer >= 1000:
            self.kill()

    def draw(self, window):
        window.blit(self.image, self.rect)
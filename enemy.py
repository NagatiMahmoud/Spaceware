import pygame
import random
from settings import *
from utils import load_image


class Enemy(pygame.sprite.Sprite):
    """Enemy that spawns at the top and moves downward.

    It chooses a random horizontal drift so enemies don't all follow straight lines.
    """

    def __init__(self, pos):
        super().__init__()
        self.image = load_image('enemy.png')
        if not self.image:
            self.image = pygame.Surface((36, 30), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 100, 100), (0, 0, 36, 30))
        self.rect = self.image.get_rect(center=pos)
        self.speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        # horizontal drift speed (-50..+50)
        self.drift = random.uniform(-40, 40)

    def update(self, dt):
        self.rect.y += int(self.speed * dt)
        self.rect.x += int(self.drift * dt)
        # keep inside horizontal bounds by bouncing drift
        if self.rect.left < 0:
            self.rect.left = 0
            self.drift = abs(self.drift)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.drift = -abs(self.drift)

import pygame
from settings import *
from utils import load_image


class Bullet(pygame.sprite.Sprite):
    """Simple bullet moving upward."""

    def __init__(self, pos):
        super().__init__()
        self.image = load_image('bullet.png')
        if not self.image:
            self.image = pygame.Surface((4, 12), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 255, 100), (0, 0, 4, 12))
        self.rect = self.image.get_rect(center=pos)
        self.speed = BULLET_SPEED

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

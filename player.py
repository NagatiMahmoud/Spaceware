import pygame
from settings import *
from bullet import Bullet
from utils import load_image


class Player(pygame.sprite.Sprite):
    """Player spaceship sprite.

    Methods:
    - move(direction, dt): move left (-1) or right (+1)
    - shoot(): return a Bullet instance
    - reset(): restore lives and position
    """

    def __init__(self, pos):
        super().__init__()
        self.image = load_image('player.png')
        if not self.image:
            # fallback: simple triangle
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (120, 200, 255), [(20, 0), (0, 40), (40, 40)])
        self.rect = self.image.get_rect(center=pos)
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES

    def move(self, direction, dt):
        """Move the player horizontally.

        direction: -1 (left) or +1 (right)
        dt: seconds since last frame
        """
        self.rect.x += int(direction * self.speed * dt)
        # clamp inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        """Create and return a Bullet starting from the player's nose."""
        x = self.rect.centerx
        y = self.rect.top - 8
        return Bullet((x, y))

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT - 80)
        self.lives = PLAYER_LIVES

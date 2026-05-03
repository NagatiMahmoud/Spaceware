import os
import pygame
from settings import IMAGES_DIR, SOUNDS_DIR


def load_image(name):
    """Load an image from the assets images folder.

    Returns a pygame.Surface or None if not found. This lets the game fall back
    to simple shapes for beginner friendliness.
    """
    path = os.path.join(IMAGES_DIR, name)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, image.get_rect().size)
    except Exception:
        return None


def load_sound(name):
    """Try to load a sound; return Sound or None on failure."""
    path = os.path.join(SOUNDS_DIR, name)
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None


def draw_text(surface, text, size, x, y, color=(255, 255, 255), align='center'):
    """Draw text centered (or top-left) on the surface."""
    font = pygame.font.SysFont('arial', size)
    surf = font.render(str(text), True, color)
    rect = surf.get_rect()
    if align == 'center':
        rect.center = (x, y)
    elif align == 'topleft':
        rect.topleft = (x, y)
    surface.blit(surf, rect)

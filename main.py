import pygame
import sys
import random
from pygame.locals import QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE, K_RETURN

from settings import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from utils import load_image, load_sound, draw_text


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Try to load background image, else use plain color
    background = load_image('background.png')

    # Sounds (optional)
    shoot_sound = load_sound('shoot.wav')
    explosion_sound = load_sound('explosion.wav')
    music = None
    try:
        music = 'assets/sounds/music.ogg'
        pygame.mixer.music.load(music)
        pygame.mixer.music.set_volume(0.4)
    except Exception:
        music = None

    # Game states: 'START', 'PLAYING', 'GAMEOVER'
    state = 'START'

    # Sprites groups
    player = Player((WIDTH // 2, HEIGHT - 80))
    player_group = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    score = 0
    enemy_timer = 0
    enemy_spawn_delay = ENEMY_SPAWN_DELAY
    difficulty_timer = 0

    explosions = []  # simple explosion effects as dicts

    if music:
        pygame.mixer.music.play(-1)

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit(); sys.exit()

                if state == 'START' and event.key == K_RETURN:
                    # start game
                    state = 'PLAYING'
                    score = 0
                    enemies.empty(); bullets.empty(); explosions.clear()
                    player.reset()
                    enemy_spawn_delay = ENEMY_SPAWN_DELAY
                    enemy_timer = 0
                    difficulty_timer = 0

                if state == 'GAMEOVER' and event.key == K_RETURN:
                    state = 'PLAYING'
                    score = 0
                    enemies.empty(); bullets.empty(); explosions.clear()
                    player.reset()
                    enemy_spawn_delay = ENEMY_SPAWN_DELAY
                    enemy_timer = 0
                    difficulty_timer = 0

                if state == 'PLAYING' and event.key == K_SPACE:
                    # player shoots
                    b = player.shoot()
                    if b:
                        bullets.add(b)
                        if shoot_sound:
                            shoot_sound.play()

        keys = pygame.key.get_pressed()

        if state == 'PLAYING':
            # update player movement
            if keys[K_LEFT]:
                player.move(-1, dt)
            if keys[K_RIGHT]:
                player.move(1, dt)

            # spawn enemies over time with increasing difficulty
            enemy_timer += dt
            difficulty_timer += dt
            if enemy_timer >= enemy_spawn_delay:
                enemy_timer = 0
                # spawn enemy at random x at top
                x = random.randint(20, WIDTH - 20)
                e = Enemy((x, -40))
                enemies.add(e)

            # increase difficulty gradually
            if difficulty_timer >= 5.0 and enemy_spawn_delay > 0.25:
                difficulty_timer = 0
                enemy_spawn_delay = max(0.25, enemy_spawn_delay - 0.1)

            # update sprites
            player_group.update(dt)
            bullets.update(dt)
            enemies.update(dt)

            # collisions: bullets vs enemies
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                score += 10
                explosions.append({'pos': hit.rect.center, 'timer': 0})
                if explosion_sound:
                    explosion_sound.play()

            # collisions: enemies vs player
            if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_rect):
                player.lives -= 1
                explosions.append({'pos': player.rect.center, 'timer': 0})
                if explosion_sound:
                    explosion_sound.play()
                if player.lives <= 0:
                    state = 'GAMEOVER'

            # cleanup off-screen bullets
            for b in bullets:
                if b.rect.bottom < 0:
                    b.kill()

            # cleanup enemies off bottom (player loses life)
            for e in enemies:
                if e.rect.top > HEIGHT:
                    e.kill()
                    player.lives -= 1
                    explosions.append({'pos': (e.rect.centerx, HEIGHT - 20), 'timer': 0})
                    if player.lives <= 0:
                        state = 'GAMEOVER'

            # update explosions
            for ex in explosions[:]:
                ex['timer'] += dt
                if ex['timer'] > 0.5:
                    explosions.remove(ex)

        # draw
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        if state == 'START':
            draw_text(screen, TITLE, 48, WIDTH // 2, HEIGHT // 3)
            draw_text(screen, 'Press ENTER to start', 28, WIDTH // 2, HEIGHT // 2)
            draw_text(screen, 'Move: Left/Right  Shoot: Space', 22, WIDTH // 2, HEIGHT // 2 + 40)

        elif state == 'PLAYING':
            player_group.draw(screen)
            bullets.draw(screen)
            enemies.draw(screen)

            # draw explosions (simple expanding circles)
            for ex in explosions:
                t = ex['timer']
                radius = int(8 + 40 * t)
                alpha = max(0, 255 - int(510 * t))
                surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 160, 0, alpha), (radius, radius), radius)
                screen.blit(surf, (ex['pos'][0] - radius, ex['pos'][1] - radius))

            draw_text(screen, f'Score: {score}', 22, 70, 20, align='topleft')
            draw_text(screen, f'Lives: {player.lives}', 22, WIDTH - 90, 20, align='topleft')

        elif state == 'GAMEOVER':
            draw_text(screen, 'GAME OVER', 56, WIDTH // 2, HEIGHT // 3)
            draw_text(screen, f'Score: {score}', 32, WIDTH // 2, HEIGHT // 2)
            draw_text(screen, 'Press ENTER to restart', 24, WIDTH // 2, HEIGHT // 2 + 50)

        pygame.display.flip()


if __name__ == '__main__':
    main()

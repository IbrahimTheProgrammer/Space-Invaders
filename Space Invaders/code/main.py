import pygame
import sys
import random
from spaceship import Spaceship
from invader import Invader
from high_score import read_high_score, write_high_score

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700

GREY = (29, 29, 27)
WHITE = (255, 255, 255)

HIGH_SCORE_FILE = "score/high_score.txt"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
filter_image = pygame.image.load("Graphics/tv.png")
filter_image = pygame.transform.scale(
    filter_image, (SCREEN_WIDTH + 25, SCREEN_HEIGHT + 30))
clock = pygame.time.Clock()


def restart_game():
    global spaceship, spaceship_group, invader_group, score, start_time, game_active, high_score, invaders_passed, spawn_rate
    spaceship = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT)
    spaceship_group = pygame.sprite.GroupSingle(spaceship)
    invader_group = pygame.sprite.Group()
    score = 0
    start_time = pygame.time.get_ticks()
    game_active = True
    high_score = read_high_score(HIGH_SCORE_FILE)
    invaders_passed = 0
    spawn_rate = 1  # Initial spawn rate


restart_game()

INVADER_SPAWN_EVENT = pygame.USEREVENT + 1
# Spawn a new invader every second
pygame.time.set_timer(INVADER_SPAWN_EVENT, 1000)

SPAWN_RATE_INCREASE_EVENT = pygame.USEREVENT + 2
# Increase spawn rate every 60 seconds
pygame.time.set_timer(SPAWN_RATE_INCREASE_EVENT, 60000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INVADER_SPAWN_EVENT and game_active:
            for _ in range(spawn_rate):  # Spawn multiple invaders based on spawn rate
                invader = Invader(SCREEN_WIDTH)
                invader_group.add(invader)
        if event.type == SPAWN_RATE_INCREASE_EVENT:
            spawn_rate += 1  # Increase spawn rate every 60 seconds
        if event.type == pygame.KEYDOWN and not game_active:
            if event.key == pygame.K_SPACE:
                restart_game()

    if game_active:
        # Updating
        spaceship_group.update()
        invader_group.update()

        # Check for collisions
        for laser in spaceship.lasers:
            invader_hit_list = pygame.sprite.spritecollide(
                laser, invader_group, True)
            for invader in invader_hit_list:
                laser.kill()
                score += 1

        for invader in invader_group:
            if invader.rect.top > SCREEN_HEIGHT:
                invader.kill()
                invaders_passed += 1
                if invaders_passed >= 3:
                    game_active = False
                    if score > high_score:
                        write_high_score(HIGH_SCORE_FILE, score)

        if pygame.sprite.spritecollideany(spaceship, invader_group):
            game_active = False
            if score > high_score:
                write_high_score(HIGH_SCORE_FILE, score)

        # Drawing
        screen.fill(GREY)
        spaceship_group.draw(screen)
        spaceship.lasers.draw(screen)
        invader_group.draw(screen)
        screen.blit(filter_image, (0, 0))

        # Display score, high score, and timer
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        score_text = font.render(f'Score: {score}', True, WHITE)
        timer_text = font.render(f'Time: {elapsed_time:.2f}', True, WHITE)
        high_score_text = font.render(f'H-Score: {high_score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 75, 10))

    else:
        game_over_text = big_font.render('GAME OVER', True, WHITE)
        restart_text = font.render('Press SPACE to Restart', True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() /
                    2, SCREEN_HEIGHT / 2 - game_over_text.get_height() / 2))
        screen.blit(restart_text, (SCREEN_WIDTH / 2 - restart_text.get_width() /
                    2, SCREEN_HEIGHT / 2 + game_over_text.get_height()))

    pygame.display.update()
    clock.tick(60)

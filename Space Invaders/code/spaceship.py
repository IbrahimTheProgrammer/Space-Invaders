import pygame
from laser import Laser


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Graphics/player.png")
        self.rect = self.image.get_rect(midbottom=(
            self.screen_width / 2, self.screen_height))
        self.speed = 6
        self.lasers = pygame.sprite.Group()
        self.shoot_cooldown = 500  # Cooldown in milliseconds
        self.last_shot_time = pygame.time.get_ticks()  # Get the current time

    def get_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            self.shoot_laser()

    def shoot_laser(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            laser = Laser(self.rect.midtop)
            self.lasers.add(laser)
            self.last_shot_time = current_time

    def update(self):
        self.get_user_input()
        self.constraint_movement()
        self.lasers.update()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.lasers.draw(surface)

    def constraint_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < 0:
            self.rect.left = 0

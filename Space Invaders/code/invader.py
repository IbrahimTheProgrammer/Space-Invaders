import pygame
import random


class Invader(pygame.sprite.Sprite):
    def __init__(self, screen_width):
        super().__init__()
        self.image = pygame.image.load("Graphics/yellow.png")
        self.rect = self.image.get_rect(
            midtop=(random.randint(20, screen_width - 20), 0))  # Ensure invaders spawn at least 20 pixels away from screen edges
        self.speed = 2  # Slower speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()

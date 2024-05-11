import pygame
from pygame.sprite import Sprite


class Person(Sprite):
    def __init__(self, screen, settings):
        super().__init__()
        self.image = pygame.image.load('assets/images/person.png')
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings

        self.rect.center = self.screen_rect.center

        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def update(self):
        if self.up:
            self.rect.y -= self.settings.person_speed
        if self.down:
            self.rect.y += self.settings.person_speed
        if self.left:
            self.rect.x -= self.settings.person_speed
        if self.right:
            self.rect.x += self.settings.person_speed

        self.screen.blit(self.image, self.rect)

import pygame
from pygame.sprite import Sprite


class Gun(Sprite):
    def __init__(self, screen, settings, person):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('assets/images/gun.png')
        self.rect = self.image.get_rect()

        self.person = person

        if pygame.mouse.get_pos()[0] <= self.person.rect.x:
            self.rect.midright = self.person.rect.center
        else:
            self.rect.midleft = self.person.rect.center

        self.old_mouse = None

    def update(self):
        if not self.old_mouse:
            self.old_mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.math.Vector2(mouse_pos)
        mouse_move = mouse - self.old_mouse
        r, angle = mouse_move.as_polar()
        self.image = pygame.transform.rotate(self.image.convert_alpha(), -angle)

        self.old_mouse = mouse

        if pygame.mouse.get_pos()[0] <= self.person.rect.x:
            self.rect.midright = self.person.rect.center
        else:
            self.rect.midleft = self.person.rect.center

        self.screen.blit(self.image, self.rect)


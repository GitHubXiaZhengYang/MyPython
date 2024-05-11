import pygame
from game import Setting
from game.Gun import Gun
from game.Person import Person

settings = Setting.Settings()


def main():
    global settings

    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill(settings.bg_colour)
    settings.screen_width = screen.get_width()
    settings.screen_height = screen.get_height()

    pygame.display.set_caption("Game")
    pygame.display.set_icon(pygame.image.load("assets/images/Logo_Mr.X.ico"))

    person = Person(screen, settings)
    gun = Gun(screen, settings, person)

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False

        person.update()
        gun.update()

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()

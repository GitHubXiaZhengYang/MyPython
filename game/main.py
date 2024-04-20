import pygame
from game import Setting

settings = Setting.Settings()
def main():
    global settings

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    settings.screen_width = screen.get_width()
    settings.screen_height = screen.get_height()

    pygame.display.set_caption("Game")
    pygame.display.set_icon(pygame.image.load("assets/images/Logo_Mr.X.ico"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    running = False

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__':
    main()

import pygame
from interface.menu_interface import MaimMenuInterface


def main():
    pygame.init()

    size = 1400, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("honkai impact 4th")

    interface = MaimMenuInterface(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                interface.click = True

        interface.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
import pygame
from interface.menu_interface import MainMenuInterface


def main():
    pygame.init()

    info = pygame.display.Info()

    size = info.current_w, info.current_h
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("honkai impact 4th")

    interface = MainMenuInterface(screen, size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                interface.click = True
            interface.update(event)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
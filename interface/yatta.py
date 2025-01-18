import pygame
import sys
import os


class Yatta(pygame.sprite.Sprite):
    def __init__(self, *group, win):
        super().__init__(*group)
        if win:
            self.image = self.load_image('yatta.png')
        else:
            self.image = self.load_image('not yatta.png')

        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 550, 500

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/yatta', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image
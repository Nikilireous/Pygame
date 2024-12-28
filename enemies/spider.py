import pygame
import sys
import os
import math


class Spider(pygame.sprite.Sprite):
    def __init__(self, *group, fps, player):
        super().__init__(*group)
        self.frames = [f"pauk{i}.png" for i in range(11)]
        self.fps = fps
        self.player = player
        self.cur_frame = 0
        self.image = self.load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 0
        self.speed = 2
        self.clock = 0

    def move_towards_player(self, player, change):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        try:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed - change[0]
            self.rect.y += dy * self.speed - change[1]
        except ZeroDivisionError:
            pass

    def update(self, change):
        self.move_towards_player(self.player, change)

        if self.clock == 250 // self.fps:
            dx, dy = (self.player.rect.x - self.rect.x), (self.player.rect.y - self.rect.y)
            self.clock = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.load_image(self.frames[self.cur_frame])
            self.image = pygame.transform.scale(self.image, (100, 100))

            angle = math.degrees(math.atan2(-dx, dy))
            self.image = pygame.transform.rotate(self.image, -angle)
        else:
            self.clock += 1

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/enemies/pauk', name)
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
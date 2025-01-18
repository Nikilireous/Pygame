import pygame
import sys
import os
import math
import time


class Witch(pygame.sprite.Sprite):
    def __init__(self, *group, fps, player, x, y, difficult):
        super().__init__(*group)
        self.frames = [self.load_image(f"vedma{i}.png") for i in range(3)]
        self.fps = fps
        self.player = player
        self.difficult = difficult
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.movement_type = 'vector'
        self.current_time = 3
        self.delta_time = time.time()
        self.dx = self.dy = self.dist = None
        self.speed = 12
        self.clock = 0
        self.HP = 150
        self.damage = 1 if self.difficult == 'Easy' else 2

    def vector_move(self, change, dx, dy, dist):
        try:
            dx, dy = (dx / dist * self.speed), (dy / dist * self.speed)

            if self.movement_type == 'vector':
                self.rect.x += dx - change[0]
                self.rect.y += dy - change[1]
            else:
                self.rect.x -= change[0]
                self.rect.y -= change[1]

        except ZeroDivisionError:
            pass

    def update(self, change, player, visible_sprites):
        if self.current_time >= 2:
            self.dx, self.dy = player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y
            self.dist = math.hypot(self.dx, self.dy)
            self.delta_time = time.time()

        if self.movement_type == 'vector':
            self.vector_move(change, self.dx, self.dy, self.dist)

        if -60 < self.rect.centerx < 1500 and -60 < self.rect.centery < 870:
            visible_sprites.add(self)
            if self.clock == 500 // self.fps:
                self.clock = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.image = pygame.transform.scale(self.image, (40, 80))

                angle = math.degrees(math.atan2(-self.dx, self.dy))
                if angle >= 0:
                    self.image = pygame.transform.rotate(self.image, -angle)
                else:
                    self.image = pygame.transform.rotate(self.image, angle)
                    self.image = pygame.transform.flip(self.image, True, False)

            else:
                self.clock += 1

        self.current_time = time.time() - self.delta_time

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/enemies/vedma', name)
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

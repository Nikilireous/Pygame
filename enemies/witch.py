import pygame
import sys
import os
import math
import time


class Witch(pygame.sprite.Sprite):
    def __init__(self, *group, player, x, y, difficult):
        super().__init__(*group)
        self.frames = [self.load_image(f"vedma{i}.png") for i in range(3)]
        self.player = player
        self.difficult = difficult
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.pos = [x, y]
        self.movement_type = 'vector'
        self.current_time = 3
        self.delta_time = time.time()
        self.dx = self.dy = self.dist = None
        self.speed = 1250
        self.clock = 0
        self.HP = 150
        self.damage = 1 if self.difficult == 'Easy' else 2

    def vector_move(self, change, dx, dy, dist, dt):
        try:
            dx, dy = (dx / dist * self.speed * dt), (dy / dist * self.speed * dt)

            self.pos[0] += dx - change[0]
            self.pos[1] += dy - change[1]

            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

        except ZeroDivisionError:
            pass

    def update(self, change, player, visible_sprites, dt):
        info = pygame.display.Info()
        if self.current_time >= 2:
            self.dx, self.dy = player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y
            self.dist = math.hypot(self.dx, self.dy)
            self.delta_time = time.time()

        if self.movement_type == 'vector':
            self.vector_move(change, self.dx, self.dy, self.dist, dt)

        if -60 < self.rect.centerx < info.current_w * 1.1 and -60 < self.rect.centery < info.current_h * 1.1:
            visible_sprites.add(self)

            self.clock += dt

            if self.clock >= 1 / 20:
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

import pygame
import sys
import os
import math
# from pathfinding.core.grid import Grid
# from pathfinding.finder.a_star import AStarFinder


class Spider(pygame.sprite.Sprite):
    def __init__(self, *group, map_data, player, x, y, difficult):
        super().__init__(*group)
        self.frames = [self.load_image(f"pauk{i}.png") for i in range(11)]
        self.player = player
        self.map_data = map_data
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.pos = [x, y]
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = x, y
        self.speed = 250 if difficult == "Easy" else 350
        self.clock = 0
        self.HP = 200 if difficult == "Easy" else 270
        self.damage = 1 if difficult == "Easy" else 2

    def get_legs_coords(self, camera_x, camera_y, tile_size):
        left_x = (self.rect.x + camera_x) // tile_size
        right_x = (self.rect.x + 80 + camera_x) // tile_size
        map_y = (self.rect.y + camera_y) // tile_size
        return (left_x, map_y), (right_x, map_y)

    def get_center_coords(self, camera_x, camera_y, tile_size):
        centre_x = (camera_x + self.rect.centerx) // tile_size
        center_y = (camera_y + self.rect.centery) // tile_size
        return centre_x, center_y

    def vector_move(self, player, change, dt):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        try:
            dx, dy = ((dx / dist) * self.speed * dt), ((dy / dist) * self.speed * dt)

            self.pos[0] += dx - change[0]
            self.pos[1] += dy - change[1]

            self.rect.x = self.pos[0]
            self.rect.y = self.pos[1]

        except ZeroDivisionError:
            pass

    def update(self, change, camera_pos, visible_sprites, dt):
        info = pygame.display.Info()
        self.vector_move(self.player, change, dt)

        if -60 < self.rect.centerx < info.current_w * 1.1 and -60 < self.rect.centery < info.current_h * 1.1:
            visible_sprites.add(self)
            self.clock += dt
            if self.clock >= 1/40:
                dx, dy = (self.player.rect.x - self.rect.x), (self.player.rect.y - self.rect.y)
                self.clock = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.image = pygame.transform.scale(self.image, (100, 100))

                angle = math.degrees(math.atan2(-dx, dy))
                self.image = pygame.transform.rotate(self.image, -angle)

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

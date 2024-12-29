import pygame
import math
import sys
import os


class KianaBaseAttack(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, fps, map_data, player_pos):
        super().__init__(*group)
        self.pos = (x, y)
        self.player_pos = player_pos
        self.fps = fps
        self.map = map_data
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.image = self.load_image("bullet.png")
        self.image = pygame.transform.scale(self.image, (15, 10))
        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.speed = 800 // self.fps

    def get_map_coords(self, camera_x, camera_y, tile_size):
        map_x = (camera_x + self.rect.centerx) // tile_size
        map_y = (camera_y + self.rect.centery) // tile_size
        return map_x, map_y

    def update(self, change, camera_pos, enemies_group):

        collision_object = pygame.sprite.spritecollideany(self, enemies_group)
        if collision_object:
            collision_object.HP -= 5
            self.kill()

        self.pos = (self.pos[0] + self.dir[0] * self.speed - change[0],
                    self.pos[1] + self.dir[1] * self.speed - change[1])
        self.rect.center = self.pos

        screen_width, screen_height = pygame.display.get_surface().get_size()
        if (self.pos[0] < 0 or self.pos[0] > screen_width or
                self.pos[1] < 0 or self.pos[1] > screen_height):
            self.kill()

        map_x, map_y = self.get_map_coords(camera_pos[0], camera_pos[1], 128)

        if self.map[map_y][map_x] == 1:
            self.kill()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/characters/Kiana', name)
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


class SkillE(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.frames = [f"laser{i}.png" for i in range(12)]
        self.cur_frame = 0
        self.image = self.load_image(self.frames[self.cur_frame])
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 400

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.load_image(self.frames[self.cur_frame])

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/characters/Kiana/Laser', name)
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

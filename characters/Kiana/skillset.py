import math
import os
import sys
import time

import pygame


class KianaBaseAttack(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, map_data, player_pos, player):
        super().__init__(*group)
        self.pos = (x, y)
        self.player = player
        self.player_pos = player_pos
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

        self.speed = 800

    def get_map_coords(self, camera_x, camera_y, tile_size):
        map_x = (camera_x + self.rect.centerx) // tile_size
        map_y = (camera_y + self.rect.centery) // tile_size
        return map_x, map_y

    def update(self, change, camera_pos, enemies_group, dt):
        collision_object = pygame.sprite.spritecollideany(self, enemies_group)
        if collision_object:
            collision_object.HP -= self.player.base_atk_damage
            self.kill()
            if collision_object.HP <= 0:
                collision_object.kill()
                self.player.XP += 1

        self.pos = (self.pos[0] + self.dir[0] * self.speed * dt - change[0],
                    self.pos[1] + self.dir[1] * self.speed * dt - change[1])
        self.rect.center = self.pos

        screen_width, screen_height = pygame.display.get_surface().get_size()
        if (self.pos[0] < 0 or self.pos[0] > screen_width or
                self.pos[1] < 0 or self.pos[1] > screen_height):
            self.kill()

        map_x, map_y = self.get_map_coords(camera_pos[0], camera_pos[1], 128)

        if self.map[round(map_y)][round(map_x)] == 1:
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


class KianaSkillE(pygame.sprite.Sprite):
    def __init__(self, *group, player, res):
        super().__init__(*group)
        self.frames = [self.load_image(f"lazer{i}.png") for i in range(12)]
        self.fire_to_second = 10
        self.player = player
        self.fire = 0
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.lazerWidth = 150
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.time = time.time()
        self.resolution = res

    def update(self, enemy_group, deltaTime, screen):
        if time.time() - self.time >= 3:
            self.kill()

        self.pos = (self.rect.x, self.rect.y)
        self.mx, self.my = pygame.mouse.get_pos()
        self.dir = (self.mx - self.resolution[0] / 2, self.my - self.resolution[1] / 2)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        for enemy in enemy_group:
            info = pygame.display.Info()
            center = [info.current_w / 2, info.current_h / 2]
            pos = [enemy.rect.centerx + 25 - center[0], enemy.rect.centery + 25 - center[1]]
            mPos = [self.mx - center[0], self.my - center[1]]
            a = math.hypot(mPos[0], mPos[1])
            b = math.hypot(pos[0], pos[1])
            if b == 0: b = 0.0001
            alpha = abs(math.atan2(mPos[1] / a, mPos[0] / a) - math.atan2(pos[1] / b, pos[0] / b))
            height = b * math.sin(alpha)
            # pygame.draw.line(screen, "blue", (pos[0] + center[0], pos[1] + center[1]), (pos[0] + height + center[0], pos[1] + center[1]), 5)
            if math.degrees(alpha) <= 90 and height < self.lazerWidth / 2:
                self.shot(enemy, deltaTime)

        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.resolution[0] / 2, self.resolution[1] / 2

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

    def shot(self, enemy, dt):
        if enemy.HP - self.player.skill_damage * dt <= 0:
            enemy.kill()
            self.player.XP += 1
        else:
            enemy.HP -= self.player.skill_damage * dt

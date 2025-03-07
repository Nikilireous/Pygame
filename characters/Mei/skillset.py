import pygame
import math
import sys
import os
import time


class MeiBaseAttack(pygame.sprite.Sprite):
    def __init__(self, *group, player, res):
        super().__init__(*group)
        self.cur_frame = 0
        self.player = player
        self.frames_time = 1
        self.frames_second = 0
        self.frames = [self.load_image(f"katana{i}.png") for i in range(15)]
        self.shot_enemies = set()
        self.resolution = res
        self.image = self.frames[self.cur_frame]

        mx, my = pygame.mouse.get_pos()

        info = pygame.display.Info()
        center = [info.current_w / 2, info.current_h / 2]

        mx += 720 - center[0]
        my += 405 - center[1]

        self.dir = (mx - 720, my - 405)
        self.length = math.hypot(*self.dir)
        if self.length == 0.0:
            self.dir2 = (0, -1)
        else:
            self.dir2 = (self.dir[0] / self.length, self.dir[1] / self.length)
        self.angle = math.degrees(math.atan2(-self.dir2[1], self.dir2[0]))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image = pygame.transform.flip(self.image, True, True)

        self.rect = self.image.get_rect()

        self.pos = (self.resolution[0]/2 + self.dir2[0] * 200,
                    self.resolution[1]/2 + self.dir2[1] * 200)
        self.rect.center = self.pos

    def update(self, change, camera_pos, enemies_group, dt):
        if self.frames_second == self.frames_time:
            self.frames_second = 0
            if self.cur_frame + 1 == len(self.frames):
                self.kill()

            collision_object = set(pygame.sprite.spritecollide(self, enemies_group, False))
            collision_object = collision_object - (collision_object & self.shot_enemies)
            for enemy in collision_object:
                self.shot(enemy)

            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.image = pygame.transform.flip(self.image, True, True)

        else:
            self.frames_second += 1

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/characters/Mei/Skill', name)
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

    def shot(self, enemy):
        enemy_length_x = enemy.rect.centerx - self.resolution[0]/2
        enemy_length_y = enemy.rect.centery - self.resolution[1]/2
        enemy_vector = (enemy_length_x, enemy_length_y)
        enemy_distance = math.hypot(enemy_length_x, enemy_length_y)
        if enemy_distance == 0: enemy_distance = 0.001
        dot_product = self.dir[0] * enemy_vector[0] + self.dir[1] * enemy_vector[1]
        angle2 = dot_product / (self.length * enemy_distance)

        if enemy_distance <= 195 and 0.5 <= angle2 <= 1:
            if enemy.HP - self.player.base_atk_damage <= 0:
                enemy.kill()
                self.player.XP += 1
            else:
                enemy.HP -= self.player.base_atk_damage
                self.shot_enemies.add(enemy)


class MeiSkillE:
    def __init__(self, player, map, enemy, resolution):
        self.player = player
        self.map = map
        self.enemy = enemy

        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - resolution[0]/2, my - resolution[1]/2)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)

        self.speed = 1000

    def dash(self, dt):
        positions = [(self.map.player_y + 35 + int(self.dir[1] * self.speed * dt), self.map.player_x + 10 + int(self.dir[0] * self.speed * dt)),
                     (self.map.player_y - 30 + int(self.dir[1] * self.speed * dt), self.map.player_x - 10 + int(self.dir[0] * self.speed * dt)),
                     (self.map.player_y + 35 + int(self.dir[1] * self.speed * dt), self.map.player_x - 10 + int(self.dir[0] * self.speed * dt)),
                     (self.map.player_y - 30 + int(self.dir[1] * self.speed * dt), self.map.player_x + 10 + int(self.dir[0] * self.speed * dt))]

        if all(list(map(self.dash_conditions, positions))):
            self.map.player_x += self.dir[0] * self.speed * dt
            self.map.player_y += self.dir[1] * self.speed * dt
            if self.enemy:
                for i in self.enemy:
                    i.pos[0] -= self.dir[0] * self.speed * dt
                    i.pos[1] -= self.dir[1] * self.speed * dt

    def dash_conditions(self, pos):
        player_in_tiles_cor = (pos[0] // self.map.TILE_SIZE, pos[1] // self.map.TILE_SIZE)
        if self.map.map_data[round(player_in_tiles_cor[0])][round(player_in_tiles_cor[1])] not in [0, 5]:
            return False
        return True
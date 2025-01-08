import pygame
import math
import sys
import os
import time


class MeiBaseAttack(pygame.sprite.Sprite):
    def __init__(self, *group, fps, player):
        super().__init__(*group)
        self.cur_frame = 0
        self.player = player
        self.fps = fps
        self.frames_time = 1
        self.frames_second = 0
        self.frames = [self.load_image(f"katana{i}.png") for i in range(15)]
        self.shot_enemies = set()

        self.image = self.frames[self.cur_frame]

        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - 700, my - 400)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.image = pygame.transform.rotate(self.image, self.angle)
        self.image = pygame.transform.flip(self.image, True, True)

        self.rect = self.image.get_rect()

        self.pos = (700 + self.dir[0] * 200,
                    400 + self.dir[1] * 200)
        self.rect.center = self.pos

    def update(self, change, camera_pos, enemies_group):
        if self.frames_second == self.frames_time:
            self.frames_second = 0
            if self.cur_frame + 1 == len(self.frames):
                self.kill()

            collision_object = set(pygame.sprite.spritecollide(self, enemies_group, False))
            if collision_object - (collision_object & self.shot_enemies):
                for enemie in collision_object:
                    self.shot(enemie)

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

        if pygame.sprite.collide_mask(self, enemy):
            if enemy.HP - self.player.base_atk_damage <= 0:
                enemy.kill()
                self.player.XP += 1
            else:
                enemy.HP -= self.player.base_atk_damage
                print(enemy.HP)
                self.shot_enemies.add(enemy)


class MeiSkillE:
    def __init__(self, player, map, enemy):
        self.player = player
        self.map = map
        self.enemy = enemy

        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - 700, my - 400)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)

        self.speed = 10

    def dash(self):
        positions = [(self.map.player_y + 35 + int(self.dir[1] * self.speed), self.map.player_x + 10 + int(self.dir[0] * self.speed)),
                     (self.map.player_y - 30 + int(self.dir[1] * self.speed), self.map.player_x - 10 + int(self.dir[0] * self.speed)),
                     (self.map.player_y + 35 + int(self.dir[1] * self.speed), self.map.player_x - 10 + int(self.dir[0] * self.speed)),
                     (self.map.player_y - 30 + int(self.dir[1] * self.speed), self.map.player_x + 10 + int(self.dir[0] * self.speed))]

        if all(list(map(self.dash_conditions, positions))):
            self.map.player_x += int(self.dir[0] * self.speed)
            self.map.player_y += int(self.dir[1] * self.speed)
            if self.enemy:
                for i in self.enemy:
                    i.rect.x -= int(self.dir[0] * self.speed)
                    i.rect.y -= int(self.dir[1] * self.speed)

    def dash_conditions(self, pos):
        player_in_tiles_cor = (pos[0] // self.map.TILE_SIZE, pos[1] // self.map.TILE_SIZE)
        if self.map.map_data[player_in_tiles_cor[0]][player_in_tiles_cor[1]] not in [0]:
            return False
        return True
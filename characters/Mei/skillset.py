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
        self.frames_time = 3
        self.frames_second = 0
        self.frames = [self.load_image(f"katana{i}.png") for i in range(7)]
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

        self.pos = (700 + self.dir[0] * 250,
                    400 + self.dir[1] * 250)
        self.rect.center = self.pos


    def update(self, change, camera_pos, enemies_group):
        if self.frames_second == self.frames_time:
            self.frames_second = 0
            if self.cur_frame + 1 == 7:
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

    def shot(self, enemie):
        if pygame.sprite.collide_mask(self, enemie):
            print(enemie.HP - self.player.base_atk_damage)
            if enemie.HP - self.player.base_atk_damage <= 0:
                enemie.kill()
                self.player.XP += 1
            else:
                enemie.HP -= self.player.base_atk_damage
                self.shot_enemies.add(enemie)


class MeiSkillE(pygame.sprite.Sprite):
    def __init__(self, *group, fps):
        super().__init__(*group)
        self.frames = [self.load_image(f"lazer{i}.png") for i in range(12)]
        self.fire_to_second = 10
        self.fps = fps
        self.fire = 0
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 360
        self.time = time.time()

    def update(self, enemies_group, player):
        if time.time() - self.time >= 3:
            self.kill()

        if self.fire == self.fps // self.fire_to_second:
            self.fire = 0
            collision_object = pygame.sprite.spritecollide(self, enemies_group, False)
            if collision_object:
                for enemie in collision_object:
                    if pygame.sprite.collide_mask(self, enemie):
                        enemie.HP -= player.skill_damage
                        if enemie.HP <= 0:
                            enemie.kill()
                            player.XP += 1
        else:
            self.fire += 1


        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.pos = (self.rect.x, self.rect.y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - 700, my - 400)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()
        self.rect.center = 700, 400

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

import pygame
import sys
import os
import time


class Kiana(pygame.sprite.Sprite):
    def __init__(self, *group, fps):
        super().__init__(*group)
        self.frames = [self.load_image(f"Kiana{i}.png") for i in range(2)]
        self.level_XP = [0, 10, 20, 35, 50, 70, 90, 110, 130, 150]
        self.fps = fps
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 660, 360
        self.clock = 0
        self.max_HP = 500
        self.HP = self.max_HP
        self.XP = 0
        self.level = 1
        self.base_atk_damage = 15
        self.skill_damage = 50
        self.regeneration_to_second = 1
        self.regeneration_time = 0

    def update(self, visible_sprites):
        self.level_update_changed()
        self.regeneration()

        if self.clock == 2500 // self.fps:
            self.clock = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (80, 80))
        else:
            self.clock += 1

        collision_object = pygame.sprite.spritecollide(self, visible_sprites, False)
        if collision_object:
            for enemy in collision_object:
                if pygame.sprite.collide_mask(self, enemy):
                    self.HP -= 1

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

    def level_update_changed(self):
        if self.level != len(self.level_XP) and self.XP >= self.level_XP[self.level]:
            self.XP = self.XP - self.level_XP[self.level]
            self.level += 1
            self.new_level()

    def new_level(self):
        self.base_atk_damage += 5
        self.max_HP += 250
        self.HP += 250
        self.regeneration_to_second += 1
        self.skill_damage += 10

    def regeneration(self):
        if self.HP != self.max_HP:
            if self.regeneration_time == 0:
                self.regeneration_time = time.time()
            elif time.time() - self.regeneration_time >= 1 / self.regeneration_to_second:
                self.HP += 1
                self.regeneration_time = 0


import pygame
import sys
import os
import math
import time
from enemies.spider import Spider


class Boss(pygame.sprite.Sprite):
    def __init__(self, *group, fps, map_data, player, x, y, summons, difficult):
        super().__init__(*group)
        self.summons_group = summons
        self.frames = [self.load_image(f"boss.png")]
        self.fps = fps
        self.map_data = map_data
        self.player = player
        self.difficult = difficult
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.movement_type = 'vector'
        self.vector_time = 2
        self.circle_time = 0
        self.delta_time = time.time()
        self.dx = self.dy = self.dist = None
        self.speed = 10
        self.clock = 0
        self.max_HP = 20_000
        self.HP = self.max_HP
        if self.difficult == 'Easy':
            self.damage = 4
        if self.difficult == 'Hard':
            self.damage = 5

        self.dashes = 0
        self.circle_step = 0

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

    def circle_move(self, x, y):
        self.rect.centerx = x - 400 * math.cos(math.radians(75 + (self.circle_step // self.fps)))
        self.rect.centery = y - 400 * math.sin(math.radians(75 + (self.circle_step // self.fps)))

    def update(self, change, player, visible_sprites, screen):
        self.Boss_HP_bar(screen)
        if self.movement_type == 'vector':
            if self.vector_time > 0.7:
                self.dx, self.dy = player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y
                self.dist = math.hypot(self.dx, self.dy)
                self.delta_time = time.time()

                if self.dashes <= 7:
                    self.dashes += 1

            self.vector_move(change, self.dx, self.dy, self.dist)

            if self.dashes > 7:
                self.movement_type = 'circle'
                self.delta_time = time.time()
            self.vector_time = time.time() - self.delta_time


        elif self.movement_type == 'circle':
            self.circle_step += 270
            self.circle_move(self.player.rect.centerx, self.player.rect.centery)

            self.dx, self.dy = player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y
            self.dist = math.hypot(self.dx, self.dy)

            if self.circle_time > 2:
                self.movement_type = 'vector'
                self.dashes = 0
                self.delta_time = time.time()

                Spider(self.summons_group, fps=self.fps, map_data=self.map_data,
                                  player=self.player, x=self.rect.centerx, y=self.rect.centery)

            self.circle_time = time.time() - self.delta_time


        if -60 < self.rect.centerx < 1460 and -60 < self.rect.centery < 860:
            visible_sprites.add(self)
            if self.clock == 500 // self.fps:
                self.clock = 0
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.image = pygame.transform.scale(self.image, (180, 180))

                angle = math.degrees(math.atan2(-self.dx, self.dy))
                self.image = pygame.transform.rotate(self.image, -angle)
            else:
                self.clock += 1

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/enemies/boss', name)
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

    def Boss_HP_bar(self, screen):
        HP_bar = pygame.Surface((250, 30))
        HP_bar.fill("Blue")

        non_hp_bar = self.max_HP - self.HP
        k = self.max_HP // 250
        pygame.draw.rect(HP_bar, (0, 0, 0), ((self.HP // k, 0), (non_hp_bar // k + 10, 30)))

        font = pygame.font.Font(None, 30)
        text = font.render(f"{str(self.HP)} / {self.max_HP}", 1, (255, 255, 255))
        HP_bar.blit(text, (70, 5))

        screen.blit(HP_bar, (1140, 10))

import pygame
import os
import sys
import math
import random
from map import Map


class Kiana(pygame.sprite.Sprite):
    def __init__(self, *group, fps):
        super().__init__(*group)
        self.frames = ["Kiana0-Photoroom.png", "Kiana00-Photoroom.png"]
        self.fps = fps
        self.cur_frame = 0
        self.image = self.load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 660, 360
        self.clock = 0

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images', name)
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

    def update(self):
        if self.clock == self.fps // 4:
            self.clock = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.load_image(self.frames[self.cur_frame])
            self.image = pygame.transform.scale(self.image, (80, 80))
        else:
            self.clock += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.image = self.load_image("bullet.png")  # Атрибут image
        self.image = pygame.transform.scale(self.image, (15, 10))
        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = self.image.get_rect()  # Атрибут rect
        self.rect.center = self.pos

        self.speed = 8

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)
        self.rect.center = self.pos

        screen_width, screen_height = pygame.display.get_surface().get_size()
        if (self.pos[0] < 0 or self.pos[0] > screen_width or
                self.pos[1] < 0 or self.pos[1] > screen_height):
            self.kill()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images', name)
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


def main():
    pygame.init()
    size = 1400, 800
    fps = 100
    map0 = Map((200, 320))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Kiana_game")

    character_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()

    Kiana(character_sprites, fps=fps)

    clock = pygame.time.Clock()
    seconds_to_shoot = 0
    fire = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                fire = True
                Bullet(size[0] // 2, size[1] // 2, bullet_sprites)
            if event.type == pygame.MOUSEBUTTONUP:
                fire = False
                seconds_to_shoot = 0

        if fire:
            if seconds_to_shoot == fps // 10:
                seconds_to_shoot = 0
                Bullet(size[0] // 2, size[1] // 2, bullet_sprites)
            else:
                seconds_to_shoot += 1

        screen.fill(0)
        map0.update(screen)
        character_sprites.draw(screen)
        character_sprites.update()

        bullet_sprites.update()
        bullet_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

import pygame
import os
import sys
import math
import random


class Kiana(pygame.sprite.Sprite):
    def __init__(self, *group, fps):
        super().__init__(*group)
        self.frames = ["Kiana0-Photoroom.png", "Kiana00-Photoroom.png"]
        self.fps = fps
        self.cur_frame = 0
        self.image = self.load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 650, 350
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
            self.image = pygame.transform.scale(self.image, (100, 100))
        else:
            self.clock += 1


class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = self.load_image("bullet.png")
        self.bullet = pygame.transform.scale(self.bullet, (15, 10))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 10

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center=self.pos)
        surf.blit(self.bullet, bullet_rect)

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
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Kiana_game")

    character_sprites = pygame.sprite.Group()
    bullet_sprites = []

    Kiana(character_sprites, fps=fps)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                bullet_sprites.append(Bullet(700, 400))

        screen.fill(0)
        character_sprites.draw(screen)
        character_sprites.update()

        for bullet in bullet_sprites[:]:
            bullet.update()
            if not screen.get_rect().collidepoint(bullet.pos):
                bullet_sprites.remove(bullet)

        for bullet in bullet_sprites:
            bullet.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

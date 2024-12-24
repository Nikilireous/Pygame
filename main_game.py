import pygame
import os
import sys
import random


class Kiana(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.frames = ["Kiana0-Photoroom.png", "Kiana00-Photoroom.png"]
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
        if self.clock == 15:
            self.clock = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.load_image(self.frames[self.cur_frame])
            self.image = pygame.transform.scale(self.image, (100, 100))
        else:
            self.clock += 1


class Bullet(pygame.sprite.Sprite):
    def __init__(self, *group, x, y):
        super().__init__(*group)
        self.image = self.load_image("bullet-Photoroom.png", colorkey=-1)
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 700, 400
        self.step_x = (x - self.rect.x + random.randrange(-2, 3)) / 50
        self.step_y = (y - self.rect.y + random.randrange(-2, 3)) / 50

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
        self.rect.x += self.step_x
        self.rect.y += self.step_y


def main():
    pygame.init()
    size = 1400, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Kiana_game")

    character_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()

    Kiana(character_sprites)

    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = event.pos
                Bullet(bullet_sprites, x=x, y=y)

        screen.fill((0, 0, 0))

        character_sprites.draw(screen)
        character_sprites.update()
        bullet_sprites.draw(screen)
        bullet_sprites.update()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

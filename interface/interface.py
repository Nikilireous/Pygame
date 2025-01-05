import pygame
import time

class Interface:
    def __init__(self, player):
        self.player = player
        self.time = time.time()

    def draw_interface(self, screen):
        self.HP_bar(screen)
        self.lvl_text(screen)
        self.XP_to_level_bar(screen)
        self.timer(screen)

    def HP_bar(self, screen):
        HP_bar = pygame.Surface((250, 30))
        HP_bar.fill("red")

        non_hp_bar = self.player.max_HP - self.player.HP
        k = self.player.max_HP // 250
        pygame.draw.rect(HP_bar, (0, 0, 0), ((self.player.HP // k, 0), (non_hp_bar // k + 10, 30)))

        font = pygame.font.Font(None, 30)
        text = font.render(f"{str(self.player.HP)} / {self.player.max_HP}", 1, (255, 255, 255))
        HP_bar.blit(text, (85, 5))

        screen.blit(HP_bar, (575, 740))

    def lvl_text(self, screen):
        font = pygame.font.Font(None, 30)
        text = font.render(f"Lv.{self.player.level}", 1, (0, 0, 0))

        screen.blit(text, (525, 750))

    def XP_to_level_bar(self, screen):
        level_bar = pygame.Surface((250, 5))
        level_bar.fill("black")

        if self.player.level != len(self.player.level_XP):
            k = 250 / self.player.level_XP[self.player.level]
            pygame.draw.rect(level_bar, "white", ((0, 0), (self.player.XP * k, 5)))

        screen.blit(level_bar, (575, 780))

    def timer(self, screen):
        font = pygame.font.Font(None, 50)
        t = str(time.ctime(time.time() - self.time))
        text = font.render(t.split()[3][3:], 1, (0, 0, 0))

        screen.blit(text, (655, 10))


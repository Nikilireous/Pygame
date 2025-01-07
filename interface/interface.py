import pygame
import time

class Interface:
    def __init__(self, player):
        self.player = player
        self.time = time.time()
        self.skill_start = False
        self.skill_time = None
        self.skill_ready = True
        self.current_time = None

    def draw_interface(self, screen):
        self.HP_bar(screen)
        self.lvl_text(screen)
        self.XP_to_level_bar(screen)
        self.timer(screen)
        self.skill_bar(screen)

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
        self.current_time = time.time() - self.time
        t = str(time.ctime(self.current_time))
        text = font.render(t.split()[3][3:], 1, (0, 0, 0))

        screen.blit(text, (655, 10))

    def skill_bar(self, screen):
        skill_bar = pygame.Surface((20, 45))
        if self.skill_ready:
            skill_bar.fill("yellow")
            font = pygame.font.Font(None, 29)
            text = font.render(f"E", 1, (0, 0, 0))
            skill_bar.blit(text, (3, 13))
        else:
            skill_bar.fill("black")

        if self.skill_start or self.skill_time:
            if not self.skill_time:
                self.skill_time = time.time()
                self.skill_start = False
                self.skill_ready = False

            height = 45 - (45 / self.player.skill_recharge * (time.time() - self.skill_time))
            if height <= 0:
                self.skill_ready = True
                self.skill_time = None
            else:
                pygame.draw.rect(skill_bar, "white", ((0, height), (20, 45)))

        screen.blit(skill_bar, (840, 740))


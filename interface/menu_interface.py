import pygame
import os
import sys
from main_game import main_game



class MaimMenuInterface:
    def __init__(self, screen):
        self.screen = screen
        self.flag_screen_1 = True
        self.flag_screen_2 = False
        self.flag_screen_3 = False
        self.flag_screen_4 = False
        self.click = False
        self.character = None

    def update(self):
        if self.flag_screen_1:
            self.screen1()
        if self.flag_screen_2:
            self.screen2()
        if self.flag_screen_3:
            self.screen3()
        if self.flag_screen_4:
            self.screen4()

    def screen1(self):
        self.screen.fill("black")
        font = pygame.font.Font(None, 100)
        mx, my = pygame.mouse.get_pos()

        text = font.render(f"Главное меню", 1, "white")
        rect = text.get_rect(center=(700, 300))
        self.screen.blit(text, rect)


        buttons_font = pygame.font.Font(None, 50)

        button1 = pygame.Surface((400, 80))
        if 200 <= mx <= 600 and 500 <= my <= 580:
            if self.click:
                self.flag_screen_1 = False
                self.flag_screen_2 = True
                self.click = False
            button1.fill((165, 165, 165))
        else:
            button1.fill((220, 220, 220))
        button1_text = buttons_font.render(f"Начать Игру", 1, "white")
        button1.blit(button1_text, (95, 25))
        self.screen.blit(button1, (200, 500))

        button2 = pygame.Surface((400, 80))
        if 800 <= mx <= 1200 and 500 <= my <= 580:
            if self.click:
                self.flag_screen_1 = False
                self.flag_screen_4 = True
                self.click = False
            button2.fill((165, 165, 165))
        else:
            button2.fill((220, 220, 220))
        button2_text = buttons_font.render(f"Посмотреть статистику", 1, "white")
        button2.blit(button2_text, (5, 25))
        self.screen.blit(button2, (800, 500))

    def screen2(self):
        self.screen.fill("black")
        font = pygame.font.Font(None, 100)
        mx, my = pygame.mouse.get_pos()

        text = font.render(f"Выберите персонажа", 1, "white")
        rect = text.get_rect(center=(700, 300))
        self.screen.blit(text, rect)


        button1 = pygame.Surface((100, 100))
        if 500 <= mx <= 600 and 500 <= my <= 600:
            if self.click:
                self.flag_screen_2 = False
                self.flag_screen_3 = True
                self.click = False
                self.character = "Kiana"
            button1.fill((165, 165, 165))
        else:
            button1.fill((220, 220, 220))
        Kianaimage = self.load_image(f"Kiana/Kiana0.png")
        Kianaimage = pygame.transform.scale(Kianaimage, (100, 100))
        button1.blit(Kianaimage, (0, 0))
        self.screen.blit(button1, (500, 500))

        button2 = pygame.Surface((100, 100))
        if 800 <= mx <= 900 and 500 <= my <= 600:
            if self.click:
                self.flag_screen_2 = False
                self.flag_screen_3 = True
                self.click = False
                self.character = "Mei"
            button2.fill((165, 165, 165))
        else:
            button2.fill((220, 220, 220))
        Meiimage = self.load_image(f"Mei/Mei0.png")
        Meiimage = pygame.transform.scale(Meiimage, (100, 100))
        button2.blit(Meiimage, (0, 0))
        self.screen.blit(button2, (800, 500))



    def screen3(self):
        game_cycle = main_game(self.character)

        if game_cycle[0]:

            print(f'Вы прошли игру. Персонаж: {game_cycle[1]}.')
        else:
            print(f'Вы выживали {int(game_cycle[1])} секунд.')
        self.flag_screen_3 = False
        self.flag_screen_1 = True

    def screen4(self):
        pass

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/characters', name)
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

import pygame
import os
import sys
from main_game import main_game
import sqlite3



class MaimMenuInterface:
    def __init__(self, screen):
        self.screen = screen
        self.flag_slot_screen = True
        self.flag_screen_1 = False
        self.flag_screen_2 = False
        self.flag_screen_3 = False
        self.flag_screen_4 = False
        self.flag_screen_5 = False
        self.click = False
        self.character = None
        self.difficult = None
        self.last_game = None
        self.last_id = None

    def update(self):
        if self.flag_slot_screen:
            self.slot_screen()
        if self.flag_screen_1:
            self.screen1()
        if self.flag_screen_2:
            self.screen2()
        if self.flag_screen_3:
            self.screen3()
        if self.flag_screen_4:
            self.screen4()
        if self.flag_screen_5:
            self.screen5()

    def slot_screen(self):
        try:
            select_request = 'SELECT Id FROM Results'
            print(self.last_id)
            con = sqlite3.connect(f"data/data.db")
            cur = con.cursor()
            current_info = str(cur.execute(select_request).fetchall())

            print(current_info)

            self.screen.fill("black")
            font = pygame.font.Font(None, 100)
            mx, my = pygame.mouse.get_pos()

            text = font.render(f"Выберите файл сохранения", 1, "white")
            rect = text.get_rect(center=(700, 150))
            self.screen.blit(text, rect)

            buttons_font = pygame.font.Font(None, 50)

            button1 = pygame.Surface((300, 80))
            if 100 <= mx <= 400 and 350 <= my <= 430 and '1' in current_info:
                if self.click:
                    self.flag_slot_screen = False
                    self.flag_screen_1 = True
                    self.last_id = 1
                    self.click = False
                button1.fill((165, 165, 165))
            else:
                button1.fill((220, 220, 220))
            button1_text = buttons_font.render(f"Слот 1", 1, "black")
            button1.blit(button1_text, (95, 25))
            self.screen.blit(button1, (100, 350))

            ex1 = pygame.Surface((300, 80))
            if 100 <= mx <= 400 and 550 <= my <= 630:
                if self.click:
                    if '1' in current_info:
                        request = '''DELETE FROM Results WHERE Id == 1'''
                    else:
                        request = '''INSERT INTO Results VALUES (1, 0, 0)'''
                    cur.execute(request)
                    con.commit()
                    self.click = False
                ex1.fill((165, 165, 165))
            else:
                ex1.fill((220, 220, 220))
            if '1' in current_info:
                ex1_text = buttons_font.render(f"Удалить", 1, "red")
            else:
                ex1_text = buttons_font.render(f"Добавить", 1, "black")
            ex1.blit(ex1_text, (95, 25))
            self.screen.blit(ex1, (100, 550))

            button2 = pygame.Surface((300, 80))
            if 550 <= mx <= 850 and 350 <= my <= 430 and '2' in current_info:
                if self.click:
                    self.flag_slot_screen = False
                    self.flag_screen_1 = True
                    self.last_id = 2
                    self.click = False
                button2.fill((165, 165, 165))
            else:
                button2.fill((220, 220, 220))
            button2_text = buttons_font.render(f"Слот 2", 1, "black")
            button2.blit(button2_text, (95, 25))
            self.screen.blit(button2, (550, 350))

            ex2 = pygame.Surface((300, 80))
            if 550 <= mx <= 850 and 550 <= my <= 630:
                if self.click:
                    if '2' in current_info:
                        request = '''DELETE FROM Results WHERE Id == 2'''
                    else:
                        request = '''INSERT INTO Results VALUES (2, 0, 0)'''
                    cur.execute(request)
                    con.commit()
                    self.click = False
                ex2.fill((165, 165, 165))
            else:
                ex2.fill((220, 220, 220))
            if '2' in current_info:
                ex2_text = buttons_font.render(f"Удалить", 1, "red")
            else:
                ex2_text = buttons_font.render(f"Добавить", 1, "black")
            ex2.blit(ex2_text, (95, 25))
            self.screen.blit(ex2, (550, 550))

            button3 = pygame.Surface((300, 80))
            if 1000 <= mx <= 1300 and 350 <= my <= 430 and '3' in current_info:
                if self.click:
                    self.flag_slot_screen = False
                    self.flag_screen_1 = True
                    self.last_id = 3
                    self.click = False
                button3.fill((165, 165, 165))
            else:
                button3.fill((220, 220, 220))
            button3_text = buttons_font.render(f"Слот 3", 1, "black")
            button3.blit(button3_text, (95, 25))
            self.screen.blit(button3, (1000, 350))

            ex3 = pygame.Surface((300, 80))
            if 1000 <= mx <= 1300 and 550 <= my <= 630:
                if self.click:
                    if '3' in current_info:
                        request = '''DELETE FROM Results WHERE Id == 3'''
                    else:
                        request = '''INSERT INTO Results VALUES (3, 0, 0)'''
                    cur.execute(request)
                    con.commit()
                    self.click = False
                ex3.fill((165, 165, 165))
            else:
                ex3.fill((220, 220, 220))
            if '3' in current_info:
                ex3_text = buttons_font.render(f"Удалить", 1, "red")
            else:
                ex3_text = buttons_font.render(f"Добавить", 1, "black")
            ex3.blit(ex3_text, (95, 25))
            self.screen.blit(ex3, (1000, 550))

            con.close()

        except sqlite3.OperationalError:
            print('База данных не найдена')

    def screen1(self):
        self.screen.fill("black")
        font = pygame.font.Font(None, 100)
        mx, my = pygame.mouse.get_pos()

        text = font.render(f"Главное меню", 1, "white")
        rect = text.get_rect(center=(700, 300))
        self.screen.blit(text, rect)


        buttons_font = pygame.font.Font(None, 50)

        button1 = pygame.Surface((400, 80))
        self.character = None
        self.difficult = None
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
                self.flag_screen_5 = True
                self.click = False
            button2.fill((165, 165, 165))
        else:
            button2.fill((220, 220, 220))
        button2_text = buttons_font.render(f"Посмотреть статистику", 1, "white")
        button2.blit(button2_text, (5, 25))
        self.screen.blit(button2, (800, 500))

        button3 = pygame.Surface((120, 60))
        if 50 <= mx <= 170 and 700 <= my <= 760:
            if self.click:
                self.flag_screen_1 = False
                self.flag_slot_screen = True
                self.click = False
            button3.fill((165, 165, 165))
        else:
            button3.fill((220, 220, 220))
        button3_text = buttons_font.render(f"Назад", 1, "black")
        button3.blit(button3_text, (5, 25))
        self.screen.blit(button3, (50, 700))

    def screen2(self):
        self.screen.fill("black")
        font1 = pygame.font.Font(None, 80)
        font2 = pygame.font.Font(None, 40)
        mx, my = pygame.mouse.get_pos()

        text = font1.render(f"Выберите персонажа:", 1, "white")
        rect = text.get_rect(center=(400, 250))
        self.screen.blit(text, rect)


        button1 = pygame.Surface((100, 100))
        if 850 <= mx <= 950 and 190 <= my <= 290:
            if self.click:
                self.click = False
                self.character = "Kiana"
            button1.fill((165, 165, 165))
        elif self.character == "Kiana":
            button1.fill((165, 165, 165))
        else:
            button1.fill((220, 220, 220))
        Kianaimage = self.load_image(f"Kiana/Kiana0.png")
        Kianaimage = pygame.transform.scale(Kianaimage, (100, 100))
        button1.blit(Kianaimage, (0, 0))
        self.screen.blit(button1, (850, 190))

        button2 = pygame.Surface((100, 100))
        if 1100 <= mx <= 1200 and 190 <= my <= 290:
            if self.click:
                self.click = False
                self.character = 'Mei'
            button2.fill((165, 165, 165))
        elif self.character == "Mei":
            button2.fill((165, 165, 165))
        else:
            button2.fill((220, 220, 220))
        Meiimage = self.load_image(f"Mei/Mei0.png")
        Meiimage = pygame.transform.scale(Meiimage, (100, 100))
        button2.blit(Meiimage, (0, 0))
        self.screen.blit(button2, (1100, 190))


        text = font1.render(f"Выберите сложность:", 1, "white")
        rect = text.get_rect(center=(400, 540))
        self.screen.blit(text, rect)

        button3 = pygame.Surface((100, 40))
        if 850 <= mx <= 950 and 520 <= my <= 560:
            if self.click:
                self.click = False
                self.difficult = "Easy"
            button3.fill((165, 165, 165))
        elif self.difficult == "Easy":
            button3.fill((165, 165, 165))
        else:
            button3.fill((220, 220, 220))
        text = font2.render('Легко', 1, 'black')
        button3.blit(text, (0, 0))
        self.screen.blit(button3, (850, 520))

        button4 = pygame.Surface((120, 40))
        if 1100 <= mx <= 1220 and 520 <= my <= 560:
            if self.click:
                self.click = False
                self.difficult = "Hard"
            button4.fill((165, 165, 165))
        elif self.difficult == "Hard":
            button4.fill((165, 165, 165))
        else:
            button4.fill((220, 220, 220))
        text = font2.render('Сложно', 1, 'black')
        button4.blit(text, (0, 0))
        self.screen.blit(button4, (1100, 520))

        button5 = pygame.Surface((200, 40))
        if 1180 <= mx <= 1380 and 700 <= my <= 740:
            if self.click:
                if self.character and self.difficult:
                    self.click = False
                    self.flag_screen_2 = False
                    self.flag_screen_3 = True
            button5.fill((165, 165, 165))
        else:
            button5.fill((220, 220, 220))
        if self.character and self.difficult:
            text = font2.render('Начать игру', 1, 'black')
        else:
            text = font2.render('Начать игру', 1, 'red')
        button5.blit(text, (0, 0))
        self.screen.blit(button5, (1180, 700))

    def screen3(self):
        game_cycle = main_game(self.character, self.difficult)
        if game_cycle[0]:
            self.last_game = {
                'winning': True,
                'time': int(game_cycle[1])
            }

        else:
            self.last_game = {
                'winning': False,
                'time': int(game_cycle[1])
            }

        try:
            select_request = f'SELECT * FROM Results WHERE Id == {self.last_id}'
            con = sqlite3.connect(f"data/data.db")
            cur = con.cursor()
            current_info = cur.execute(select_request).fetchall()[0]

            all_games = int(current_info[1]) + 1
            winnings = int(current_info[2]) + game_cycle[0]

            update_request = f'''UPDATE Results SET AllRuns = "{all_games}",
                                WinningRuns = "{winnings}" WHERE Id == {self.last_id}'''

            cur.execute(update_request)
            con.commit()
            con.close()
        except sqlite3.OperationalError:
            print('База данных не найдена')

        self.flag_screen_3 = False
        self.flag_screen_4 = True

    def screen4(self):
        self.screen.fill("black")
        font1 = pygame.font.Font(None, 80)
        font2 = pygame.font.Font(None, 40)
        mx, my = pygame.mouse.get_pos()

        if self.last_game['winning']:
            text = font1.render(f"Вы прошли игру. Время прохождения: {self.last_game['time']}.", 1, "white")
        else:
            text = font1.render(f"Вы проиграли. Вы выживали {self.last_game['time']} сек.", 1, "white")

        rect = text.get_rect(center=(700, 300))
        self.screen.blit(text, rect)

        button1 = pygame.Surface((380, 40))
        if 500 <= mx <= 880 and 400 <= my <= 440:
            if self.click:
                self.click = False
                self.flag_screen_4 = False
                self.flag_screen_1 = True
            button1.fill((165, 165, 165))
        else:
            button1.fill((220, 220, 220))
        text = font2.render('Вернуться в главное меню', 1, 'black')
        button1.blit(text, (0, 0))
        self.screen.blit(button1, (500, 400))

    def screen5(self):
        self.screen.fill("black")
        font1 = pygame.font.Font(None, 80)
        font2 = pygame.font.Font(None, 40)
        mx, my = pygame.mouse.get_pos()

        try:
            select_request = f'SELECT * FROM Results WHERE Id == {self.last_id}'
            con = sqlite3.connect(f"data/data.db")
            current_info = con.cursor().execute(select_request).fetchall()[0]

            all_games = int(current_info[1])
            winnings = int(current_info[2])
            con.close()
        except sqlite3.OperationalError:
            print('База данных не найдена')

        text = font1.render( f'Всего игр: {all_games}, выиграно: {winnings}.', 1, "white")
        rect = text.get_rect(center=(700, 300))
        self.screen.blit(text, rect)

        button1 = pygame.Surface((380, 40))
        if 500 <= mx <= 880 and 400 <= my <= 440:
            if self.click:
                self.click = False
                self.flag_screen_5 = False
                self.flag_screen_1 = True
            button1.fill((165, 165, 165))
        else:
            button1.fill((220, 220, 220))
        text = font2.render('Вернуться в главное меню', 1, 'black')
        button1.blit(text, (0, 0))
        self.screen.blit(button1, (500, 400))

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

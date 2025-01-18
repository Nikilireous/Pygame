import pygame
import os
import sys
from main_game import main_game
import sqlite3
import hashlib


class MainMenuInterface:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size
        self.event = None
        self.click = False
        self.flag_auth = True
        self.flag_register = False
        self.flag_screen_1 = False
        self.flag_screen_2 = False
        self.flag_screen_3 = False
        self.flag_screen_4 = False
        self.flag_screen_5 = False
        self.current_user = None

        self.email_input_active = False
        self.password_input_active = False
        self.email_input = ""
        self.password_input = ""

        self.bad_auth = None
        self.bad_email = None
        self.bad_password = None

        self.character = None
        self.difficult = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def update(self, event):
        self.event = event
        if self.flag_auth:
            self.auth_screen()
        elif self.flag_register:
            self.register_screen()
        elif self.flag_screen_1:
            self.screen1()
        elif self.flag_screen_2:
            self.screen2()
        elif self.flag_screen_3:
            self.screen3()
        elif self.flag_screen_4:
            self.screen4()
        elif self.flag_screen_5:
            self.screen5()

    def auth_screen(self):
        self.screen.fill("black")
        font = pygame.font.Font(None, 50)
        mx, my = pygame.mouse.get_pos()

        title = font.render("Авторизация", True, "white")
        self.screen.blit(title, (600, 100))

        email_label = font.render("Email:", True, "white")
        self.screen.blit(email_label, (400, 200))

        password_label = font.render("Пароль:", True, "white")
        self.screen.blit(password_label, (400, 300))

        pygame.draw.rect(self.screen, "white", (550, 200, 400, 40))
        email_surface = font.render(self.email_input, True, "black")
        self.screen.blit(email_surface, (560, 205))

        pygame.draw.rect(self.screen, "white", (550, 300, 400, 40))
        password_surface = font.render("*" * len(self.password_input), True, "black")
        self.screen.blit(password_surface, (560, 305))

        login_button = pygame.Surface((250, 50))
        login_button.fill((165, 165, 165) if 600 <= mx <= 850 and 400 <= my <= 450 else (220, 220, 220))
        login_text = font.render("Войти", True, "black")
        login_button.blit(login_text, (70, 10))
        self.screen.blit(login_button, (600, 400))

        register_button = pygame.Surface((250, 50))
        register_button.fill((165, 165, 165) if 600 <= mx <= 850 and 500 <= my <= 550 else (220, 220, 220))
        register_text = font.render("Регистрация", True, "black")
        register_button.blit(register_text, (20, 10))
        self.screen.blit(register_button, (600, 500))

        if self.bad_auth:
            font1 = pygame.font.Font(None, 25)
            error_surface = font1.render(self.bad_auth, True, "red")
            self.screen.blit(error_surface, (610, 380))

        if self.click:
            self.click = False
            if 600 <= mx <= 850 and 400 <= my <= 450:
                self.authenticate_user()
            elif 600 <= mx <= 850 and 500 <= my <= 550:
                self.flag_auth = False
                self.flag_register = True
                self.email_input = ""
                self.password_input = ""
            elif 550 <= mx <= 950 and 200 <= my <= 240:
                self.email_input_active = True
                self.password_input_active = False
            elif 550 <= mx <= 950 and 300 <= my <= 340:
                self.email_input_active = False
                self.password_input_active = True
            else:
                self.email_input_active = False
                self.password_input_active = False

        if self.email_input_active or self.password_input_active:
            if self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_BACKSPACE:
                    if self.email_input_active:
                        self.email_input = self.email_input[:-1]
                    elif self.password_input_active:
                        self.password_input = self.password_input[:-1]
                elif self.email_input_active:
                    self.email_input += self.event.unicode
                    self.bad_auth = None
                elif self.password_input_active:
                    self.bad_auth = None
                    self.password_input += self.event.unicode

    def authenticate_user(self):
        con = sqlite3.connect("data/users.db")
        cur = con.cursor()
        hashed_password = self.hash_password(self.password_input)
        user = cur.execute("SELECT * FROM Users WHERE email = ? AND password = ?",
                           (self.email_input, hashed_password)).fetchone()
        con.close()

        if user:
            self.current_user = user[1]
            self.flag_auth = False
            self.flag_screen_1 = True
            self.bad_auth = None
            self.password_input = ""
            self.email_input = ""
        else:
            self.bad_auth = "Неверный email или пароль"

    def register_screen(self):
        self.screen.fill("black")
        font = pygame.font.Font(None, 50)
        mx, my = pygame.mouse.get_pos()

        title = font.render("Регистрация", True, "white")
        self.screen.blit(title, (600, 100))

        email_label = font.render("Email:", True, "white")
        self.screen.blit(email_label, (400, 200))

        password_label = font.render("Пароль:", True, "white")
        self.screen.blit(password_label, (400, 300))

        pygame.draw.rect(self.screen, "white", (550, 200, 400, 40))
        email_surface = font.render(self.email_input, True, "black")
        self.screen.blit(email_surface, (560, 205))

        pygame.draw.rect(self.screen, "white", (550, 300, 400, 40))
        password_surface = font.render("*" * len(self.password_input), True, "black")
        self.screen.blit(password_surface, (560, 305))

        register_button = pygame.Surface((360, 50))
        register_button.fill((165, 165, 165) if 545 <= mx <= 905 and 400 <= my <= 450 else (220, 220, 220))
        register_text = font.render("Зарегистрироваться", True, "black")
        register_button.blit(register_text, (10, 10))
        self.screen.blit(register_button, (545, 400))

        back_button = pygame.Surface((250, 50))
        back_button.fill((165, 165, 165) if 600 <= mx <= 850 and 500 <= my <= 550 else (220, 220, 220))
        back_text = font.render("Назад", True, "black")
        back_button.blit(back_text, (60, 10))
        self.screen.blit(back_button, (600, 500))

        if self.bad_email:
            font1 = pygame.font.Font(None, 25)
            error_surface = font1.render(self.bad_email, True, "red")
            self.screen.blit(error_surface, (960, 200))

        if self.bad_password:
            font1 = pygame.font.Font(None, 25)
            error_surface = font1.render(self.bad_password, True, "red")
            self.screen.blit(error_surface, (960, 300))

        if self.click:
            self.click = False
            if 545 <= mx <= 905 and 400 <= my <= 450:
                self.register_user()
            elif 600 <= mx <= 850 and 500 <= my <= 550:
                self.flag_register = False
                self.flag_auth = True
            elif 550 <= mx <= 950 and 200 <= my <= 240:
                self.email_input_active = True
                self.password_input_active = False
            elif 550 <= mx <= 950 and 300 <= my <= 340:
                self.email_input_active = False
                self.password_input_active = True
            else:
                self.email_input_active = False
                self.password_input_active = False

        if self.email_input_active or self.password_input_active:
            if self.event.type == pygame.KEYDOWN:
                if self.event.key == pygame.K_BACKSPACE:
                    if self.email_input_active:
                        self.bad_email = None
                        self.bad_password = None
                        self.email_input = self.email_input[:-1]
                    elif self.password_input_active:
                        self.bad_email = None
                        self.bad_password = None
                        self.password_input = self.password_input[:-1]
                elif self.email_input_active:
                    self.bad_email = None
                    self.bad_password = None
                    self.email_input += self.event.unicode
                elif self.password_input_active:
                    self.bad_email = None
                    self.bad_password = None
                    self.password_input += self.event.unicode

    def register_user(self):
        if self.register_requrments():
            con = sqlite3.connect("data/users.db")
            cur = con.cursor()
            hashed_password = self.hash_password(self.password_input)
            try:
                cur.execute("INSERT INTO Users (email, password) VALUES (?, ?)", (self.email_input, hashed_password))
                con.commit()
                self.flag_register = False
                self.flag_screen_1 = True
                self.email_input = ""
                self.password_input = ""
            finally:
                con.close()

    def register_requrments(self):
        if ("@" not in self.email_input) or (len(self.email_input) < 10):
            self.bad_email = "Некорректный Email"
            return False

        if any([self.password_input.isdigit(), self.password_input.isalpha(),
                self.password_input.isupper(), self.password_input.islower(),
                self.password_input == ""]):
            if self.password_input.isdigit():
                self.bad_password = "Пароль не должен состоять только из цыфр"
            elif self.password_input.isalpha():
                self.bad_password = "Пароль не должен состоять только из букв"
            elif self.password_input.isupper():
                self.bad_password = "Пароль не должен состоять только из заглавных букв"
            elif self.password_input.islower():
                self.bad_password = "Пароль не должен состоять только из маленьких букв"
            elif self.password_input == "":
                self.bad_password = "Пароль не должен состоять быть пустым"
            return False
        return True

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
                self.flag_screen_5 = True
                self.click = False
            button2.fill((165, 165, 165))
        else:
            button2.fill((220, 220, 220))
        button2_text = buttons_font.render(f"Посмотреть статистику", 1, "white")
        button2.blit(button2_text, (5, 25))
        self.screen.blit(button2, (800, 500))

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
        game_cycle = main_game(self.character, self.size, self.difficult)
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
            select_request = 'SELECT * FROM Results'
            con = sqlite3.connect(f"data/data.db")
            cur = con.cursor()
            current_info = cur.execute(select_request).fetchall()[0]

            all_games = int(current_info[1]) + 1
            winnings = int(current_info[2]) + game_cycle[0]

            update_request = f'UPDATE Results SET AllRuns = "{all_games}", WinningRuns = "{winnings}" WHERE Id == 1'
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
            select_request = 'SELECT * FROM Results'
            con = sqlite3.connect(f"data/data.db")
            current_info = con.cursor().execute(select_request).fetchall()[0]

            all_games = int(current_info[1])
            winnings = int(current_info[2])
            con.close()
        except sqlite3.OperationalError:
            print('База данных не найдена')

        text = font1.render(f'Всего игр: {all_games}, выиграно: {winnings}.', 1, "white")
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

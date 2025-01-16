import random
from enemies.spider import Spider
from enemies.witch import Witch
from enemies.boss import Boss


class Events:
    def __init__(self, difficult, fps, flightless_data, player, spider_sprites, witch_sprites, boss_sprites):
        self.difficult = difficult
        self.fps = fps
        self.flightless_data = flightless_data
        self.player = player
        self.spider_sprites = spider_sprites
        self.witch_sprites = witch_sprites
        self.boss_sprites = boss_sprites
        self.boss_alive = False

    def spawn_enemies(self, enemy, max_enemies, camera_pos, available_range):
        for quantity in range(random.randint(0, max_enemies)):
            side = random.choice(['x', 'y'])

            if side == 'x':
                x = random.randint(*available_range[0])
                y = random.choice(available_range[1])

            else:
                x = random.choice(available_range[0])
                y = random.randint(*available_range[1])

            if enemy is Spider:
                current_enemy = enemy(self.spider_sprites, fps=self.fps, map_data=self.flightless_data,
                                      player=self.player, x=(x - camera_pos[0]), y=(y - camera_pos[1]),
                                      difficult=self.difficult)

            if enemy is Witch:
                current_enemy = enemy(self.witch_sprites, fps=self.fps, player=self.player,
                                      x=(x - camera_pos[0]), y=(y - camera_pos[1]), difficult=self.difficult)

            if enemy is Boss:
                current_enemy = enemy(self.boss_sprites, fps=self.fps, map_data=self.flightless_data,
                                      player=self.player, x=(x - camera_pos[0]), y=(y - camera_pos[1]),
                                      summons=self.spider_sprites, difficult=self.difficult)

    def phases(self, camera_pos, current_time, borders, spiders, witches, bosses):
        if self.difficult == 'Easy':
            if current_time <= 90:
                if len(spiders) < 40:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 990:
                        self.spawn_enemies(
                            enemy=Spider, max_enemies=1,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 90 < current_time <= 180:
                if len(spiders) < 85:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 980:
                        self.spawn_enemies(
                            enemy=Spider, max_enemies=2,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 180 < current_time <= 270:
                if len(spiders) < 50:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 900:
                        self.spawn_enemies(
                            enemy=Spider, max_enemies=4,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 270 < current_time <= 360:
                if len(witches) < 20:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 995:
                        self.spawn_enemies(
                            enemy=Witch, max_enemies=2,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 360 < current_time and not self.boss_alive:
                if len(bosses) < 1:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 0:
                        self.spawn_enemies(
                            enemy=Boss, max_enemies=1,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))
                if len(bosses) == 1:
                    self.boss_alive = True

            if 370 < current_time and len(self.boss_sprites) == 0 and self.boss_alive:
                return True

        if self.difficult == 'Hard':
            if current_time <= 60:
                if len(spiders) < 60:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 990:
                        self.spawn_enemies(
                            enemy=Spider, max_enemies=1,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 60 < current_time <= 120:
                if len(spiders) < 110:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 980:
                        self.spawn_enemies(
                            enemy=Spider, max_enemies=2,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 120 < current_time <= 180:
                if len(spiders) < 70:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 675:
                        self.spawn_enemies(
                            enemy=Spider, max_enemies=5,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 180 < current_time <= 240:
                if len(witches) < 35:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 990:
                        self.spawn_enemies(
                            enemy=Witch, max_enemies=2,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))

            if 270 < current_time and not self.boss_alive:
                if len(bosses) < 1:
                    spawn_chance = random.randint(1, 1000)
                    if spawn_chance > 0:
                        self.spawn_enemies(
                            enemy=Boss, max_enemies=1,
                            camera_pos=camera_pos, available_range=(borders[:2], borders[2:]))
                if len(bosses) == 1:
                    self.boss_alive = True

            if 280 < current_time and  len(self.boss_sprites) == 0 and self.boss_alive:
                return True

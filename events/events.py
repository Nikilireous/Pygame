import random
from enemies.spider import Spider
from enemies.witch import Witch


class Events:
    def __init__(self, fps, flightless_data, player, spider_sprites, witch_sprites):
        self.fps = fps
        self.flightless_data = flightless_data
        self.player = player
        self.spider_sprites = spider_sprites
        self.witch_sprites = witch_sprites

    def spawn_enemies(self, enemy, camera_pos, available_range):
        for quantity in range(random.randint(0, 2)):
            side = random.choice(['x', 'y'])

            if side == 'x':
                x = random.randint(*available_range[0])
                y = random.choice(available_range[1])

            else:
                x = random.choice(available_range[0])
                y = random.randint(*available_range[1])

            if enemy is Spider:
                current_enemy = enemy(self.spider_sprites, fps=self.fps, map_data=self.flightless_data,
                                  player=self.player, x=(x - camera_pos[0]), y=(y - camera_pos[1]))

            if enemy is Witch:
                current_enemy = enemy(self.witch_sprites, fps=self.fps, map_data=self.flightless_data,
                                  player=self.player, x=(x - camera_pos[0]), y=(y - camera_pos[1]))

import pygame
import os


class Map:
    def __init__(self, fps, player):
        self.TILE_SIZE = 128
        self.player = player
        self.tiles = self.load_tiles()
        self.change = [0, 0]
        self.fps = fps
        with open("maps/map_number_1") as file:
            player_pos = list(map(int, file.readline().split()))
            self.map_data = list(map(lambda x: list(map(int, x.split())), file.readlines()))
            self.player_x = player_pos[0] * self.TILE_SIZE + 64
            self.player_y = player_pos[1] * self.TILE_SIZE + 64

        self.flightless_map = []
        for y in range(len(self.map_data)):
            row = []
            for x in range(len(self.map_data[y])):
                if self.map_data[y][x] in [0, 4]:
                    row.append(1)
                else:
                    row.append(0)
            self.flightless_map.append(row)

    def load_tiles(self):
        tiles = {
            0: pygame.image.load(os.path.join("images/tiles", "grass.png")),
            1: pygame.image.load(os.path.join("images/tiles", "wall.png")),
            2: pygame.image.load(os.path.join("images/tiles", "water.png")),
            3: pygame.image.load(os.path.join("images/tiles", "lava.png")),
            4: pygame.image.load(os.path.join("images/tiles", "earth.png"))
        }
        for key in tiles:
            tiles[key] = pygame.transform.scale(tiles[key], (self.TILE_SIZE, self.TILE_SIZE))
        return tiles

    def draw_map(self, screen, camera_x, camera_y):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                screen_x = x * self.TILE_SIZE - camera_x
                screen_y = y * self.TILE_SIZE - camera_y

                if -self.TILE_SIZE < screen_x < screen.get_width() and -self.TILE_SIZE < screen_y < screen.get_height():
                    screen.blit(self.tiles[tile], (screen_x, screen_y))

    def update(self, screen):
        self.change = [0, 0]
        speed = self.player.move_speed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Движение Вверх
            pos1, pos2 = (self.player_y - 30 - speed, self.player_x - 10), (
                self.player_y - 30 - speed, self.player_x + 10)
            if self.step_condition(pos1, pos2):
                self.player_y -= speed
                self.change[1] -= speed

        if keys[pygame.K_s]:  # Движение Вниз
            pos1, pos2 = (self.player_y + 35 + speed, self.player_x - 10), (
                self.player_y + 35 + speed, self.player_x + 10)
            if self.step_condition(pos1, pos2):
                self.player_y += speed
                self.change[1] += speed

        if keys[pygame.K_a]:  # Движение Влево
            pos1, pos2 = (self.player_y - 30, self.player_x - 10 - speed), (
                self.player_y + 35, self.player_x - 10 - speed)
            if self.step_condition(pos1, pos2):
                self.player_x -= speed
                self.change[0] -= speed

        if keys[pygame.K_d]:  # Движение Вправо
            pos1, pos2 = (self.player_y - 30, self.player_x + 10 + speed), (
                self.player_y + 35, self.player_x + 10 + speed)
            if self.step_condition(pos1, pos2):
                self.player_x += speed
                self.change[0] += speed

        camera_x = self.player_x - screen.get_width() // 2
        camera_y = self.player_y - screen.get_height() // 2
        self.draw_map(screen, camera_x, camera_y)

    def step_condition(self, pos1, pos2):
        for i in (pos1, pos2):
            player_in_tiles_cor = (i[0] // self.TILE_SIZE, i[1] // self.TILE_SIZE)
            if self.map_data[player_in_tiles_cor[0]][player_in_tiles_cor[1]] not in [0, 4]:
                return False
        return True

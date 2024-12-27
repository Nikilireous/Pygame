import pygame
import os


class Map:
    def __init__(self, player_pos):
        self.TILE_SIZE = 128
        self.player_x = player_pos[0]
        self.player_y = player_pos[1]
        self.tiles = self.load_tiles()
        self.map_data = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 2, 0, 0, 2, 2, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 0, 0, 2, 2, 0, 0, 0, 1],
            [1, 0, 0, 0, 2, 2, 0, 0, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 2, 0, 1],
            [1, 0, 2, 2, 0, 0, 2, 2, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

    def load_tiles(self):
        tiles = {
            0: pygame.image.load(os.path.join("images", "tiles", "grass.png")),
            1: pygame.image.load(os.path.join("images", "tiles", "wall.png")),
            2: pygame.image.load(os.path.join("images", "tiles", "water.png"))
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
        speed = 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.step_condition(self.player_x, self.player_y - speed - 40, "top"):
                self.player_y -= speed
        if keys[pygame.K_s]:
            if self.step_condition(self.player_x, self.player_y + speed + 40, "bot"):
                self.player_y += speed
        if keys[pygame.K_a]:
            if self.step_condition(self.player_x - speed - 40, self.player_y, "left"):
                self.player_x -= speed
        if keys[pygame.K_d]:
            if self.step_condition(self.player_x + speed + 40, self.player_y, "right"):
                self.player_x += speed

        camera_x = self.player_x - screen.get_width() // 2
        camera_y = self.player_y - screen.get_height() // 2
        self.draw_map(screen, camera_x, camera_y)

    def step_condition(self, pos1, pos2, direction):
        if direction == "top":
            player_in_tiles_cor = (pos1 // self.TILE_SIZE, pos2 // self.TILE_SIZE)
            if self.map_data[player_in_tiles_cor[0]][player_in_tiles_cor[1]] == 0:
                return True
            return False


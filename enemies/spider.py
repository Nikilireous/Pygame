import pygame
import sys
import os
import math
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Spider(pygame.sprite.Sprite):
    def __init__(self, *group, fps, map_data, player):
        super().__init__(*group)
        self.frames = [f"pauk{i}.png" for i in range(11)]
        self.fps = fps
        self.player = player
        self.map_data = map_data
        self.cur_frame = 0
        self.image = self.load_image(self.frames[self.cur_frame])
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 650, 700
        self.movement_type = 'vector'
        self.matrix_timer = self.fps * 3
        self.speed = 2
        self.clock = 0

    def get_legs_coords(self, camera_x, camera_y, tile_size):
        left_x = (self.rect.x + camera_x) // tile_size
        right_x = (self.rect.x + 80 + camera_x) // tile_size
        map_y = (self.rect.y + camera_y) // tile_size
        return (left_x, map_y), (right_x, map_y)

    def get_center_coords(self, camera_x, camera_y, tile_size):
        centre_x = (camera_x + self.rect.centerx) // tile_size
        center_y = (camera_y + self.rect.centery) // tile_size
        return centre_x, center_y

    def vector_move(self, player, change, camera_pos):
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)

        try:
            dx, dy = (dx / dist * self.speed), (dy / dist * self.speed)
            for coords in self.get_legs_coords(camera_pos[0] + int(dx) - change[0],
                                              camera_pos[1] + int(dy) - change[1],
                                              128):

                if self.map_data[coords[0]][coords[1]] in [0]:
                    self.movement_type = 'matrix'

            if self.movement_type == 'vector':
                self.rect.x += dx - change[0]
                self.rect.y += dy - change[1]
            else:
                self.rect.x -= change[0]
                self.rect.y -= change[1]

        except ZeroDivisionError:
            pass

    def matrix_move(self, player, change, camera_pos):
        grid = Grid(matrix=self.map_data)
        start = self.get_center_coords(camera_pos[0], camera_pos[1], 128)
        end = (camera_pos[0] + 700) // 128, (camera_pos[1] + 400) // 128

        start = grid.node(start[0], start[1])
        end = grid.node(end[0], end[1])


        finder = AStarFinder()
        path, runs = finder.find_path(start, end, grid)

        try:
            next_cell = list(path[1])
            next_x, next_y = ((next_cell[0]) * 128 + (128 // 2)), ((next_cell[1]) * 128 + (128 // 2))

            dx, dy = (next_x - camera_pos[0]) - self.rect.centerx, (next_y - camera_pos[1]) - self.rect.centery
            dist = math.hypot(dx, dy)

            try:
                dx, dy = (dx / dist * self.speed), (dy / dist * self.speed)
                self.rect.x += dx - change[0]
                self.rect.y += dy - change[1]


            except ZeroDivisionError:
                pass

        except IndexError:
            self.movement_type = 'vector'
            pass

    def update(self, change, camera_pos):
        print(self.movement_type)
        if self.movement_type == 'vector':
            self.vector_move(self.player, change, camera_pos)

        if self.movement_type == 'matrix':
            self.matrix_move(self.player, change, camera_pos)

            if self.matrix_timer == 0:
                self.movement_type = 'vector'
                self.matrix_timer = self.fps * 3
            else:
                self.matrix_timer -= 1

        if self.clock == 250 // self.fps:
            dx, dy = (self.player.rect.x - self.rect.x), (self.player.rect.y - self.rect.y)
            self.clock = 0
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.load_image(self.frames[self.cur_frame])
            self.image = pygame.transform.scale(self.image, (100, 100))

            angle = math.degrees(math.atan2(-dx, dy))
            self.image = pygame.transform.rotate(self.image, -angle)
        else:
            self.clock += 1

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images/enemies/pauk', name)
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

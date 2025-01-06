import pygame
from map import Map
from characters.Kiana.kiana import Kiana
from characters.Kiana.skillset import KianaBaseAttack, KianaSkillE
from characters.Mei.mei import Mei
from characters.Mei.skillset import MeiBaseAttack, MeiSkillE
from enemies.spider import Spider
from events.events import Events
from interface.interface import Interface
import random
import time


def main():
    pygame.init()
    # pygame.mixer.init()
    # pygame.mixer.music.load('Audio/background_music_2.mp3')
    # pygame.mixer.music.set_volume(1)
    # pygame.mixer.music.play(-1)
    size = 1400, 800
    fps = 100
    main_map = Map(fps)
    main_map_data = main_map.map_data
    main_map_flightless_data = main_map.flightless_map
    tile_size = main_map.TILE_SIZE
    right_border = 6 * tile_size + tile_size // 2
    left_border = (len(main_map_data[0]) - 7) * tile_size - tile_size // 2
    upper_border = 3 * tile_size + tile_size // 2
    lower_border = (len(main_map_data) - 4) * tile_size - tile_size // 2

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Kiana_game")

    character_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    visible_enemies = pygame.sprite.Group()
    spider_sprites = pygame.sprite.Group()
    skill_sprites = pygame.sprite.Group()

    character = Kiana(character_sprites, fps=fps)
    interface = Interface(character)

    events = Events(fps=fps, flightless_data=main_map_flightless_data, player=character,
                    spider_sprites=spider_sprites)

    clock = pygame.time.Clock()
    laser_clock = 0
    skill = True
    seconds_to_shoot = 0
    fire = False
    running = True
    while running:
        player_pos = (main_map.player_x, main_map.player_y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                fire = True
            if event.type == pygame.MOUSEBUTTONUP:
                fire = False
                seconds_to_shoot = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and skill:
                    KianaSkillE(skill_sprites, fps=fps, player=character)
                    skill = False
                    laser_clock = time.time()

        if fire:
            if seconds_to_shoot == fps // 10:
                seconds_to_shoot = 0
                x, y = size[0] // 2, size[1] // 2
                KianaBaseAttack(bullet_sprites, x=x, y=y, fps=fps, map_data=main_map_data, player_pos=player_pos)
            else:
                seconds_to_shoot += 1

        if time.time() - laser_clock >= 23:
            skill = True

        screen.fill(0)
        main_map.update(screen)
        all_change = main_map.change
        camera_pos = (main_map.player_x - size[0] // 2, main_map.player_y - size[1] // 2)
        visible_enemies = pygame.sprite.Group()

        if len(spider_sprites) < 150:
            spawn_chance = random.randint(1, 100)
            if spawn_chance > 98:
                events.spawn_enemies(
                    enemy=Spider,
                    camera_pos=camera_pos, available_range=((right_border, left_border), (upper_border, lower_border))
                )

        spider_sprites.update(change=all_change, camera_pos=camera_pos, visible_sprites=visible_enemies)
        visible_enemies.draw(screen)

        character_sprites.update(visible_sprites=visible_enemies)
        character_sprites.draw(screen)

        bullet_sprites.update(change=all_change, camera_pos=camera_pos, enemies_group=visible_enemies, player=character)
        bullet_sprites.draw(screen)

        skill_sprites.update(enemies_group=visible_enemies)
        skill_sprites.draw(screen)

        interface.draw_interface(screen)

        pygame.display.flip()
        clock.tick(fps)

        if character.HP <= 0:
            print("Вас убили!")
            running = False

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()

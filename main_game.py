import pygame
from map import Map
from characters.Kiana.kiana import Kiana
from characters.Kiana.skillset import KianaBaseAttack
from enemies.spider import Spider


def main():
    pygame.init()
    # pygame.mixer.init()
    # pygame.mixer.music.load('Audio/background_music.mp3')
    # pygame.mixer.music.set_volume(1)
    # pygame.mixer.music.play(-1)
    size = 1400, 800
    fps = 100
    main_map = Map(fps)
    main_map_data = main_map.map_data
    flightless_data = main_map.flightless_map
    flightless_tiles = main_map.flightless_sprite_group

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Kiana_game")

    character_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    spider_sprites = pygame.sprite.Group()

    kiana_character = Kiana(character_sprites, fps=fps)
    Spider(spider_sprites, fps=fps, map_data=flightless_data, tiles_data=flightless_tiles, player=kiana_character)

    clock = pygame.time.Clock()
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

        if fire:
            if seconds_to_shoot == fps // 10:
                seconds_to_shoot = 0
                x, y = size[0] // 2, size[1] // 2  #Позиция центра экрана
                KianaBaseAttack(bullet_sprites, x=x, y=y, fps=fps, map_data=main_map_data, player_pos=player_pos)
            else:
                seconds_to_shoot += 1

        screen.fill(0)
        main_map.update(screen)
        flightless_tiles = main_map.flightless_sprite_group
        all_change = main_map.change
        camera_pos = (main_map.player_x - size[0] // 2, main_map.player_y - size[1] // 2)

        character_sprites.update()
        character_sprites.draw(screen)

        bullet_sprites.update(change=all_change, camera_pos=camera_pos, enemies_group=spider_sprites)
        bullet_sprites.draw(screen)

        spider_sprites.update(change=all_change, camera_pos=camera_pos, tiles_data=flightless_tiles)
        spider_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
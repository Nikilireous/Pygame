import pygame
from map import Map
from characters.Kiana.kiana import Kiana
from characters.Kiana.skillset import KianaBaseAttack, KianaSkillE
from characters.Mei.mei import Mei
from characters.Mei.skillset import MeiBaseAttack, MeiSkillE
from enemies.spider import Spider
from enemies.witch import Witch
from enemies.boss import Boss
from events.events import Events
from interface.game_interface import Interface
import random
import time


def character_choice(group, fps, size):
    name = input("Выберите персонажа. (Mei, Kiana): ")
    while True:
        if name == "Mei":
            return Mei(group, fps=fps, size=size), name
        elif name == "Kiana":
            return Kiana(group, fps=fps, size=size), name
        else:
            name = input("Такого персонажа не существует. Выберите одного из предложенных. (Mei, Kiana): ")


def main_game(char, size0, difficult):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Audio/background_music_2.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    size = size0

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("honkai impact 4th")

    character_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    visible_enemies = pygame.sprite.Group()
    spider_sprites = pygame.sprite.Group()
    witch_sprites = pygame.sprite.Group()
    boss_sprites = pygame.sprite.Group()
    skill_sprites = pygame.sprite.Group()

    info = pygame.display.Info()

    if char:
        character, character_name = eval(char)(character_sprites, size=size), char
    else:
        character, character_name = character_choice(group=character_sprites, size=size)

    main_map = Map(character, difficult)
    main_map_data = main_map.map_data
    main_map_flightless_data = main_map.flightless_map
    tile_size = main_map.TILE_SIZE
    right_border = 6 * tile_size + tile_size // 2
    left_border = (len(main_map_data[0]) - 7) * tile_size - tile_size // 2
    upper_border = 3 * tile_size + tile_size // 2
    lower_border = (len(main_map_data) - 4) * tile_size - tile_size // 2
    interface = Interface(character)
    interface.get_info()

    events = Events(difficult=difficult, flightless_data=main_map_flightless_data, player=character,
                    spider_sprites=spider_sprites, witch_sprites=witch_sprites, boss_sprites=boss_sprites)

    clock = pygame.time.Clock()
    skill_clock = 0
    skill = True
    seconds_to_shoot = 0
    fire = False
    mei_skill_duration = False
    mei_skill_time = 0
    running = True

    deltaTime = 0

    while running:
        currTime = time.time()
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
                    if character_name == "Kiana":
                        KianaSkillE(skill_sprites, player=character, res=[info.current_w, info.current_h])
                    elif character_name == "Mei":
                        character.HP -= 5
                        skill_damage = character.skill_damage
                        character.base_atk_damage += skill_damage
                        mei_skill = MeiSkillE(player=character, map=main_map, enemy=visible_enemies,
                                              resolution=[info.current_w, info.current_h])
                        mei_skill_duration = True
                    interface.skill_start = True
                    skill = False
                    skill_clock = time.time()

        if fire:
            if character_name == "Kiana":
                seconds_to_shoot += deltaTime
                if seconds_to_shoot >= 0.1:
                    seconds_to_shoot = 0
                    x, y = size[0] // 2, size[1] // 2
                    KianaBaseAttack(bullet_sprites, x=x, y=y, map_data=main_map_data, player_pos=player_pos,
                                    player=character)

            elif character_name == "Mei":
                if seconds_to_shoot == 50:
                    seconds_to_shoot = 0
                    MeiBaseAttack(bullet_sprites,  player=character, res=[info.current_w, info.current_h])
                else:
                    seconds_to_shoot += 1

        if time.time() - skill_clock >= character.skill_recharge and not skill:
            if character_name == "Mei":
                character.base_atk_damage -= skill_damage
            skill = True

        if mei_skill_duration:
            if mei_skill_time == 20:
                mei_skill_duration = False
                mei_skill_time = 0
            else:
                mei_skill.dash()
                mei_skill_time += 1

        screen.fill(0)
        main_map.update(screen, deltaTime)
        all_change = main_map.change
        camera_pos = (main_map.player_x - size[0] // 2, main_map.player_y - size[1] // 2)
        visible_enemies = pygame.sprite.Group()

        interface.timer(screen)

        phases = events.phases(camera_pos=camera_pos, current_time=interface.current_time,
                               borders=(right_border, left_border, upper_border, lower_border),
                               spiders=spider_sprites, witches=witch_sprites, bosses=boss_sprites)

        if phases:
            pygame.mixer.music.stop()
            return True, interface.current_time

        spider_sprites.update(change=all_change, camera_pos=camera_pos, visible_sprites=visible_enemies, dt=deltaTime)
        witch_sprites.update(change=all_change, player=character, visible_sprites=visible_enemies, dt=deltaTime)
        boss_sprites.update(change=all_change, player=character, visible_sprites=visible_enemies, screen=screen,
                            dt=deltaTime)
        visible_enemies.draw(screen)

        character_sprites.update(visible_sprites=visible_enemies, dt=deltaTime)
        character_sprites.draw(screen)

        bullet_sprites.update(change=all_change, camera_pos=camera_pos, enemies_group=visible_enemies, dt=deltaTime)
        bullet_sprites.draw(screen)

        skill_sprites.update(enemy_group=visible_enemies, deltaTime=deltaTime, screen=screen)
        skill_sprites.draw(screen)

        interface.draw_interface(screen)

        if character.HP <= 0:
            pygame.mixer.music.stop()
            return False, interface.current_time
        pygame.display.flip()

        deltaTime = time.time() - currTime

    pygame.mixer.music.stop()
    return False, interface.current_time


if __name__ == "__main__":
    main_game(None)

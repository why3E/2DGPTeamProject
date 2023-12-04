from pico2d import *

import game_world
import item_mode
import title_mode
from background import Background
from main_character import Main_Character
import game_framework
from monster import Ghost, Slime, Skeleton


# Game object class here

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            game_framework.push_mode(item_mode)
            pass
        else:
            main_character.handle_event(event)


def init():
    global background
    global main_character
    global start_time
    global play_check
    global paturn_time
    global elapsed_time
    global monster_count
    monster_count = 10
    play_check = True
    start_time = get_time() + 1
    elapsed_time = get_time() + 1
    paturn_time = 2

    background = Background()
    game_world.add_object(background, 0)

    main_character = Main_Character()
    game_world.add_object(main_character, 1)
    game_world.add_collision_pair('main_character:monster', None, main_character)
    game_world.add_collision_pair('Main:Coin', main_character, None)
    # 메인 캐릭터 초기값을 json이나 피클로 초기화 해서 파일 읽어들이는 걸로 수정해야함


def update():
    global start_time
    global paturn_time
    global elapsed_time
    global monster_count

    if main_character.hp <= 0:
        game_world.clear()
        game_framework.change_mode(title_mode)

    game_world.update()
    game_world.handle_collisions()

    current_time = get_time()

    if int(current_time - elapsed_time) >= 20:  # 100초가 경과했는지 확인
        elapsed_time = current_time  # 경과 시간 초기화
        monster_count += 1
        print('패턴')  # 패턴 주기를 10초로 변경
        if monster_count == 14:
            game_framework.change_mode(title_mode)
    if int((current_time - start_time) / paturn_time) > 0:
        start_time = current_time
        for i in range(monster_count):
            monster_make()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    global play_check
    play_check = False
    pass


def resume():
    global play_check
    play_check = True
    pass


def monster_make():
    global monster_count

    skeleton = Skeleton(monster_count*5)
    slime = Slime(monster_count*5)
    ghost = Ghost(monster_count*5)

    game_world.add_object(ghost, 1)
    game_world.add_collision_pair('main_character:monster', ghost, None)
    game_world.add_collision_pair('atk:monster', ghost, None)

    game_world.add_object(slime, 1)
    game_world.add_collision_pair('main_character:monster', slime, None)
    game_world.add_collision_pair('atk:monster', slime, None)

    game_world.add_object(skeleton, 1)
    game_world.add_collision_pair('main_character:monster', skeleton, None)
    game_world.add_collision_pair('atk:monster', skeleton, None)

    if monster_count > 5:
        game_world.add_collision_pair('ghost:skeleton', ghost, None)
        game_world.add_collision_pair('ghost:skeleton', None, skeleton)

        game_world.add_collision_pair('slime:skeleton', None, slime)
        game_world.add_collision_pair('slime:skeleton', skeleton, None)

        game_world.add_collision_pair('ghost:slime', slime, None)
        game_world.add_collision_pair('ghost:slime', None, ghost)

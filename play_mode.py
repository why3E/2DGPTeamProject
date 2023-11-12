from pico2d import *

import game_world
import item_mode
import title_mode
from background import Background
from main_character import Main_Character
from atk import Sword
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
        else:
            main_character.handle_event(event)



def init():
    global background
    global main_character
    global start_time

    start_time = get_time()+1
    main_character = Main_Character()
    game_world.add_object(main_character, 1)

    background = Background(main_character)
    game_world.add_object(background, 0)

    main_character.Sword_s()
    main_character.Magic_s()

def update():
    global start_time
    game_world.update()

    current_time = get_time()
    if int((current_time - start_time) / 2) > 0:
        start_time = current_time

        ghost = Ghost(main_character)
        game_world.add_object(ghost, 1)

        slime = Slime(main_character)
        game_world.add_object(slime, 1)

        skeleton = Skeleton(main_character)
        game_world.add_object(skeleton, 1)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass

def pause():
    pass

def resume():
    pass
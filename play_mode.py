from pico2d import *

import game_world
import item_mode
import title_mode
from background import Background
from boy import Boy
import game_framework

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
            boy.handle_event(event)


def init():
    global background
    global team
    global boy

    boy = Boy()
    game_world.add_object(boy, 1)

    background = Background(boy)
    game_world.add_object(background, 0)

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass

def pause():
    boy.wait_time = 10000000000000000000000000000.0
    pass

def resume():
    boy.wait_time = get_time()
    pass
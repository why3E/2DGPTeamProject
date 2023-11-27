from pico2d import *

import game_world
import game_framework
import play_mode
from pannel import Pannel


# Game object class here
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            match event.key:
                case pico2d.SDLK_UP:
                    pannel.check-=1
                    pannel.check %=3
                case pico2d.SDLK_DOWN:
                    pannel.check+=1
                    pannel.check %=3
                case pico2d.SDLK_SPACE:
                    play_mode.main_character.level_up(pannel.item_random_choice[pannel.check])
                    game_framework.pop_mode()



def init():
    global pannel
    pannel = Pannel()
    game_world.add_object(pannel, 3)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.remove_object(pannel)
    pass


def pause():
    pass


def resume():
    pass


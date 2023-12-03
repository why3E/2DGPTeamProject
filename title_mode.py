from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, get_canvas_width, get_canvas_height
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import game_world
import play_mode


def init():
    global image,image2,image3,ch,cw
    image = load_image('source/title_image.png')
    image2 = load_image('source/start_UI.png')
    image3 = load_image('source/start_button.png')
    cw = get_canvas_width()
    ch = get_canvas_height()
    pass


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0,0,720,580,cw//2,ch//2,cw, ch)
    image2.clip_draw(0,0,116,33,cw//2,150,300,100)
    image3.clip_draw(0,0,122,29,cw//2,170,100,40)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(play_mode)

def pause():
    pass

def resume():
    pass
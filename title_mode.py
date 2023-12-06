from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time, get_canvas_width, get_canvas_height, \
    load_music, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
import game_world
import play_mode
import server


def init():
    global image,image2,image3,ch,cw,bgm,image4,image5
    global font, font2
    image = load_image('source/title_image.png')
    image2 = load_image('source/start_UI.png')
    image3 = load_image('source/start_button.png')

    image4 = load_image('source/hero_a.png')
    image5 = load_image('source/hero_b.png')
    cw = get_canvas_width()
    ch = get_canvas_height()

    bgm = load_music('source/start_bgm.mp3')
    bgm.set_volume(48)
    bgm.repeat_play()

    font = load_font('source/ENCR10B.TTF', 96)
    font2 = load_font('source/ENCR10B.TTF', 32)
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
    image4.draw(100,100,400,400)
    image5.draw(cw-200,200,200,200)
    font.draw(150, 450, f'Only Alive', (255, 255, 255))
    font2.draw(325, 50, f'start is space', (255, 255, 255))
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            bgm.stop()
            game_framework.change_mode(play_mode)

def pause():
    pass

def resume():
    pass
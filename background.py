from pico2d import load_image, get_canvas_width, get_canvas_height, clamp, load_music

import play_mode
import server


class Background:
    def __init__(self):
        self.image = load_image('bg_world_background.png')

        self.image2 = load_image('bg_world_up.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        self.bgm = load_music('source/battle_bgm.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def draw(self):
        self.image.clip_draw_to_origin(self.q3l, self.q3b, self.q3w, self.q3h, 0, 0)  # quadrant 3
        self.image.clip_draw_to_origin(self.q2l, self.q2b, self.q2w, self.q2h, 0, self.q3h)  # quadrant 2
        self.image.clip_draw_to_origin(self.q4l, self.q4b, self.q4w, self.q4h, self.q3w, 0)  # quadrant 4
        self.image.clip_draw_to_origin(self.q1l, self.q1b, self.q1w, self.q1h, self.q3w, self.q3h)  # quadrant 1
        self.image2.draw(self.cw // 2, self.ch - 100, self.cw, 200)

    def update(self):
        self.window_left = int(server.main_character.x) - self.cw // 2
        self.window_bottom = int(server.main_character.y) - self.ch // 2

        # quadrant 3
        self.q3l = (int(server.main_character.x) - self.cw // 2) % self.w
        self.q3b = (int(server.main_character.y) - self.ch // 2) % self.h
        self.q3w = clamp(0, self.w - self.q3l, self.w)
        self.q3h = clamp(0, self.h - self.q3b, self.h)

        # quadrant 2
        self.q2l = self.q3l
        self.q2b = 0
        self.q2w = self.q3w
        self.q2h = self.ch - self.q3h

        # quadrand 4
        self.q4l = 0
        self.q4b = self.q3b
        self.q4w = self.cw - self.q3w
        self.q4h = self.q3h

        # quadrand 1
        self.q1l = 0
        self.q1b = 0
        self.q1w = self.q4w
        self.q1h = self.q2h


class Background_sub:
    def __init__(self):
        self.image2 = load_image('bg_world_up.png')
        self.image3 = load_image('bg_world_down.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

    def draw(self):
        self.image2.draw(self.cw // 2, self.ch - 100, self.cw, 200)
        self.image3.draw(self.cw // 2, 100, self.cw, 200)

    def update(self): pass

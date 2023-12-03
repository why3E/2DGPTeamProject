from pico2d import load_image, get_canvas_width, get_canvas_height, clamp


class Background:
    def __init__(self,boy):
        self.image = load_image('bg_world_background.png')
        self.boy = boy
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom,
                                       self.cw, self.ch,
                                       0, 0)
    #무한맵 계획안 1.3x3 네모들로 편집 칸별로 300 잡고 boy.x값을 수정하지않고 self.x-boy.x%300 이런식으로 계속 가능하지 않을까?
    def update(self):
        self.window_left = clamp(0, int(self.boy.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(self.boy.y) - self.ch // 2, self.h - self.ch - 1)
        pass
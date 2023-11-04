from pico2d import load_image


class Background:
    def __init__(self,boy):
        self.image = load_image('bg_world_background.png')
        self.boy = boy

    def draw(self):
        self.image.draw(600 - self.boy.x, 600 - self.boy.y)


    def update(self):

        pass
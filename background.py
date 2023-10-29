from pico2d import load_image


class Grass:
    def __init__(self,boy):
        self.image = load_image('bg_world_background.png')
        self.boy = boy

    def draw(self):
        self.image.draw(400 - self.boy.x, 300 - self.boy.y)


    def update(self):

        pass
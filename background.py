from pico2d import load_image


class Background:
    def __init__(self,boy):
        self.image = load_image('bg_world_background.png')
        self.boy = boy
        self.x = self.boy.x
        self.y = self.boy.y

    def draw(self):
        self.x = self.x - self.boy.x
        self.y = self.y - self.boy.y

        self.image.draw(400 ,400,1200,1800)
#무한맵 계획안 1.3x3 네모들로 편집 칸별로 300 잡고 boy.x값을 수정하지않고 self.x-boy.x%300 이런식으로 계속 가능하지 않을까?
    def update(self):
        pass
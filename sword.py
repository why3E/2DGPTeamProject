from pico2d import *

import boy
import game_world

class Sword:
    image = None
    def __init__(self,boy):
        self.boy = boy
        self.level = 1
        if Sword.image == None:
            Sword.image = load_image('source/sword_01.png')
        self.x, self.y, self.velocity = boy.x, boy.y, boy.face_dir*20

    def draw(self):
        if (self.boy.face_dir == 1):
            self.image.draw(self.x+self.velocity, self.y-10)
        elif (self.boy.face_dir == -1):
            self.image.clip_composite_draw(0, 0, 32, 32, 0, 'h', self.x+self.velocity, self.y-10, 32, 32)
    def update(self):
        self.x, self.y, self.velocity = self.boy.x, self.boy.y, self.boy.face_dir * 20
        if(self.level == 2):
            Sword.image = load_image('source/sword_02.png')
        elif(self.level == 3):
            Sword.image = load_image('source/sword_03.png')
        elif (self.level == 4):
            Sword.image = load_image('source/sword_04.png')
        elif (self.level == 5):
            Sword.image = load_image('source/sword_05.png')
        pass

class BigBall:
    image = None

    def __init__(self, x = 400, y = 300, velocity = 1):
        if BigBall.image == None:
            BigBall.image = load_image('ball41x41.png')
        self.x, self.y, self.velocity = x, y, velocity

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += self.velocity

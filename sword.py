from pico2d import *

import boy
import game_framework
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


# zombie Action Speed
TIME_PER_ACTION = 0.9
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0


animation_names = ['sword']

class Swordline:
    images = None
    def __init__(self, boy):
        self.boy = boy
        self.x, self.y, self.velocity = boy.x, boy.y, boy.face_dir*20
        self.frame =0
        self.size = 80
        self.pos = 15
        self.count = 0
        self.wait_time = get_time()
        if Swordline.images == None:
            Swordline.images = {}
            for name in animation_names:
                Swordline.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 4)]

    def draw(self):
        if int(self.frame) < 3 and self.count == 0:
            if (self.boy.face_dir == 1):
                Swordline.images['sword'][int(self.frame)].draw(self.x+self.velocity+self.pos, self.y-self.pos, self.size, self.size)
            elif(self.boy.face_dir == -1):
                Swordline.images['sword'][int(self.frame)].composite_draw(0, 'h', self.x-self.pos, self.y-self.pos, self.size, self.size)
        print(int(self.frame))

    def update(self):
        self.x, self.y, self.velocity = self.boy.x, self.boy.y, self.boy.face_dir * 20
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

        if int(self.frame) == 3 and self.count == 3:
            self.count = 0
            self.frame = 0

        if int(self.frame) == 3:
            self.count += 1
            self.frame = 0

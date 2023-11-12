from pico2d import *

import game_framework


class Sword:
    image = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.level = 1
        if self.image == None:
            self.image1 = load_image('source/sword_01.png')
            self.image2 = load_image('source/sword_02.png')
            self.image3 = load_image('source/sword_03.png')
            self.image4 = load_image('source/sword_04.png')
            self.image5 = load_image('source/sword_05.png')
            self.image = self.image1
        self.x, self.y, self.velocity = main_character.x, main_character.y, main_character.face_dir * 20

        self.image_dict = {
            2: self.image2,
            3: self.image3,
            4: self.image4,
            5: self.image5
        }

    def draw(self):
        if (self.main_character.face_dir == 1):
            self.image.draw(self.x + self.velocity, self.y - 10)
        else:
            self.image.clip_composite_draw(0, 0, 32, 32, 0, 'h', self.x + self.velocity, self.y - 10, 32, 32)

    def update(self):
        self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
        if self.level in self.image_dict:
            Sword.image = self.image_dict[self.level]


# zombie Action Speed


animation_names = ['sword']
class Swordline:
    images = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.x, self.y, self.velocity = main_character.x, main_character.y, main_character.face_dir * 20
        self.frame = 0
        self.size = 80
        self.pos = 15
        self.count = 0
        self.wait_time = get_time()

        self.TIME_PER_ACTION = 0.5/self.main_character.atk_speed
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 4.0

        if Swordline.images == None:
            Swordline.images = {}
            for name in animation_names:
                Swordline.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 4)]

    def draw(self):
        if int(self.frame) < 3 and self.count == 0:
            if (self.main_character.face_dir == 1):
                Swordline.images['sword'][int(self.frame)].draw(self.x + self.velocity + self.pos, self.y - self.pos,
                                                                self.size, self.size)
            elif (self.main_character.face_dir == -1):
                Swordline.images['sword'][int(self.frame)].composite_draw(0, 'h', self.x - self.pos, self.y - self.pos,
                                                                          self.size, self.size)
        print(int(self.frame))

    def update(self):
        self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
        self.frame = (self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        if int(self.frame) == 3 and self.count == 3:
            self.count = 0
            self.frame = 0

        if int(self.frame) == 3:
            self.count += 1
            self.frame = 0

from pico2d import *

import game_framework


class Sword:
    image1 = None
    image2 = None
    image3 = None
    image4 = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.level = 1
        self.load_images()
        self.x, self.y, self.velocity = main_character.x, main_character.y, main_character.face_dir * 20
        self.image_dict = {
            1: Sword.image1,
            2: Sword.image2,
            3: Sword.image3,
            4: Sword.image4
        }

    def load_images(self):
        global image1, image2, image3, image4, image5
        if Sword.image1 is None:
            Sword.image1 = load_image('source/sword_01.png')
            Sword.image2 = load_image('source/sword_02.png')
            Sword.image3 = load_image('source/sword_03.png')
            Sword.image4 = load_image('source/sword_04.png')

    def draw(self):
        if self.main_character.face_dir == 1:
            Sword.image1.draw(self.x + self.velocity, self.y - 10)
        else:
            Sword.image1.clip_composite_draw(0, 0, 32, 32, 0, 'h', self.x + self.velocity, self.y - 10, 32, 32)

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

        self.TIME_PER_ACTION = 0.5 / self.main_character.atk_speed
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

    def update(self):
        self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
        self.frame = (
                             self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        if int(self.frame) == 3 and self.count == 3:
            self.count = 0
            self.frame = 0

        if int(self.frame) == 3:
            self.count += 1
            self.frame = 0



class Magic:
    image1 = None
    image2 = None
    image3 = None
    image4 = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.level = 1
        self.load_images()
        self.x, self.y, self.velocity = main_character.x, main_character.y, main_character.face_dir * 20
        self.image_dict = {
            1: Magic.image1,
            2: Magic.image2,
            3: Magic.image3,
            4: Magic.image4
        }

    def load_images(self):
        global image1, image2, image3, image4, image5
        if Magic.image1 is None:
            Magic.image1 = load_image('source/saintring_00.png')
            Magic.image2 = load_image('source/saintring_01.png')
            Magic.image3 = load_image('source/saintring_02.png')
            Magic.image4 = load_image('source/saintring_03.png')

    def draw(self):
        if self.main_character.face_dir == 1:
            Magic.image1.draw(self.x + self.velocity, self.y - 10)
        else:
            Magic.image1.clip_composite_draw(0, 0, 32, 32, 0, 'h', self.x + self.velocity, self.y - 10, 32, 32)

    def update(self):
        self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
        if self.level in self.image_dict:
            Magic.image = self.image_dict[self.level]



animation_names_two = ['cir']


class Magicline:
    images = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.x, self.y, self.velocity = main_character.x, main_character.y, 40
        self.frame = 0
        self.size = 80
        self.pos = 15
        self.count = 0
        
        self.wait_time = get_time()

        self.TIME_PER_ACTION = 0.5 / self.main_character.atk_speed
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 4.0

        if Magicline.images == None:
            Magicline.images = {}
            for name in animation_names_two:
                Magicline.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 5)]

    def draw(self):
        if int(self.frame) < 3 and self.count == 0:
            if (self.main_character.face_dir == 1):
                Magicline.images['cir'][int(self.frame)].draw(self.x + self.velocity + self.pos, self.y - self.pos,
                                                              self.size, self.size)
            elif (self.main_character.face_dir == -1):
                Magicline.images['cir'][int(self.frame)].composite_draw(0, 'h', self.x - self.pos, self.y - self.pos,
                                                                        self.size, self.size)
        print(int(self.frame))

    def update(self):
        self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
        self.frame = (self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        if int(self.frame) == 3 and self.count == 5:
            self.count = 0
            self.frame = 0

        if int(self.frame) == 3:
            self.count += 1
            self.frame = 0

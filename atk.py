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

import math

class Magicline:
    images = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.magic_circles = []  # 원에 대한 정보를 저장할 리스트
        self.radius = 60
        self.angular_velocity = 180  # 180도/초로 설정
        self.count = 0

        self.TIME_PER_ACTION = 0.5 / self.main_character.atk_speed
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 4.0

        if Magicline.images is None:
            Magicline.images = {}
            for name in animation_names_two:
                Magicline.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 5)]

        self.initialize_circles()

    def initialize_circles(self):
        self.add_circles(2)

    def add_circles(self, num_circles):
        # 주어진 개수만큼 원을 추가하고 각도를 설정
        angle_interval = 360 / num_circles
        for i in range(num_circles):
            self.add_circle(angle=i * angle_interval)

    def add_circle(self, angle=0):
        self.magic_circles.append({'angle': angle})

    def draw(self):
        for circle in self.magic_circles:
            draw_x = self.main_character.x + self.radius * math.cos(math.radians(circle['angle']))
            draw_y = self.main_character.y + self.radius * math.sin(math.radians(circle['angle']))

            if self.main_character.face_dir == 1:
                Magicline.images['cir'][int(self.count)].draw(draw_x, draw_y-10, self.radius , self.radius )
            else:
                Magicline.images['cir'][int(self.count)].composite_draw(0, 'h', draw_x, draw_y-10, self.radius , self.radius )

    def update(self):
        for circle in self.magic_circles:
            circle['angle'] = (circle['angle'] + self.angular_velocity * game_framework.frame_time) % 360

        self.count = (self.count + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 4

        if int(self.count) == 3:
            self.count = 0

    def increase_level(self):
        # 레벨이 오를 때마다 원의 개수를 늘리고 초기화
        num_circles = len(self.magic_circles) + 1
        self.magic_circles = []  # 기존 원 초기화
        self.add_circles(num_circles)

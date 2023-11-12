from pico2d import *

import game_framework
import game_world


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
                Swordline.images['sword'][int(self.frame)].draw(self.x + self.size/2, self.y - self.pos,
                                                                self.size, self.size)
            elif (self.main_character.face_dir == -1):
                Swordline.images['sword'][int(self.frame)].composite_draw(0, 'h', self.x - self.size/2, self.y - self.pos,
                                                                          self.size, self.size)
            draw_rectangle(*self.get_bb())

    def update(self):
        self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
        self.frame = (
                             self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

        if int(self.frame) == 3 and self.count == 3:
            self.count = 0
            self.frame = 0
            self.size = 80
        if int(self.frame) == 3:
            self.count += 1
            self.frame = 0
            self.size = 0

    def get_bb(self):
        if self.main_character.face_dir == 1:
            return self.x, self.y - self.size, self.x + self.size, self.y + self.size / 2
        else:
            return self.x - self.size, self.y - self.size, self.x, self.y + self.size / 2

    def handle_collision(self, group, other):
        pass


class Magic:
    def __init__(self, main_character):
        self.main_character = main_character
        self.level = 1
        magic_line = Magicline(main_character,self.level+1)
        game_world.add_object(magic_line)

animation_names_two = ['cir']

class Magicline:
    images = None

    def __init__(self, main_character, num_circles):
        self.main_character = main_character
        self.radius = 60
        self.angular_velocity = 180  # 180도/초로 설정
        self.magic_circles = []  # 원에 대한 정보를 저장할 리스트
        self.count = 2
        self.TIME_PER_ACTION = 0.5 / self.main_character.atk_speed
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 4.0

        if Magicline.images is None:
            Magicline.images = {}
            for name in animation_names_two:
                Magicline.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 5)]

        self.initialize_circles(num_circles)

    def initialize_circles(self, num_circles):
        angle_interval = 360 / num_circles
        for i in range(num_circles):
            self.add_circle(angle=i * angle_interval)

    def add_circle(self, angle=0):
        new_circle = {'angle': angle, 'radius': self.radius}
        self.magic_circles.append(new_circle)

    def draw(self):
        for circle in self.magic_circles:
            draw_x = self.main_character.x + circle['radius'] * math.cos(math.radians(circle['angle']))
            draw_y = self.main_character.y + circle['radius'] * math.sin(math.radians(circle['angle']))

            if self.main_character.face_dir == 1:
                Magicline.images['cir'][int(self.count)].draw(draw_x, draw_y - 10, circle['radius'], circle['radius'])
            else:
                Magicline.images['cir'][int(self.count)].composite_draw(0, 'h', draw_x, draw_y - 10, circle['radius'], circle['radius'])

    def update(self):
        self.count = (self.count + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 4

        for circle in self.magic_circles:
            circle['angle'] = (circle['angle'] + self.angular_velocity * game_framework.frame_time) % 360

        if int(self.count) == 3:
            self.count = 0

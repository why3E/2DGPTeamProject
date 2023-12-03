import random
import time

from pico2d import *

import game_framework
import game_world
import play_mode


class Sword:
    image = None
    image1 = None
    image2 = None
    image3 = None
    image4 = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.level = 1
        self.x, self.y, self.velocity = main_character.x, main_character.y, main_character.face_dir * 20
        self.load_images()
        self.invulnerable_time = 2.0 / self.level
        self.last_collision_time = time.time()
        self.image_dict = {
            1: Sword.image1,
            2: Sword.image2,
            3: Sword.image3,
            4: Sword.image4
        }

    def load_images(self):
        if Sword.image is None:
            Sword.image1 = load_image('source/sword_01.png')
            Sword.image2 = load_image('source/sword_02.png')
            Sword.image3 = load_image('source/sword_03.png')
            Sword.image4 = load_image('source/sword_04.png')
            Sword.image = Sword.image1

    def draw(self):
        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        if self.main_character.face_dir == 1:
            Sword.image.draw(sx + self.velocity, sy - 10)
        else:
            Sword.image.clip_composite_draw(0, 0, 32, 32, 0, 'h', sx + self.velocity, sy - 10, 32, 32)

    def update(self):
        if play_mode.play_check ==True:
            self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
            if self.level in self.image_dict:
                Sword.image = self.image_dict[self.level]

            self.invulnerable_time = 2.0 / self.level
            current_time = time.time()
            if self.level in self.image_dict:
                Magic.image = self.image_dict[self.level]
            if current_time - self.last_collision_time > self.invulnerable_time:
                self.last_collision_time = current_time
                sword_line = Swordline(self.main_character)
                game_world.add_object(sword_line, 1)
                game_world.add_collision_pair('atk:monster', None, sword_line)

# zombie Action Speed
animation_names = ['sword']


class Swordline:
    images = None
    def __init__(self, main_character):
        self.main_character = main_character
        self.x, self.y, self.velocity = main_character.x, main_character.y, main_character.face_dir * 20
        self.frame = 0
        self.size = 80+self.main_character.sword.level*10
        self.pos = 15
        self.count = 0
        self.wait_time = get_time()

        self.TIME_PER_ACTION = 0.5 / self.main_character.sword.level
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 4.0

        if Swordline.images == None:
            Swordline.images = {}
            for name in animation_names:
                Swordline.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 4)]

    def draw(self):
        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        if int(self.frame) < 3 and self.count == 0:
            if (self.main_character.face_dir == 1):
                Swordline.images['sword'][int(self.frame)].draw(sx + self.size / 2, sy - self.pos,
                                                                self.size, self.size)
            elif (self.main_character.face_dir == -1):
                Swordline.images['sword'][int(self.frame)].composite_draw(0, 'h', sx - self.size / 2,
                                                                          sy - self.pos,
                                                                          self.size, self.size)
            draw_rectangle(*self.get_bb())

    def update(self):
        if play_mode.play_check == True:
            self.TIME_PER_ACTION = 0.5 / self.main_character.sword.level
            self.x, self.y, self.velocity = self.main_character.x, self.main_character.y, self.main_character.face_dir * 20
            self.frame = (
                                 self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % self.FRAMES_PER_ACTION

            if int(self.frame) == 3 and self.count == 3:
                game_world.remove_object(self)
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
    Magic_image = None
    image1 = None
    image2 = None
    image3 = None
    image4 = None

    def __init__(self, main_character):
        self.main_character = main_character
        self.last_collision_time = time.time()
        self.level = 0
        self.invulnerable_time = 2.0  # 예시로 2초로 설정
        self.load_images()
        self.image_dict = {
            0: Magic.image1,
            1: Magic.image1,
            2: Magic.image2,
            3: Magic.image3,
            4: Magic.image4
        }

    def load_images(self):
        if Magic.Magic_image is None:
            Magic.image1 = load_image('source/saintring_00.png')
            Magic.image2 = load_image('source/saintring_01.png')
            Magic.image3 = load_image('source/saintring_02.png')
            Magic.image4 = load_image('source/saintring_03.png')
            Magic.Magic_image = Magic.image1

    def update(self):
        if self.level != 0:
            self.invulnerable_time = 2.0 / self.level
            if play_mode.play_check == True:
                current_time = time.time()
                if self.level in self.image_dict:
                    Magic.image = self.image_dict[self.level]
                if current_time - self.last_collision_time > self.invulnerable_time:
                    self.last_collision_time = current_time
                    magic_circle = Magiccircle()
                    game_world.add_object(magic_circle)
                    game_world.add_collision_pair('atk:monster', None, magic_circle)
    def draw(self):
        pass

animation_names_two = ['cir']

class Magiccircle:
    images = None
    def __init__(self):
        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 4.0
        self.size = 50
        self.frame = 0
        self.x,self.y = play_mode.main_character.x +random.randint(-400, 400),play_mode.main_character.y +random.randint(-400, 400)
        if Magiccircle.images is None:
            Magiccircle.images = {}
            for name in animation_names_two:
                Magiccircle.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 5)]


    def draw(self):

        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        self.images['cir'][int(self.frame)].clip_composite_draw(0, 0, 220, 220, 0, '', sx, sy, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        if play_mode.play_check == True:
            self.frame = (self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 4

    def get_bb(self):
        return self.x - self.size/2, self.y - self.size/2, self.x + self.size/2, self.y + self.size/2

    def handle_collision(self, group, other):
        if group == 'atk:monster':
            game_world.remove_object(self)
        pass


class Bow:
    Bow_image = None
    image1 = None
    image2 = None
    image3 = None
    image4 = None
    def __init__(self, main_character):
        self.main_character = main_character
        self.last_collision_time = time.time()
        self.level = 0
        self.invulnerable_time = 1.0   # 예시로 2초로 설정
        self.load_images()
        self.image_dict = {
            0: Bow.image1,
            1: Bow.image1,
            2: Bow.image2,
            3: Bow.image3,
            4: Bow.image4
        }

    def load_images(self):
        if Bow.Bow_image is None:
            Bow.image1 = load_image('source/bow_00.png')
            Bow.image2 = load_image('source/bow_01.png')
            Bow.image3 = load_image('source/bow_02.png')
            Bow.image4 = load_image('source/bow_03.png')
            Bow.Bow_image = Bow.image1

    def update(self):
        if self.level != 0:
            self.invulnerable_time = 1.0 / self.level
            if play_mode.play_check == True:
                current_time = time.time()
                if self.level in self.image_dict:
                    Bow.image = self.image_dict[self.level]
                if current_time - self.last_collision_time > self.invulnerable_time:
                    self.last_collision_time = current_time
                    arrow = Arrow(self.main_character)
                    game_world.add_object(arrow)
                    game_world.add_collision_pair('atk:monster', None, arrow)

    def draw(self):
        pass


animation_names_three = ['arrow']


class Arrow:
    images = None

    def __init__(self, main_character):
        self.x, self.y = main_character.x, main_character.y
        self.main_character = main_character
        self.angle = math.radians(random.randint(0, 360))  # 현재 캐릭터의 각도를 화살의 시작 각도로 설정
        self.size = 10

        self.TIME_PER_ACTION = 0.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 3.0

        self.PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
        self.RUN_SPEED_KMPH = 0.3  # Km / Hour
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        if Arrow.images is None:
            Arrow.images = {}
            for name in animation_names_three:
                Arrow.images[name] = [load_image("source/" + name + " (%d)" % i + ".png") for i in range(1, 4)]
        self.frame = random.randint(0, 2)

    def draw(self):
        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        self.images['arrow'][int(self.frame)].clip_composite_draw(0, 0, 96, 41, self.angle, '', sx, sy, 48, 20)
        draw_rectangle(*self.get_bb())

    def update(self):
        if play_mode.play_check == True:
            self.x += self.RUN_SPEED_PPS * math.cos(self.angle)
            self.y += self.RUN_SPEED_PPS * math.sin(self.angle)

            self.frame = (self.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 3

            # 화살이 일정 거리 이상 날아가면 제거

            sx = self.x - play_mode.background.window_left
            sy = self.y - play_mode.background.window_bottom

            if sx > 900 or sx < 0 or sy < 0 or sy > 900:
                game_world.remove_object(self)

    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        if group == 'atk:monster':
            game_world.remove_object(self)
        pass

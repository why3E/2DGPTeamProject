import random
import math
import game_framework

from pico2d import *

import game_world
import main_character

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
GHOST_FRAMES_PER_ACTION = 4.0
SLIME_FRAMES_PER_ACTION = 7.0
SKELETON_FRAMES_PER_ACTION = 4.0

class Ghost:
    image = None

    def load_images(self):
        if Ghost.image == None:
            Ghost.image =load_image('source/ghost_AT.png')

    def __init__(self, main_character):
        self.main_character = main_character
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.x = self.main_character.x + self.radius * math.cos(math.radians(self.radians))
        self.y = self.main_character.y + self.radius * math.sin(math.radians(self.radians))
        self.load_images()
        self.frame = random.randint(0, 4)
        self.dir = random.choice([-1,1])
        self.dir2 = random.choice([-1,1])
        self.size = 16
        self.hp = 10
        self.invulnerable_time = 1.0  # 무적 상태 지속 시간
        self.last_collision_time = 0.0


    def update(self):
        if self.main_character.wait_time_play == 0:

            if self.hp <= 0:
                game_world.remove_object(self)
                self.main_character.Exp += 10
            self.frame = (self.frame + GHOST_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % GHOST_FRAMES_PER_ACTION

            self.dir = self.main_character.x - self.x
            self.dir2 = self.main_character.y - self.y

            distance = (self.dir ** 2 + self.dir2 ** 2) ** 0.5

            if distance != 0:
                self.dir /= distance
                self.dir2 /= distance

            if self.dir != 0 and self.dir2 != 0:
                self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time*0.5
                self.y += RUN_SPEED_PPS * self.dir2 * game_framework.frame_time*0.5
            else:
                self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
                self.y += RUN_SPEED_PPS * self.dir2 * game_framework.frame_time

            pass


    def draw(self):
        if self.dir >= 0:
            self.image.clip_composite_draw(int(self.frame) * 32, 0, 32, 32, 0, 'h', self.x, self.y, 32, 32)
        else:
            self.image.clip_draw(int(self.frame) * 32, 0, 32, 32, self.x, self.y,32,32)
        draw_rectangle(*self.get_bb())

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        current_time = get_time()
        if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
            self.last_collision_time = current_time
            self.hp -= 5



class Slime:
    image = None

    def load_images(self):
        if Slime.image == None:
            Slime.image =load_image('source/slime_2.png')

    def __init__(self, main_character):
        self.main_character = main_character
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.x = self.main_character.x + self.radius * math.cos(math.radians(self.radians))
        self.y = self.main_character.y + self.radius * math.sin(math.radians(self.radians))
        self.load_images()
        self.frame = random.randint(0, 7)
        self.dir = random.choice([-1,1])
        self.dir2 = random.choice([-1,1])
        self.size = 16
        self.hp = 10
        self.invulnerable_time = 1.0  # 무적 상태 지속 시간
        self.last_collision_time = 0.0


    def update(self):
        if self.main_character.wait_time_play == 0:
            if self.hp <= 0:
                game_world.remove_object(self)
                self.main_character.Exp += 10

            self.frame = (self.frame + SLIME_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SLIME_FRAMES_PER_ACTION

            self.dir = self.main_character.x - self.x
            self.dir2 = self.main_character.y - self.y

            distance = (self.dir ** 2 + self.dir2 ** 2) ** 0.5

            if distance != 0:
                self.dir /= distance
                self.dir2 /= distance

            if self.dir != 0 and self.dir2 != 0:
                self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time*0.5
                self.y += RUN_SPEED_PPS * self.dir2 * game_framework.frame_time*0.5
            else:
                self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
                self.y += RUN_SPEED_PPS * self.dir2 * game_framework.frame_time

            pass


    def draw(self):
        if self.dir >= 0:
            self.image.clip_composite_draw(int(self.frame) * 28, 0, 28, 25, 0, 'h', self.x, self.y, 32, 32)
        else:
            self.image.clip_draw(int(self.frame) * 28, 0, 28, 25, self.x, self.y,32,32)
        draw_rectangle(*self.get_bb())

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size


    def handle_collision(self, group, other):
        current_time = get_time()
        if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
            self.last_collision_time = current_time
            self.hp -= 5


class Skeleton:
    image = None

    def load_images(self):
        if Skeleton.image == None:
            Skeleton.image =load_image('source/skeleton.png')

    def __init__(self, main_character):
        self.hp = 10
        self.main_character = main_character
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.x = self.main_character.x + self.radius * math.cos(math.radians(self.radians))
        self.y = self.main_character.y + self.radius * math.sin(math.radians(self.radians))
        self.load_images()
        self.frame = random.randint(0, 4)
        self.dir = random.choice([-1,1])
        self.dir2 = random.choice([-1,1])
        self.size = 16
        self.invulnerable_time = 1.0  # 무적 상태 지속 시간
        self.last_collision_time = 0.0


    def update(self):
        if self.main_character.wait_time_play == 0:
            if self.hp <= 0:
                game_world.remove_object(self)
                self.main_character.Exp += 10

            self.frame = (self.frame + SKELETON_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SKELETON_FRAMES_PER_ACTION

            self.dir = self.main_character.x - self.x
            self.dir2 = self.main_character.y - self.y

            distance = (self.dir ** 2 + self.dir2 ** 2) ** 0.5

            if distance != 0:
                self.dir /= distance
                self.dir2 /= distance

            if self.dir != 0 and self.dir2 != 0:
                self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time*0.5
                self.y += RUN_SPEED_PPS * self.dir2 * game_framework.frame_time*0.5
            else:
                self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
                self.y += RUN_SPEED_PPS * self.dir2 * game_framework.frame_time

            pass


    def draw(self):
        if self.dir >= 0:
            self.image.clip_composite_draw(int(self.frame) * 35, 0, 35, 36, 0, 'h', self.x, self.y, 32, 32)
        else:
            self.image.clip_draw(int(self.frame) * 35, 0, 35, 36, self.x, self.y, 32,32)
        draw_rectangle(*self.get_bb())

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size


    def handle_collision(self, group, other):
        current_time = get_time()
        if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
            self.last_collision_time = current_time
            self.hp -= 5

# 피격판정을 받았을떄 풍선을 만든다(스킬 3개니까 각기 다른 풍선 3개) 하고 만약 해당하는 피격 종류를 받으면 풍선을 터트리고
# 시간을 잰 다음 다시 부풀어 오르게 하자)
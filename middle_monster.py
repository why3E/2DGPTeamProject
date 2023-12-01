import random
import game_framework
from pico2d import *
import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from pasive_item import Coin

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 7.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
SKELETON_GHOST_FRAMES_PER_ACTION = 4.0
SLIME_SLIME_FRAMES_PER_ACTION = 6.0
SKELETON_FRAMES_PER_ACTION = 4.0


class Skeleton_ghost:
    image = None

    def load_images(self):
        if Skeleton_ghost.image is None:
            Skeleton_ghost.image = load_image('source/skeleton_ghost.png')

    def __init__(self, other):
        self.other = other
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.x = self.other.x
        self.y = self.other.y
        self.load_images()
        self.frame = random.randint(0, 4)
        self.dir = random.choice([-1, 1])
        self.dir2 = random.choice([-1, 1])
        self.size = 25
        self.hp = 20
        self.invulnerable_time = play_mode.main_character.atk_speed  # 무적 상태 지속 시간 - 캐릭터 공격속도로 지정하면 될듯?
        self.last_collision_time = 0.0
        self.tx, self.ty = 1000, 1000
        self.bt = None
        behavior_tree(self)

    def update(self):
        if play_mode.play_check is True:
            self.frame = (
                                 self.frame + SKELETON_GHOST_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SKELETON_GHOST_FRAMES_PER_ACTION
            self.bt.run()
            pass

    def draw(self):
        if math.cos(self.dir) >= 0:
            self.image.clip_composite_draw(int(self.frame) * 49, 0, 49, 48, 0, 'h', self.x, self.y, 50, 50)
        else:
            self.image.clip_draw(int(self.frame) * 49, 0, 49, 48, self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        current_time = get_time()
        if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
            self.last_collision_time = current_time
            self.hp -= play_mode.main_character.atk

            if self.hp <= 0:
                coin = Coin(self, 'middle_monster')
                game_world.add_object(coin, 1)
                game_world.add_collision_pair('Main:Coin', None, coin)
                game_world.remove_object(self)


class Slime_Slime:
    image = None

    def load_images(self):
        if Slime_Slime.image is None:
            Slime_Slime.image = load_image('source/slime_slime.png')

    def __init__(self, other):
        self.other = other
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.x = self.other.x
        self.y = self.other.y
        self.load_images()
        self.frame = random.randint(0, 6)
        self.dir = random.choice([-1, 1])
        self.dir2 = random.choice([-1, 1])
        self.size = 20
        self.hp = 25
        self.invulnerable_time = play_mode.main_character.atk_speed  # 무적 상태 지속 시간
        self.last_collision_time = 0.0
        self.tx, self.ty = 1000, 1000
        self.bt = None
        behavior_tree(self)

    def update(self):
        if play_mode.play_check is True:
            self.frame = (
                                 self.frame + SLIME_SLIME_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SLIME_SLIME_FRAMES_PER_ACTION
            self.bt.run()

    def draw(self):
        if math.cos(self.dir) >= 0:
            self.image.clip_composite_draw(int(self.frame) * 52, 0, 52, 55, 0, 'h', self.x, self.y, 40, 40)
        else:
            self.image.clip_draw(int(self.frame) * 52, 0, 52, 55, self.x, self.y, 40, 40)
        draw_rectangle(*self.get_bb())

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        current_time = get_time()
        if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
            self.last_collision_time = current_time
            self.hp -= play_mode.main_character.atk

            if self.hp <= 0:
                coin = Coin(self, 'middle_monster')
                game_world.add_object(coin, 1)
                game_world.add_collision_pair('Main:Coin', None, coin)
                game_world.remove_object(self)


class Sliem_Skeleton:
    image = None

    def __init__(self, other):
        self.hp = 25
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.x = other.x
        self.y = other.y
        self.load_images()
        self.frame = random.randint(0, 4)
        self.dir = random.choice([-1, 1])
        self.dir2 = random.choice([-1, 1])
        self.size = 25
        self.invulnerable_time = play_mode.main_character.atk_speed  # 무적 상태 지속 시간
        self.last_collision_time = 0.0
        self.tx, self.ty = 1000, 1000
        self.bt = None
        behavior_tree(self)

    def load_images(self):
        if Sliem_Skeleton.image is None:
            Sliem_Skeleton.image = load_image('source/slime_skeleton.png')

    def update(self):
        if play_mode.play_check is True:
            self.frame = (
                                 self.frame + SKELETON_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SKELETON_FRAMES_PER_ACTION
            # fill here
            self.bt.run()

    def draw(self):
        if math.cos(self.dir) >= 0:
            self.image.clip_composite_draw(int(self.frame) * 56, 0, 56, 46, 0, 'h', self.x, self.y, 50, 50)
        else:
            self.image.clip_draw(int(self.frame) * 56, 0, 56, 46, self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        current_time = get_time()
        if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
            self.last_collision_time = current_time
            self.hp -= play_mode.main_character.atk
            if self.hp <= 0:
                coin = Coin(self, 'middle_monster')
                game_world.add_object(coin, 1)
                game_world.add_collision_pair('Main:Coin', None, coin)

                game_world.remove_object(self)


def set_target_location(self, x=None, y=None):
    if not x or not y:
        raise ValueError("위치 지정을 해야합니다.")
    self.tx, self.ty = play_mode.main_character.x, play_mode.main_character.x
    return BehaviorTree.SUCCESS
    pass


def distance_less_than(x1, y1, x2, y2, r):
    distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
    return distance2 < (PIXEL_PER_METER * r) ** 2
    pass


def move_slightly_to(self, tx, ty):
    self.dir = math.atan2(ty - self.y, tx - self.x)
    self.speed = RUN_SPEED_PPS
    self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
    self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
    pass


def move_to_main_character(self, r=0.5):
    move_slightly_to(self, play_mode.main_character.x, play_mode.main_character.y)
    if distance_less_than(play_mode.main_character.x, play_mode.main_character.y, self.x, self.y, r):
        return BehaviorTree.SUCCESS
    else:
        return BehaviorTree.RUNNING
    pass


def behavior_tree(self):
    a1 = Action('Set target location', set_target_location, self, 500, 50)  # action node 생성
    a2 = Action('Move to', move_to_main_character, self)
    root = SEQ_move_to_target_location = Sequence('Move to target location', a1, a2)

    self.bt = BehaviorTree(root)
    pass

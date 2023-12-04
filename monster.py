import random
import game_framework
from pico2d import *
import game_world
import play_mode
from behavior_tree import BehaviorTree, Action, Sequence
from middle_monster import Slime_Slime, Sliem_Skeleton, Skeleton_ghost
from pasive_item import Coin

# Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 7.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
GHOST_FRAMES_PER_ACTION = 4.0
SLIME_FRAMES_PER_ACTION = 7.0
SKELETON_FRAMES_PER_ACTION = 4.0


def random_position(self):
    if self.position == 0:
        self.x = play_mode.main_character.x + random.randint(-450, 450)
        self.y = play_mode.main_character.y + random.choice([-450, 450])
    elif self.position == 1:
        self.x = play_mode.main_character.x + random.choice([-450, 450])
        self.y = play_mode.main_character.y + random.randint(-450, 450)


class Ghost:
    image = None
    death_sound = None

    def load_images(self):
        if Ghost.image is None:
            Ghost.image = load_image('source/ghost_AT.png')
        if Ghost.death_sound is None:
            Ghost.death_sound = load_wav('source/ghost.wav')
            Ghost.death_sound.set_volume(16)

    def __init__(self,hp):
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.position = random.choice([0, 1])
        self.x = 0
        self.y = 0
        random_position(self)
        self.load_images()
        self.frame = random.randint(0, 4)
        self.dir = random.choice([-1, 1])
        self.dir2 = random.choice([-1, 1])
        self.size = 16
        self.hp = hp
        self.invulnerable_time = play_mode.main_character.atk_speed  # 무적 상태 지속 시간 - 캐릭터 공격속도로 지정하면 될듯?
        self.last_collision_time = 0.0
        self.tx, self.ty = 1000, 1000
        self.bt = None

        behavior_tree(self)

    def update(self):

        if play_mode.play_check == True:
            self.frame = (
                                 self.frame + GHOST_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % GHOST_FRAMES_PER_ACTION
            self.bt.run()
            pass

    def draw(self):
        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        if math.cos(self.dir) >= 0:
            self.image.clip_composite_draw(int(self.frame) * 32, 0, 32, 32, 0, 'h', sx, sy, 32, 32)
        else:
            self.image.clip_draw(int(self.frame) * 32, 0, 32, 32, sx, sy, 32, 32)

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        current_time = get_time()

        if self in game_world.objects[1]:
            if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
                self.last_collision_time = current_time
                self.hp -= play_mode.main_character.atk

                if self.hp <= 0:
                    Ghost.death_sound.play()
                    coin = Coin(self, 'monster')
                    game_world.add_object(coin, 1)
                    game_world.add_collision_pair('Main:Coin', None, coin)

                    game_world.remove_object(self)
            elif group == 'ghost:slime':
                game_world.remove_object(self)
            elif group == 'ghost:skeleton':
                skeleton_ghost = Skeleton_ghost(self)
                game_world.add_object(skeleton_ghost, 1)
                game_world.add_collision_pair('main_character:monster', skeleton_ghost, None)
                game_world.add_collision_pair('atk:monster', skeleton_ghost, None)

                game_world.remove_object(self)


class Slime:
    image = None
    death_sound = None

    def load_images(self):
        if Slime.image == None:
            Slime.image = load_image('source/slime_2.png')
        if Slime.death_sound is None:
            Slime.death_sound = load_wav('source/slime.wav')
            Slime.death_sound.set_volume(20)

    def __init__(self,hp):
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.position = random.choice([0, 1])
        self.x = 0
        self.y = 0
        random_position(self)
        self.load_images()
        self.frame = random.randint(0, 7)
        self.dir = random.choice([-1, 1])
        self.dir2 = random.choice([-1, 1])
        self.size = 16
        self.hp = hp
        self.invulnerable_time = play_mode.main_character.atk_speed  # 무적 상태 지속 시간
        self.last_collision_time = 0.0
        self.tx, self.ty = 1000, 1000

        self.bt = None
        behavior_tree(self)

    def update(self):

        if play_mode.play_check == True:
            self.frame = (
                                 self.frame + SLIME_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SLIME_FRAMES_PER_ACTION
            self.bt.run()

    def draw(self):
        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        if math.cos(self.dir) >= 0:
            self.image.clip_composite_draw(int(self.frame) * 28, 0, 28, 25, 0, 'h', sx, sy, 32, 32)
        else:
            self.image.clip_draw(int(self.frame) * 28, 0, 28, 25, sx, sy, 32, 32)

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        current_time = get_time()
        if self in game_world.objects[1]:
            if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
                self.last_collision_time = current_time
                self.hp -= play_mode.main_character.atk

                if self.hp <= 0:
                    Slime.death_sound.play()
                    coin = Coin(self, 'monster')
                    game_world.add_object(coin, 1)
                    game_world.add_collision_pair('Main:Coin', None, coin)
                    game_world.remove_object(self)
            elif group == 'ghost:slime':
                slime_slime = Slime_Slime(self)
                game_world.add_object(slime_slime, 1)
                game_world.add_collision_pair('main_character:monster', slime_slime, None)
                game_world.add_collision_pair('atk:monster', slime_slime, None)

                game_world.remove_object(self)
            elif group == 'slime:skeleton':
                game_world.remove_object(self)


class Skeleton:
    image = None
    death_sound = None

    def load_images(self):
        if Skeleton.image == None:
            Skeleton.image = load_image('source/skeleton.png')
        if Skeleton.death_sound is None:
            Skeleton.death_sound = load_wav('source/skeleton.wav')
            Skeleton.death_sound.set_volume(16)

    def __init__(self,hp):
        self.hp = hp
        self.radius = 400
        self.radians = random.randint(0, 360)
        self.position = random.choice([0, 1])
        self.x = 0
        self.y = 0
        random_position(self)
        self.load_images()
        self.frame = random.randint(0, 4)
        self.dir = random.choice([-1, 1])
        self.dir2 = random.choice([-1, 1])
        self.size = 16
        self.invulnerable_time = play_mode.main_character.atk_speed  # 무적 상태 지속 시간
        self.last_collision_time = 0.0
        self.tx, self.ty = 1000, 1000
        self.bt = None
        behavior_tree(self)

    def update(self):
        if play_mode.play_check == True:
            self.frame = (
                                 self.frame + SKELETON_FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % SKELETON_FRAMES_PER_ACTION
            # fill here
            self.bt.run()

    def draw(self):
        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        if math.cos(self.dir) >= 0:
            self.image.clip_composite_draw(int(self.frame) * 35, 0, 35, 36, 0, 'h', sx, sy, 32, 32)
        else:
            self.image.clip_draw(int(self.frame) * 35, 0, 35, 36, sx, sy, 32, 32)

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        current_time = get_time()

        if self in game_world.objects[1]:
            if group == 'atk:monster' and current_time - self.last_collision_time > self.invulnerable_time:
                self.last_collision_time = current_time
                self.hp -= play_mode.main_character.atk
                if self.hp <= 0:
                    Skeleton.death_sound.play()
                    coin = Coin(self, 'monster')
                    game_world.add_object(coin, 1)
                    game_world.add_collision_pair('Main:Coin', None, coin)

                    game_world.remove_object(self)
            elif group == 'slime:skeleton':
                slime_skeleton = Sliem_Skeleton(self)
                game_world.add_object(slime_skeleton, 1)
                game_world.add_collision_pair('main_character:monster', slime_skeleton, None)
                game_world.add_collision_pair('atk:monster', slime_skeleton, None)
                game_world.remove_object(self)
            elif group == 'ghost:skeleton':
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

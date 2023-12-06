# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, \
    SDLK_DOWN, get_canvas_width, get_canvas_height, load_wav, draw_rectangle

import game_framework
import item_mode
import play_mode
import server
import title_mode
from atk_item import Sword, Swordline, Magic, Bow, Magic2
import game_world
from pasive_item import Ring, Amor, Glove, Meat

# 키 입력이 왔을때 각각 따로 키를 계산하지 않고 이미 한번 donw 눌림이 인식된 키는 up이 들어올떄까지 True로 인식시킨다.
# 상하, 좌우 나눌필요는 없고 Run에서 이동값을 계산할때만 따로 반영하면 됨

TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


def check_move_down(main_character, e):
    if (e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN):
        if (e[1].key == SDLK_RIGHT):
            main_character.right_move = 2
            if (main_character.left_move == 2):
                main_character.left_move = 1
        if (e[1].key == SDLK_LEFT):
            main_character.left_move = 2
            if (main_character.right_move == 2):
                main_character.right_move = 1
        if (e[1].key == SDLK_UP):
            main_character.up_move = 2
            if (main_character.down_move == 2):
                main_character.down_move = 1
        if (e[1].key == SDLK_DOWN):
            main_character.down_move = 2
            if (main_character.up_move == 2):
                main_character.up_move = 1
    elif (e[0] == 'INPUT' and e[1].type == SDL_KEYUP):
        if (e[1].key == SDLK_RIGHT and main_character.right_move != 0):
            main_character.right_move = 0
            if (main_character.left_move == 1):
                main_character.left_move = 2
        if (e[1].key == SDLK_LEFT and main_character.left_move != 0):
            main_character.left_move = 0
            if (main_character.right_move == 1):
                main_character.right_move = 2
        if (e[1].key == SDLK_UP and main_character.up_move != 0):
            main_character.up_move = 0
            if (main_character.down_move == 1):
                main_character.down_move = 2
        if (e[1].key == SDLK_DOWN and main_character.down_move != 0):
            main_character.down_move = 0
            if (main_character.up_move == 1):
                main_character.up_move = 2
    if (main_character.right_move or main_character.left_move or main_character.up_move or main_character.down_move):
        move_check = True
    else:
        move_check = False

    return e[0] == 'INPUT' and move_check


def check_move_up(main_character, e):
    if (main_character.move_check == False):
        return e[0] == 'INPUT' and True
    else:
        return e[0] == 'INPUT' and False


class Idle:
    @staticmethod
    def enter(main_character, e):
        main_character.frame = 0
        main_character.wait_time = get_time()  # pico2d import 필요
        main_character.dir = 0
        main_character.dir2 = 0
        pass

    @staticmethod
    def exit(main_character, e):
        pass

    @staticmethod
    def do(main_character):
        main_character.frame = (main_character.frame + 1) % 4

    @staticmethod
    def draw(main_character):
        sx, sy = get_canvas_width() // 2, get_canvas_height() // 2
        if main_character.face_dir == 1:
            main_character.image.clip_draw(0, 0, 32, 64, sx, sy, 32, 64)
        elif main_character.face_dir == -1:
            main_character.image.clip_composite_draw(0, 0, 32, 64, 0, 'h', sx, sy, 32, 64)
        main_character.hp_bar_image.clip_draw(0, 0, 46, 12, sx, sy - 50,
                                              main_character.hp_max + 6, 12)
        main_character.hp_image.clip_draw(0, 0, 30, 6,
                                          sx + (main_character.hp - main_character.hp_max) / 2,
                                          sy - 50, main_character.hp,
                                          6)


class Run:
    @staticmethod
    def enter(main_character, e):
        main_character.dir = 0
        main_character.dir2 = 0

        if check_move_down(main_character, e):
            if main_character.right_move == 2:
                main_character.dir, main_character.face_dir = 1, 1
            elif main_character.left_move == 2:
                main_character.dir, main_character.face_dir = -1, -1
            if main_character.up_move == 2:
                main_character.dir2 = 1
            elif main_character.down_move == 2:
                main_character.dir2 = -1

    @staticmethod
    def exit(main_character, e):
        pass

    @staticmethod
    def do(main_character):
        main_character.frame = (
                                       main_character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        main_character.x += main_character.dir * main_character.RUN_SPEED_PPS * game_framework.frame_time
        main_character.y += main_character.dir2 * main_character.RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(main_character):
        sx, sy = get_canvas_width() // 2, get_canvas_height() // 2
        if main_character.face_dir == 1:
            main_character.image.clip_draw(int(main_character.frame) * 32, 0, 32, 64, sx, sy, 32, 64)
        elif main_character.face_dir == -1:
            main_character.image.clip_composite_draw(int(main_character.frame) * 32, 0, 32, 64, 0, 'h',
                                                     sx, sy, 32, 64)
        main_character.hp_bar_image.clip_draw(0, 0, 46, 12, sx, sy - 50,
                                              main_character.hp_max + 6, 12)
        main_character.hp_image.clip_draw(0, 0, 30, 6,
                                          sx + (main_character.hp - main_character.hp_max) / 2,
                                          sy - 50, main_character.hp,
                                          6)


class StateMachine:
    def __init__(self, main_character):
        self.main_character = main_character
        self.cur_state = Idle
        self.transitions = {
            Idle: {check_move_down: Run, check_move_up: Idle},
            Run: {check_move_down: Run, check_move_up: Idle}
        }

    def start(self):
        self.cur_state.enter(self.main_character, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.main_character)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(self.main_character, e):
                self.cur_state.exit(self.main_character, e)
                self.cur_state = next_state
                self.cur_state.enter(self.main_character, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.main_character)


class Main_Character:
    def __init__(self):
        self.x = server.background.w // 2
        self.y = server.background.h // 2
        self.frame = 0
        self.size = 10
        # 캐릭터의 이동 방향 확인
        self.right_move = 0
        self.left_move = 0
        self.up_move = 0
        self.down_move = 0
        # dir은 x이동 dir2는 y 이동
        self.dir = 0
        self.dir2 = 0
        self.move_check = False
        # 얼굴 보는 방향
        self.face_dir = 1
        self.image = load_image('character.png')
        self.hp_bar_image = load_image('source/HP_bar.png')
        self.hp_image = load_image('source/HP_life.png')
        self.exp_bar_image = load_image('source/EXP_bar.png')
        self.exp_image = load_image('source/EXP_exp.png')

        self.level_sound = load_wav('source/levelup.wav')
        self.level_sound.set_volume(48)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = ['sword', 'magic', 'magic2', 'bow', 'ring', 'amor', 'glove', 'meat']
        # 캐릭터 패시브
        self.hp = 100
        self.hp_max = 100
        self.hit_back = 0
        self.move_speed = 1.0
        self.atk = 6
        self.level = 1
        self.invulnerable_time = 0.2
        self.last_collision_time = 0.0
        # 경험치 최대량은 level*100 이런식으로 구상
        self.Exp = 0  # 경험치를 채운 정도
        self.damage = 10

        self.PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
        self.RUN_SPEED_KMPH = 20.0 * self.move_speed  # Km / Hour
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * self.PIXEL_PER_METER)

        self.sword = Sword(self)
        game_world.add_object(self.sword, 1)

        self.bow = Bow(self)
        game_world.add_object(self.bow, 1)

        self.magic = Magic(self)
        game_world.add_object(self.magic, 1)

        self.magic2 = Magic2(self)
        game_world.add_object(self.magic2, 1)

        self.ring = Ring()
        game_world.add_object(self.ring, 1)
        self.amor = Amor()
        game_world.add_object(self.amor, 1)
        self.glove = Glove()
        game_world.add_object(self.glove, 1)
        self.meat = Meat()

    def update(self):

        if server.play_check is True:
            if self.Exp >= 100 * self.level:
                self.level_sound.play()
                game_framework.push_mode(item_mode)
                self.Exp %= 100
                self.level += 1
            self.state_machine.update()
        else:
            self.right_move = 0
            self.left_move = 0
            self.up_move = 0
            self.down_move = 0
            # dir은 x이동 dir2는 y 이동
            self.dir = 0
            self.dir2 = 0
            self.move_check = False

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size * 4, self.x + self.size, self.y + self.size - 20

    def handle_collision(self, group, other):
        current_time = get_time()
        if server.play_check:
            if group == 'main_character:monster' and current_time - self.last_collision_time > self.invulnerable_time:
                self.last_collision_time = current_time
                self.hp -= 5

                if server.main_character.hp <= 0:
                    game_world.clear()
                    game_framework.change_mode(title_mode)
                pass

    # 장갑을 밀어내는 정도를 높이게 하자
    def level_up_item(self, item_type):
        items = {
            'bow': {'attribute': self.bow, 'max_level': 4},
            'sword': {'attribute': self.sword, 'max_level': 4},
            'magic': {'attribute': self.magic, 'max_level': 4},
            'magic2': {'attribute': self.magic2, 'max_level': 4},
            'ring': {'attribute': self.ring, 'max_level': float('inf'), 'atk_increase': 5},
            'amor': {'attribute': self.amor, 'max_level': float('inf'), 'hp_increase': 20},
            'glove': {'attribute': self.glove, 'max_level': 4, 'hit_back': 4},
            'meat': {'max_level': float('inf'), 'restore_hp': True}
        }

        if item_type in items:
            item_info = items[item_type]

            if 'attribute' in item_info:
                attribute = item_info['attribute']
                attribute.level += 1

                if attribute.level == item_info.get('max_level', float('inf')):
                    self.item.remove(item_type)

            if 'atk_increase' in item_info:
                self.atk += item_info['atk_increase']

            if 'hp_increase' in item_info:
                self.hp_max += item_info['hp_increase']
                self.hp += item_info['hp_increase']

            if 'hit_back' in item_info:
                self.hit_back = item_info['hit_back'] * attribute.level

            if 'restore_hp' in item_info:
                self.hp = self.hp_max


class Exp:
    def __init__(self):

        self.exp_bar_image = load_image('source/EXP_bar.png')
        self.exp_image = load_image('source/EXP_exp.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

    def draw(self):

        self.exp_bar_image.clip_draw(0, 0, 49, 6, get_canvas_width() // 2, get_canvas_height() - 25, 400 + 15, 50)
        self.exp_image.clip_draw(0, 0, 49, 6, get_canvas_width() // 2 + (server.main_character.Exp / server.main_character.level - 100) * 2,
                                 get_canvas_height() - 25, (server.main_character.Exp / server.main_character.level * 4), 32)
    def update(self): pass

# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, clamp, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, \
    SDLK_DOWN, draw_rectangle

import game_framework
from atk import Sword, Swordline, Magic, Bow
import game_world

# 키 입력이 왔을때 각각 따로 키를 계산하지 않고 이미 한번 donw 눌림이 인식된 키는 up이 들어올떄까지 True로 인식시킨다.
# 상하, 좌우 나눌필요는 없고 Run에서 이동값을 계산할때만 따로 반영하면 됨

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

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
        if (main_character.face_dir == 1):
            main_character.image.clip_draw(0, 0, 32, 64, main_character.x, main_character.y)
        elif (main_character.face_dir == -1):
            main_character.image.clip_composite_draw(0, 0, 32, 64, 0, 'h', main_character.x, main_character.y, 32, 64)
        main_character.hp_bar_image.clip_draw(0, 0, 46, 12, main_character.x, main_character.y - 50,
                                              main_character.hp_max + 6, 12)
        main_character.hp_image.clip_draw(0, 0, 30, 6,
                                          main_character.x + (main_character.hp - main_character.hp_max) / 2,
                                          main_character.y - 50, main_character.hp,
                                          6)


class Run:
    @staticmethod
    def enter(main_character, e):
        main_character.dir = 0
        main_character.dir2 = 0

        if check_move_down(main_character, e):
            if (main_character.right_move == 2):
                main_character.dir, main_character.face_dir = 1, 1
            elif (main_character.left_move == 2):
                main_character.dir, main_character.face_dir = -1, -1
            if (main_character.up_move == 2):
                main_character.dir2 = 1
            elif (main_character.down_move == 2):
                main_character.dir2 = -1

    @staticmethod
    def exit(main_character, e):
        pass

    @staticmethod
    def do(main_character):
        main_character.frame = (
                                           main_character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        main_character.x += main_character.dir * RUN_SPEED_PPS * game_framework.frame_time
        main_character.x = clamp(25, main_character.x, 800 - 25)
        main_character.y += main_character.dir2 * RUN_SPEED_PPS * game_framework.frame_time
        main_character.y = clamp(30, main_character.y, 800 - 30)
        pass

    @staticmethod
    def draw(main_character):
        if (main_character.face_dir == 1):
            main_character.image.clip_draw(int(main_character.frame) * 32, 0, 32, 64, main_character.x,
                                           main_character.y)
        elif (main_character.face_dir == -1):
            main_character.image.clip_composite_draw(int(main_character.frame) * 32, 0, 32, 64, 0, 'h',
                                                     main_character.x, main_character.y, 32, 64)
        main_character.hp_bar_image.clip_draw(0, 0, 46, 12, main_character.x, main_character.y - 50,
                                              main_character.hp_max + 6, 12)
        main_character.hp_image.clip_draw(0, 0, 30, 6,
                                          main_character.x + (main_character.hp - main_character.hp_max) / 2,
                                          main_character.y - 50, main_character.hp,
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
        self.x, self.y = 400, 400
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
        self.image = load_image('character_move.png')
        self.hp_bar_image = load_image('source/HP_bar.png')
        self.hp_image = load_image('source/HP_life.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = ['sword', 'magic','bow']
        # 캐릭터 패시브
        self.hp = 50
        self.hp_max = 50
        self.atk_speed = 1.0
        self.level = 1
        # 경험치 최대량은 level*100 이런식으로 구상
        self.level_gage = 0  # 경험치를 채운 정도
        self.damage = 10

    def update(self):
        self.state_machine.update()
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size * 4, self.x + self.size, self.y + self.size - 5

    def handle_collision(self, group, other):
        if group == 'main_character:monster':
            self.hp -= 1
            pass


    def Sword_s(self):
        if 'sword' in self.item:
            sword = Sword(self)
            game_world.add_object(sword)

            sword_line = Swordline(self)
            game_world.add_object(sword_line, 1)
            game_world.add_collision_pair('atk:monster', None, sword_line)
        pass

    def Magic_s(self):
        if 'magic' in self.item:
            magic = Magic(self)
        pass

    def Bow_s(self):
        if 'bow' in self.item:
            bow = Bow(self)
            game_world.add_object(bow, 1)
        pass
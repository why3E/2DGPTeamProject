# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN

import game_world

def check_move_down(boy,e):
    right_move = False
    left_move = False
    up_move = False
    down_move = False
    move_check = False

    if(e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN):
        if(e[1].key == SDLK_RIGHT):
            right_move = True
        if (e[1].key == SDLK_LEFT):
            left_move = True
        if (e[1].key == SDLK_UP):
            up_move = True
        if (e[1].key == SDLK_DOWN):
            down_move = True
    elif (e[0] == 'INPUT' and e[1].type == SDL_KEYUP):
        if (e[1].key == SDLK_RIGHT):
            right_move = False
        if (e[1].key == SDLK_LEFT):
            left_move = False
        if (e[1].key == SDLK_UP):
            up_move = False
        if (e[1].key == SDLK_DOWN):
            down_move = False
    if(right_move or left_move or up_move or down_move):
        move_check = True
    else:
        move_check = False

    return e[0] == 'INPUT' and move_check

# 키 입력이 왔을때 각각 따로 키를 계산하지 않고 이미 한번 donw 눌림이 인식된 키는 up이 들어올떄까지 True로 인식시킨다.
# 상하, 좌우 나눌필요는 없고 Run에서 이동값을 계산할때만 따로 반영하면 됨
#

def time_out(e):
    return e[0] == 'TIME_OUT'


# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        boy.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 4

    @staticmethod
    def draw(boy):
        if (boy.face_dir == 1):
            boy.image.clip_draw(0, 0, 32, 64, 400, 300)
        elif (boy.face_dir == -1):
            boy.image.clip_composite_draw(0, 0, 32, 64, 0, 'h', 400, 300, 32, 64)

class Run:
    @staticmethod
    def enter(boy, e):
        boy.dir = 0
        boy.dir2 = 0

        if check_move_down(boy,e):
            if (e[1].key == SDLK_RIGHT):
                boy.dir = 1
            elif (e[1].key == SDLK_LEFT):
                boy.dir = -1
            if (e[1].key == SDLK_UP):
                boy.dir2 = 1
            elif (e[1].key == SDLK_DOWN):
                boy.dir2 = -1

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 4
        boy.x += boy.dir * 5
        boy.y += boy.dir2 * 5
        pass

    @staticmethod
    def draw(boy):
        if(boy.face_dir == 1):
            boy.image.clip_draw(boy.frame * 32, 0, 32, 64, 400, 300)
        elif(boy.face_dir == -1):
            boy.image.clip_composite_draw(boy.frame * 32, 0, 32, 64 , 0, 'h', 400, 300,32,64)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.transitions = {
            Idle: {check_move_down: Run},
            Run: { check_move_down: Run}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(self.boy,e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 300
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.dir2 = 0
        self.face_dir = 1
        self.image = load_image('character_move.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()

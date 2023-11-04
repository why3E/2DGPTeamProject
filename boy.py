# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN

import game_world

def check_move_down(boy,e):

    if(e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN):
        if(e[1].key == SDLK_RIGHT):
            boy.right_move = 2
            if(boy.left_move == 2):
                boy.left_move = 1
        if (e[1].key == SDLK_LEFT):
            boy.left_move = 2
            if (boy.right_move == 2):
                boy.right_move = 1
        if (e[1].key == SDLK_UP):
            boy.up_move = 2
            if (boy.down_move == 2):
                boy.down_move = 1
        if (e[1].key == SDLK_DOWN):
            boy.down_move = 2
            if (boy.up_move == 2):
                boy.up_move = 1
    elif (e[0] == 'INPUT' and e[1].type == SDL_KEYUP):
        if (e[1].key == SDLK_RIGHT and boy.right_move !=0):
            boy.right_move = 0
            if(boy.left_move == 1):
                boy.left_move = 2
        if (e[1].key == SDLK_LEFT and boy.left_move !=0):
            boy.left_move = 0
            if(boy.right_move == 1):
                boy.right_move = 2
        if (e[1].key == SDLK_UP and boy.up_move != 0):
            boy.up_move = 0
            if (boy.down_move == 1):
                boy.down_move = 2
        if (e[1].key == SDLK_DOWN and boy.down_move != 0):
            boy.down_move = 0
            if (boy.up_move == 1):
                boy.up_move = 2
    if(boy.right_move or boy.left_move or boy.up_move or boy.down_move):
        move_check = True
    else:
        move_check = False

    return e[0] == 'INPUT' and move_check

def check_move_up(boy,e):
    if(boy.move_check == False):
        return e[0] == 'INPUT' and True
    else:
        return e[0] == 'INPUT' and False

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
            if (boy.right_move==2):
                boy.dir = 1
            elif (boy.left_move==2):
                boy.dir = -1
            if (boy.up_move==2):
                boy.dir2 = 1
            elif (boy.down_move==2):
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
            Idle: {check_move_down: Run,check_move_up: Idle},
            Run: { check_move_down: Run,check_move_up: Idle}
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
        self.right_move = 0
        self.left_move = 0
        self.up_move = 0
        self.down_move = 0
        self.dir = 0
        self.dir2 = 0
        self.face_dir = 1
        self.image = load_image('character_move.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.move_check = False

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
    def draw(self):
        self.state_machine.draw()

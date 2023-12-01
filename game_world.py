import item_mode
import play_mode

objects = [[] for _ in range(4)]


# fill here

def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


# fill here
def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def clear_collision_objects():
    for pairs in collision_pairs.values():
        pairs[0].clear()
        pairs[1].clear()

def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)#시각적 월드에서 지운다.
            remove_collision_object(o) # 충돌 그룹에서 삭제 완료
            del o # 객체자체를 완전히 메모리에서 제거
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()
        clear_collision_objects()


# fill here
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


collision_pairs = {}


# {'boy:ball' : [[a],[b]]}
def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        print(f'Added new group {group}')
        collision_pairs[group] = [[], []]
    if a:  # a가 있을떄, 즉 a가 None이 아니면 추가
        collision_pairs[group][0].append(a)
    if b:  # b가 있을떄, 즉 b가 None이 아니면 추가
        collision_pairs[group][1].append(b)


def handle_collisions():
    # 등록된 모든 충돌 상황에 대해서 충돌 검사 및 충돌처리 수행
    for group, pairs in collision_pairs.items():  # key 'boy:ball',value[[][]]
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def add_object_pair(group, a, b):
    if a not in objects:
        print(f'Added new group {group}')
        collision_pairs[group] = [[], []]
    if a:  # a가 있을떄, 즉 a가 None이 아니면 추가
        collision_pairs[group][0].append(a)
    if b:  # b가 있을떄, 즉 b가 None이 아니면 추가
        collision_pairs[group][1].append(b)
import random
import time

from pico2d import *

import game_framework
import game_world
import play_mode


class Ring:
    Ring_image = None
    image1 = None
    image2 = None
    image3 = None
    image4 = None

    def __init__(self):
        self.level = 1
        self.load_images()
        self.image_dict = {
            1: Ring.image1,
            2: Ring.image2,
            3: Ring.image3,
            4: Ring.image4
        }

    def load_images(self):
        if Ring.Ring_image is None:
            Ring.image1 = load_image('source/ring_01.png')
            Ring.image2 = load_image('source/ring_02.png')
            Ring.image3 = load_image('source/ring_03.png')
            Ring.image4 = load_image('source/ring_04.png')
            Ring.Ring_image = Ring.image1

    def draw(self):pass
    def update(self):pass
class Glove:
    Glove_image = None
    image1 = None
    image2 = None
    image3 = None
    image4 = None

    def __init__(self):
        self.level = 1
        self.load_images()
        self.image_dict = {
            1: Glove.image1,
            2: Glove.image2,
            3: Glove.image3,
            4: Glove.image4
        }

    def load_images(self):
        if Glove.Glove_image is None:
            Glove.image1 = load_image('source/glove_00.png')
            Glove.image2 = load_image('source/glove_01.png')
            Glove.image3 = load_image('source/glove_02.png')
            Glove.image4 = load_image('source/glove_03.png')
            Glove.Glove_image = Glove.image1

    def draw(self):pass
    def update(self):pass

class Amor:
    Amor_image = None
    image1 = None
    image2 = None
    image3 = None
    image4 = None

    def __init__(self):
        self.level = 1
        self.load_images()
        self.image_dict = {
            1: Amor.image1,
            2: Amor.image2,
            3: Amor.image3,
            4: Amor.image4
        }

    def load_images(self):
        if Amor.Amor_image is None:
            Amor.image1 = load_image('source/shield_00.png')
            Amor.image2 = load_image('source/shield_01.png')
            Amor.image3 = load_image('source/shield_02.png')
            Amor.image4 = load_image('source/shield_03.png')
            Amor.Amor_image = Amor.image1

    def draw(self):pass
    def update(self):pass

class Meat:
    Meat_image = None
    def __init__(self):
        if Meat.Meat_image is None:
            Meat.Meat_image = load_image('source/meat.png')

    def draw(self):pass
    def update(self):pass


class Coin:
    image1 = None
    image2 = None
    sound = None
    def __init__(self, other,type):
        if Coin.image1 is None:
            Coin.image1 = load_image('source/coin.png')
            Coin.image2 = load_image('source/coins.png')
        if Coin.sound is None:
            Coin.sound = load_wav('source/coin.wav')
            Coin.sound.set_volume(20)
        self.image = self.set_image(type)
        self.x = other.x
        self.y = other.y
        self.size = 10

    def update(self):
        pass
    def draw(self):
        sx = self.x - play_mode.background.window_left
        sy = self.y - play_mode.background.window_bottom
        self.image.draw(sx, sy, 20, 20)

    # fill here
    def get_bb(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        if group == 'Main:Coin':
            Coin.sound.play()
            play_mode.main_character.Exp += 20
            game_world.remove_object(self)

    def set_image(self,type):
        if type == 'monster':
            return Coin.image1
        elif type =='middle_monster':
            return Coin.image2
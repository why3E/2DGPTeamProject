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
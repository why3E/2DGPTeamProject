import random

from pico2d import load_image, get_canvas_width, get_canvas_height

import pasive_item
import play_mode
import atk_item


class Pannel:
    def __init__(self):
        self.image = load_image('source/select_UI.png')
        self.choice_image = load_image('source/choice_UI.png')
        self.check = 0
        self.choice_size1 = 280
        self.choice_size2 = 200
        self.choice_size3 = 200
        self.item_random_choice = random.sample(play_mode.main_character.item, 3)
        self.cw = get_canvas_width()//2
        self.ch = get_canvas_height()//2
    def draw(self):
        self.image.draw(self.cw, self.ch,400,500)
        self.choice_image.draw(self.cw, 600, self.choice_size1, 100)
        self.choice_image.draw(self.cw, 450, self.choice_size2,100)
        self.choice_image.draw(self.cw, 300, self.choice_size3, 100)
        self.draw_item(self.item_random_choice[0],600)
        self.draw_item(self.item_random_choice[1], 450)
        self.draw_item(self.item_random_choice[2], 300)

    def update(self):
        if self.check == 0:
            self.choice_size1 = 280
            self.choice_size2 = 200
            self.choice_size3 = 200
        elif self.check == 1:
            self.choice_size1 = 200
            self.choice_size2 = 280
            self.choice_size3 = 200
        elif self.check == 2:
            self.choice_size1 = 200
            self.choice_size2 = 200
            self.choice_size3 = 280
        pass

    def draw_item(self, a, y):
        if a == 'sword':
            atk_item.Sword.image.draw(self.cw, y, 50, 50)
        elif a == 'bow':
            atk_item.Bow.Bow_image.draw(self.cw, y, 50, 50)
        elif a == 'magic':
            atk_item.Magic.Magic_image.draw(self.cw, y, 50, 50)
        elif a == 'ring':
            pasive_item.Ring.Ring_image.draw(self.cw, y, 50, 50)
        elif a == 'amor':
            pasive_item.Amor.Amor_image.draw(self.cw, y, 50, 50)
        elif a == 'glove':
            pasive_item.Glove.Glove_image.draw(self.cw, y, 50, 50)
        elif a == 'meat':
            pasive_item.Meat.Meat_image.draw(self.cw, y, 50, 50)
        elif a == 'magic2':
            atk_item.Magic2.Magic2_image.draw(self.cw, y, 50, 50)

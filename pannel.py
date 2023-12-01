import random

from pico2d import load_image

import pasive_item
import play_mode
import atk_item


class Pannel:
    def __init__(self):
        self.image = load_image('source/select_UI.png')
        self.choice_image = load_image('source/choice_UI.png')
        self.check = 0
        self.choice_size1 = 380
        self.choice_size2 = 300
        self.choice_size3 = 300
        self.item_random_choice = random.sample(play_mode.main_character.item, 3)

    def draw(self):
        self.image.draw(400, 400,400,500)
        self.choice_image.draw(400, 550, self.choice_size1, 100)
        self.choice_image.draw(400, 400, self.choice_size2,100)
        self.choice_image.draw(400, 250, self.choice_size3, 100)
        self.draw_item(self.item_random_choice[0],550)
        self.draw_item(self.item_random_choice[1], 400)
        self.draw_item(self.item_random_choice[2], 250)

    def update(self):
        if self.check == 0:
            self.choice_size1 = 380
            self.choice_size2 = 300
            self.choice_size3 = 300
        elif self.check == 1:
            self.choice_size1 = 300
            self.choice_size2 = 380
            self.choice_size3 = 300
        elif self.check == 2:
            self.choice_size1 = 300
            self.choice_size2 = 300
            self.choice_size3 = 380
        pass

    def draw_item(self, a, y):
        if a == 'sword':
            atk_item.Sword.image.draw(300, y, 50, 50)
        elif a == 'bow':
            atk_item.Bow.Bow_image.draw(300, y, 50, 50)
        elif a == 'magic':
            atk_item.Magic.Magic_image.draw(300, y, 50, 50)
        elif a == 'ring':
            pasive_item.Ring.Ring_image.draw(300, y, 50, 50)
        elif a == 'amor':
            pasive_item.Amor.Amor_image.draw(300, y, 50, 50)
        elif a == 'glove':
            pasive_item.Glove.Glove_image.draw(300, y, 50, 50)
        elif a == 'meat':
            pasive_item.Meat.Meat_image.draw(300, y, 50, 50)

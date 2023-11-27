import random

from pico2d import load_image
import play_mode
import atk


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
            atk.Sword.image.draw(300, y, 50, 50)
        elif a == 'bow':
            atk.Bow.Bow_image.draw(300, y, 50, 50)
        elif a == 'magic':
            atk.Magic.Magic_image.draw(300, y, 50, 50)
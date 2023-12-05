import random

from pico2d import load_image, get_canvas_width, get_canvas_height, load_font

import pasive_item
import play_mode
import atk_item
import server


class Pannel:
    def __init__(self):
        self.image = load_image('source/select_UI.png')
        self.choice_image = load_image('source/choice_UI.png')
        self.check = 0
        self.choice_size1 = 380
        self.choice_size2 = 300
        self.choice_size3 = 300
        self.item_random_choice = random.sample(server.main_character.item, 3)
        self.cw = get_canvas_width() // 2
        self.ch = get_canvas_height() // 2
        self.font = load_font('source/ENCR10B.TTF', 20)
        self.item_data = {
            'sword': {'image': atk_item.Sword.image, 'description': 'attack speed up'},
            'bow': {'image': atk_item.Bow.Bow_image, 'description': 'arrow speed up'},
            'magic': {'image': atk_item.Magic.Magic_image, 'description': 'magic speed up'},
            'ring': {'image': pasive_item.Ring.Ring_image, 'description': 'damage up'},
            'amor': {'image': pasive_item.Amor.Amor_image, 'description': 'HP, HP MAX up'},
            'glove': {'image': pasive_item.Glove.Glove_image, 'description': 'Knock Back up'},
            'meat': {'image': pasive_item.Meat.Meat_image, 'description': 'Full HP'},
            'magic2': {'image': atk_item.Magic2.Magic2_image, 'description': 'Tornado speed up'}
        }
    def draw(self):
        self.image.draw(self.cw, self.ch, 400, 500)
        self.choice_image.draw(self.cw, 600, self.choice_size1, 100)
        self.choice_image.draw(self.cw, 450, self.choice_size2, 100)
        self.choice_image.draw(self.cw, 300, self.choice_size3, 100)
        self.draw_item(self.item_random_choice[0], 600)
        self.draw_item(self.item_random_choice[1], 450)
        self.draw_item(self.item_random_choice[2], 300)

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

    def draw_item(self, item_type, y):
        if item_type in self.item_data:
            item = self.item_data[item_type]
            item['image'].draw(self.cw - 100, y, 50, 50)
            self.font.draw(self.cw - 50, y, item['description'], (0, 0, 0))
        else:
            # Handle unknown item type
            print(f"Unknown item type: {item_type}")
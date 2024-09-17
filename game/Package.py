import random


class Package:
    def __init__(self, pos):
        self.pos = pos
        self.number = random.randint(1, 9)  # Generate a random number
        self.picked_up = False
        self.visible = True

    def pick_up(self):
        self.picked_up = True

    def drop_off(self):
        self.picked_up = False
        self.number = None

    def set_position(self, pos):
        self.pos = pos

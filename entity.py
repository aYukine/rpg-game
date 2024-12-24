import pygame as pg
from settings import *

class Entity:
    def __init__(self, x, y, name, hp):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.width = 50
        self.height = 50

    def draw(self, master, offsetx, offsety):
        pg.draw.rect(master, WHITE, (self.x+offsetx-self.width//2, self.y+offsety-self.height//2, self.width, self.height))
        print(self.x+offsetx, self.y+offsety)

class Player(Entity):
    def __init__(self, name, hp, x, y):
        super().__init__(x, y, name, hp)

    def shoot():
        pass

class Enemy(Entity):
    def __init__(self, name, hp, x, y):
        super().__init__(x, y, name, hp)
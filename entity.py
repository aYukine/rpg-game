import pygame as pg
from settings import *


# entity
class Entity:
    def __init__(self, x, y, name, hp):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.width = width
        self.height = height

    def draw(self, master, offsetx, offsety):
        pg.draw.rect(master, WHITE, (self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height))

class Player(Entity):
    def __init__(self, name, hp, x, y):
        super().__init__(x, y, name, hp)

    def shoot():
        pass

class Enemy(Entity):
    def __init__(self, name, hp, x, y):
        super().__init__(x, y, name, hp)

class Passive(Entity):
    def __init__(self, name, hp, x, y):
        super().__init__(x, y, name, hp)

class Projectile:
    def __init__(self, x, y, vector):
        self.x = x
        self.y = y
        self.radius = 5
        self.vector = vector

    def move(self, dt):
        self.x += self.vector[0]*dt*bullet_speed
        self.y += self.vector[1]*dt*bullet_speed
    
    def draw(self, master, offsetx, offsety):
        pg.draw.circle(master, WHITE, (self.x-offsetx, self.y-offsety), self.radius)

class Bullets(Projectile):
    def __init__(self, x, y, vector):
        super().__init__(x, y, vector)

# blocks

class Block():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = None

    def draw(self, master, offsetx, offsety):
        pg.draw.rect(master, WHITE, (self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height))

        
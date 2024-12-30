import pygame as pg
from settings import *


# entity
class Entity:
    def __init__(self, x, y, name, hp, offsetx, offsety):
        self.x = x
        self.y = y
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height)
        self.invincibility = 1
        self.invincibility_cooldown = 1

    def draw(self, master, offsetx, offsety):
        self.rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height)
        pg.draw.rect(master, WHITE, (self.x-offsetx-self.width//2, self.y-offsety-self.height, self.width, 10))
        pg.draw.rect(master, RED, (self.x-offsetx-self.width//2+2, self.y-offsety-self.height+1, self.width*(self.hp/self.max_hp)-4, 8))
        pg.draw.rect(master, WHITE, (self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height))

    def move(self, x, y):
        self.x += x
        self.y += y

    def take_damage(self, damage):
        if self.invincibility <= 0:
            self.hp -= 10
            self.invincibility = self.invincibility_cooldown

    def process(self, dt):
        self.invincibility -= dt

class Player(Entity):
    def __init__(self, name, hp, x, y, offsetx, offsety):
        super().__init__(x, y, name, hp, offsetx, offsety)

class Enemy(Entity):
    def __init__(self, name, hp, x, y, offsetx, offsety):
        super().__init__(x, y, name, hp, offsetx, offsety)

class Passive(Entity):
    def __init__(self, name, hp, x, y, offsetx, offsety):
        super().__init__(x, y, name, hp, offsetx, offsety)

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

        
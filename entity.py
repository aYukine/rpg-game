import pygame as pg
from settings import *


# entity
class Entity:
    def __init__(self, x, y, name, hp, offsetx, offsety, sprite, width=50, height=50):
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
        self.sprite = sprite
        self.sprite_index = 0
        self.sprite_counter = 0

    def draw(self, master:pg.Surface, offsetx, offsety):
        self.rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height)
        pg.draw.rect(master, WHITE, (self.x-offsetx-self.width//2, self.y-offsety-self.height, self.width, 10))
        pg.draw.rect(master, RED, (self.x-offsetx-self.width//2+2, self.y-offsety-self.height+1, self.width*(self.hp/self.max_hp)-4, 8))
        master.blit(self.sprite[self.sprite_index], (self.x-offsetx-self.width//2, self.y-offsety-self.height//2))

    def move(self, x, y, dt):
        self.sprite_counter += dt
        self.x += x*dt
        self.y += y*dt
        if self.sprite_counter > 0.2:
            if x > 0 and abs(x)>=abs(y):
                self.sprite_index = (self.sprite_index+1) % 3 + 6
            elif x < 0 and abs(x)>=abs(y):
                self.sprite_index = (self.sprite_index+1) % 3 + 3
            elif y > 0 and abs(y)>abs(x):
                self.sprite_index = (self.sprite_index+1) % 3 
            elif y < 0 and abs(y)>abs(x):
                self.sprite_index = (self.sprite_index+1) % 3 + 9
            self.sprite_counter = 0

    def take_damage(self, damage):
        if self.invincibility <= 0:
            self.hp -= damage
            self.invincibility = self.invincibility_cooldown
            if self.hp < 0:
                self.hp = 0

    def process(self, dt):
        self.invincibility -= dt

class Player(Entity):
    def __init__(self, name, hp, x, y, offsetx, offsety, sprite, width=50, height=50):
        super().__init__(x, y, name, hp, offsetx, offsety, sprite, width, height)

class Enemy(Entity):
    def __init__(self, name, hp, x, y, offsetx, offsety, sprite, width=50, height=50):
        super().__init__(x, y, name, hp, offsetx, offsety, sprite, width, height)

class Passive(Entity):
    def __init__(self, name, hp, x, y, offsetx, offsety, sprite, width=50, height=50):
        super().__init__(x, y, name, hp, offsetx, offsety, sprite, width, height)

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
    def __init__(self, sprite):
        self.sprite = sprite
        self.rect = pg.Rect(0, 0, 50, 50)
        self.x = 0
        self.y = 0
        self.width = 50
        self.height = 50

    def update_rect(self, x, y):
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, 50, 50)

    def fix_collision(self, entity, offsetx, offsety):
        if self.rect.colliderect(entity.rect):
            error_x = entity.x - self.x - offsetx
            error_y = entity.y - self.y - offsety

            if error_x > 25:
                entity.x += 25
            elif error_x <= -25:
                entity.x -= 25
            if error_y > 25:
                entity.y += 25
            elif error_y <= -25:
                entity.y -= 25        
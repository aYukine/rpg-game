import pygame as pg
from settings import *

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
        self.left_rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2, 10, self.height)
        self.right_rect = pg.Rect(self.x-offsetx+self.width//2-10, self.y-offsety-self.height//2, 10, self.height)
        self.top_rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, 10)
        self.bottom_rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety+self.height//2-10, self.width, 10)
        self.invincibility = 1
        self.invincibility_cooldown = 1
        self.sprite = sprite
        self.sprite_index = 0
        self.sprite_counter = 0
        self.collision = [0, 0, 0, 0]

    def draw(self, master:pg.Surface, offsetx, offsety):
        self.rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height)
        self.left_rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2+10, 10, self.height-20)
        self.right_rect = pg.Rect(self.x-offsetx+self.width//2-10, self.y-offsety-self.height//2+10, 10, self.height-20)
        self.top_rect = pg.Rect(self.x-offsetx-self.width//2+10, self.y-offsety-self.height//2, self.width-20, 10)
        self.bottom_rect = pg.Rect(self.x-offsetx-self.width//2+10, self.y-offsety+self.height//2-10, self.width-20, 10)
        pg.draw.rect(master, WHITE, (self.x-offsetx-self.width//2, self.y-offsety-self.height, self.width, 10))
        pg.draw.rect(master, RED, (self.x-offsetx-self.width//2+2, self.y-offsety-self.height+1, self.width*(self.hp/self.max_hp)-4, 8))
        master.blit(self.sprite[self.sprite_index], (self.x-offsetx-self.width//2, self.y-offsety-self.height//2))

    def check_rect_collide_block(self, blocks:Block):
        
        self.collision = [0, 0, 0, 0]
        for row in blocks:
            for b in row:
                if type(b) != Block:
                    continue
                if self.left_rect.colliderect(b.rect) or self.collision[0] == 1:
                    self.collision[0] = 1
                else:
                    self.collision[0] = 0
                if self.right_rect.colliderect(b.rect) or self.collision[1] == 1:
                    self.collision[1] = 1
                else:
                    self.collision[1] = 0
                if self.top_rect.colliderect(b.rect) or self.collision[2] == 1:
                    self.collision[2] = 1
                else:
                    self.collision[2] = 0
                if self.bottom_rect.colliderect(b.rect) or self.collision[3] == 1:
                    self.collision[3] = 1
                else:
                    self.collision[3] = 0
            print(self.collision)

    def move(self, x, y, dt):
        self.sprite_counter += dt
        if self.collision[0] and x < 0:
            x = 0
        if self.collision[1] and x > 0:
            x = 0
        if self.collision[2] and y < 0:
            y = 0
        if self.collision[3] and y > 0:
            y = 0
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

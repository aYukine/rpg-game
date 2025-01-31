import pygame as pg
from settings import *
import utils

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
        self._sprite_index = 0
        self._sprite_counter = 0
        self.collision = [0, 0, 0, 0]
        self.draw_health = True

    def draw(self, master:pg.Surface, offsetx, offsety):
        self.rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height)
        self.left_rect = pg.Rect(self.x-offsetx-self.width//2, self.y-offsety-self.height//2+10, 10, self.height-20)
        self.right_rect = pg.Rect(self.x-offsetx+self.width//2-10, self.y-offsety-self.height//2+10, 10, self.height-20)
        self.top_rect = pg.Rect(self.x-offsetx-self.width//2+10, self.y-offsety-self.height//2, self.width-20, 10)
        self.bottom_rect = pg.Rect(self.x-offsetx-self.width//2+10, self.y-offsety+self.height//2-10, self.width-20, 10)
        if self.draw_health:
            pg.draw.rect(master, WHITE, (self.x-offsetx-self.width//2, self.y-offsety-self.height, self.width, 10))
            pg.draw.rect(master, RED, (self.x-offsetx-self.width//2+2, self.y-offsety-self.height+1, self.width*(self.hp/self.max_hp)-4, 8))
        if self.sprite:
            if type(self.sprite) == list:
                master.blit(self.sprite[self._sprite_index], 
                            (self.x-offsetx-self.width//2, 
                            self.y-offsety-self.height//2))
            else:
                master.blit(self.sprite, (self.x-offsetx-self.width//2, self.y-offsety-self.height//2))
        else:
            pg.draw.rect(master, RED, (self.x-offsetx-self.width//2, self.y-offsety-self.height//2, self.width, self.height))

    def check_rect_collide_block(self, blocks):
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

    def move(self, x, y, dt):
        self._sprite_counter += dt
        if self.collision[0] and x < 0:
            self._sprite_index = 3
            x = 0
        if self.collision[1] and x > 0:
            self._sprite_index = 6
            x = 0
        if self.collision[2] and y < 0:
            self._sprite_index = 9
            y = 0
        if self.collision[3] and y > 0:
            self._sprite_index = 0
            y = 0
        self.x += x*dt
        self.y += y*dt
        if self._sprite_counter > 0.2:
            if x > 0 and abs(x)>=abs(y):
                self._sprite_index = (self._sprite_index+1) % 3 + 6
            elif x < 0 and abs(x)>=abs(y):
                self._sprite_index = (self._sprite_index+1) % 3 + 3
            elif y > 0 and abs(y)>abs(x):
                self._sprite_index = (self._sprite_index+1) % 3 
            elif y < 0 and abs(y)>abs(x):
                self._sprite_index = (self._sprite_index+1) % 3 + 9
            self._sprite_counter = 0

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
        self.draw_health = False
        self.quest_accepted = False
        self.dialog = []

    def draw_speech(self, surface, text, image=None):
        font = pg.font.Font(None, 24)
        margin = 20
        spacing = 10
        max_width = 300  # adjust as needed

        # Simple text-wrapping function
        def wrap_text(txt, fnt, max_w):
            words = txt.split()
            lines = []
            current_line = ""
            for w in words:
                test_line = (current_line + " " + w).strip()
                if fnt.size(test_line)[0] <= max_w:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = w
            if current_line:
                lines.append(current_line)
            return lines

        lines = wrap_text(text, font, max_width)
        img_w, img_h = (0, 0) if not image else image.get_size()

        # Calculate box width & height based on lines and optional image
        text_lines_height = len(lines) * font.get_height()
        box_w = max(img_w, max_width) + margin * 2
        box_h = margin * 2 + text_lines_height + (img_h + spacing if image else 0)

        # Position box above the entity
        box_x = self.rect.centerx - box_w // 2
        box_y = self.rect.top - box_h - 10
        pg.draw.rect(surface, (255, 255, 255), (box_x, box_y, box_w, box_h))

        # Draw optional image at top center
        current_y = box_y + margin
        if image:
            surface.blit(image, (box_x + (box_w - img_w) // 2, current_y))
            current_y += img_h + spacing

        # Draw each wrapped line
        for line in lines:
            text_surf = font.render(line, True, (0, 0, 0))
            line_w = text_surf.get_width()
            surface.blit(text_surf, (box_x + (box_w - line_w) // 2, current_y))
            current_y += font.get_height()
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

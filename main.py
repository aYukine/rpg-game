import pygame as pg
from settings import *
import utils
import entity
import time
from resource_loader import *

pg.init()

class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((screenx, screeny))
        convert_images()
        self.clock = pg.time.Clock()
        self.offset_x = -screenx//2
        self.offset_y = -screeny//2
        self.run = True
        self.player = entity.Player("Player", 200, 0, 0)
        self.enemy = entity.Enemy("Enemy", 100, 100, 100)
        self.current_time = time.perf_counter()
        self.map = utils.map_reader("resource/map.csv")
        self.map_offsetx = (player_starting[0]-1)*width
        self.map_offsety = (player_starting[1]-1)*height
        self.projectiles = []
        self.start = False

    def controller_handle(self, dt, key, mouse):
        mx, my = pg.mouse.get_pos()
        if mouse:
            self.projectiles.append(entity.Bullets(self.player.x, self.player.y, utils.find_bullet_vector(self.player.x, self.player.y, mx+self.offset_x, my+self.offset_y)))
        press = pg.key.get_pressed()
        if press[pg.K_w]:
            self.player.y -= dt*player_speed
        if press[pg.K_s]:
            self.player.y += dt*player_speed
        if press[pg.K_a]:
            self.player.x -= dt*player_speed
        if press[pg.K_d]:
            self.player.x += dt*player_speed

        self.update_global_xy()

    def handle_games(self, dt, key, mouse):
        self.controller_handle(dt, key, mouse)
        for p in self.projectiles:
            p.move(dt)
        
    def update_global_xy(self): 
        self.offset_x = self.player.x - screenx//2
        self.offset_y = self.player.y - screeny//2

    
    def map_builder_old(self):
        for i, row in enumerate(self.map):
            for j, block in enumerate(row):
                self.screen.blit(block_decoder[block], (j*width-width//2-self.offset_x-self.map_offsetx, i*height-height//2-self.offset_y-self.map_offsety))

    def map_builder(self):
        for i in range(int(self.player.y//height + player_starting[1] - 12), int(self.player.y//height + player_starting[1] + 12)):
            if i > len(self.map)-1 or i < 0:
                continue
            for j in range(int(self.player.x//width + player_starting[0] - 12), int(self.player.x//width + player_starting[0] + 12)):
                if j > len(self.map[i])-1 or j < 0:
                    continue
                self.screen.blit(block_decoder[self.map[i][j]], (j*width-width//2-self.offset_x-self.map_offsetx, i*height-height//2-self.offset_y-self.map_offsety))

    def draw(self):
        self.screen.fill(BLACK)
        self.map_builder()
        self.player.draw(self.screen, self.offset_x, self.offset_y)
        self.enemy.draw(self.screen, self.offset_x, self.offset_y)
        utils.write(self.screen, WHITE, f"x: {self.player.x/width:.2f}, y: {self.player.y/width:.2f}", 10, 20, "TOPLEFT", 30)
        for p in self.projectiles:
            if utils.distant_from_player(p.x, p.y, self.player.x, self.player.y) > 1000:
                self.projectiles.remove(p)
            p.draw(self.screen, self.offset_x, self.offset_y)
        pg.display.flip()

    def menu(self, key):
        if key == pg.K_SPACE:
            self.start = True

    def mainloop(self):
        while self.run:
            key = None
            mouse = False
            dt = time.perf_counter() - self.current_time
            self.current_time = time.perf_counter()
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                if event.type == pg.KEYDOWN:
                    key = event.key
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse = True

            if self.start == False:
                self.menu(key)
                continue
            self.handle_games(dt, key, mouse)
            self.draw()
            
def main():
    game = Game()
    game.mainloop()
    pg.quit()

if __name__ == "__main__":
    main()
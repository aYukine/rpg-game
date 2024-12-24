import pygame as pg
import socket
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
        print(self.map_offsetx, self.map_offsety)

    def handle_games(self, dt):
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

    def update_global_xy(self): 
        self.offset_x = self.player.x - screenx//2
        self.offset_y = self.player.y - screeny//2

    def map_builder(self):
        for i, row in enumerate(self.map):
            for j, block in enumerate(row):
                self.screen.blit(block_decoder[block], (j*width-width//2-self.offset_x-self.map_offsetx, i*height-height//2-self.offset_y-self.map_offsety))

    def draw(self):
        self.screen.fill(BLACK)
        self.map_builder()
        self.player.draw(self.screen, self.offset_x, self.offset_y)
        self.enemy.draw(self.screen, self.offset_x, self.offset_y)
        utils.write(self.screen, WHITE, f"x: {self.player.x/width:.2f}, y: {self.player.y/width:.2f}", 10, 20, "TOPLEFT", 30)
        pg.display.flip()

    def mainloop(self):
        while self.run:
            dt = time.perf_counter() - self.current_time
            self.current_time = time.perf_counter()
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
            self.handle_games(dt)
            self.draw()
            
def main():
    game = Game()
    game.mainloop()
    pg.quit()

if __name__ == "__main__":
    main()
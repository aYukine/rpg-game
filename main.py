import pygame as pg
import socket
from settings import *
import utils
import entity
import time

pg.init()

class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((screenx, screeny))
        self.clock = pg.time.Clock()
        self.global_x = screenx//2
        self.global_y = screeny//2
        self.run = True
        self.player = entity.Player("Player", 200, 0, 0)
        self.enemy = entity.Enemy("Enemy", 100, 100, 100)
        self.current_time = time.perf_counter()

    def handle_games(self, dt):
        press = pg.key.get_pressed()
        if press[pg.K_w]:
            self.global_y += dt*player_speed
            self.player.y -= dt*player_speed
        if press[pg.K_s]:
            self.global_y -= dt*player_speed
            self.player.y += dt*player_speed
        if press[pg.K_a]:
            self.global_x += dt*player_speed
            print("hi")
            self.player.x -= dt*player_speed
        if press[pg.K_d]:
            self.global_x -= dt*player_speed
            self.player.x += dt*player_speed

    def draw(self):
        self.screen.fill((0, 0, 0)) # background
        self.player.draw(self.screen, self.global_x, self.global_y)
        self.enemy.draw(self.screen, self.global_x, self.global_y)
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
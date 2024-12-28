import pygame as pg
from settings import *
import utils
import entity
import time
from resource_loader import *
import threading
import time

pg.init()

class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((screenx, screeny))
        self.clock = pg.time.Clock()
        self.offset_x = -screenx//2
        self.offset_y = -screeny//2
        self.run = True
        self.player = entity.Player("Player", 200, 0, 0)
        self.current_time = time.perf_counter()
        self.map = None
        self.map_offsetx = (player_starting[0]-1)*width
        self.map_offsety = (player_starting[1]-1)*height
        self.projectiles = []
        self.enemies = []

        self.loaded = False
        
        self.enemies.append(entity.Enemy("Enemy", 100, 100, 100))
        self.start = False

    def load_game(self):
        load_data()
        self.map = utils.map_reader("resource/map.csv")
        time.sleep(5)
        self.loaded = True

    def controller_handle(self, dt, key, mouse):
        mx, my = pg.mouse.get_pos()
        x, y = 0, 0
        if mouse:
            self.projectiles.append(entity.Bullets(self.player.x, self.player.y, utils.find_bullet_vector(self.player.x, self.player.y, mx+self.offset_x, my+self.offset_y)))
        press = pg.key.get_pressed()
        if press[pg.K_w]:
            y -= dt*player_speed
        if press[pg.K_s]:
            y += dt*player_speed
        if press[pg.K_a]:
            x -= dt*player_speed
        if press[pg.K_d]:
            x += dt*player_speed
        
        self.player.move(x, y, self.offset_x, self.offset_y)
        self.update_global_xy()

    def handle_games(self, dt, key, mouse):
        self.controller_handle(dt, key, mouse)
        for p in self.projectiles:
            p.move(dt)

        for e in self.enemies:
            if utils.distant_from_player(e.x, e.y, self.player.x, self.player.y) < 400:
                e.move((self.player.x - e.x) * dt, (self.player.y - e.y) * dt, self.offset_x, self.offset_y)
            for p in self.projectiles:
                if e.rect.colliderect(pg.Rect(p.x-self.offset_x-5, p.y-self.offset_y-5, 10, 10)):
                    e.hp -= 10
                    self.projectiles.remove(p)
            if e.hp <= 0:
                self.enemies.remove(e)
        
    def update_global_xy(self): 
        self.offset_x = self.player.x - screenx//2
        self.offset_y = self.player.y - screeny//2

    def map_builder(self):
        pass
        # start_y = int(self.player.y // height + player_starting[1] - 4)
        # end_y = int(self.player.y // height + player_starting[1] + 4)
        # start_x = int(self.player.x // width + player_starting[0] - 4)
        # end_x = int(self.player.x // width + player_starting[0] + 4)

        # offset_x = self.offset_x + self.map_offsetx
        # offset_y = self.offset_y + self.map_offsety
        # half_width = width // 2
        # half_height = height // 2

        # for i in range(start_y, end_y):
        #     if 0 <= i < len(self.map):
        #         for j in range(start_x, end_x):
        #             if 0 <= j < len(self.map[i]):
        #                 block = block_decoder.get(self.map[i][j])
        #                 if block:
        #                     self.screen.blit(block, (j * width - half_width - offset_x, i * height - half_height - offset_y))

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.map, (-self.map_offsetx-self.offset_x, -self.map_offsety-self.offset_y))
        self.map_builder()
        self.player.draw(self.screen, self.offset_x, self.offset_y)
        for e in self.enemies:
            e.draw(self.screen, self.offset_x, self.offset_y)
        utils.write(self.screen, WHITE, f"x: {self.player.x/width:.2f}, y: {self.player.y/width:.2f}", 10, 20, "TOPLEFT", 30)
        for p in self.projectiles:
            if utils.distant_from_player(p.x, p.y, self.player.x, self.player.y) > 1000:
                self.projectiles.remove(p)
            p.draw(self.screen, self.offset_x, self.offset_y)
        pg.display.flip()

    def menu(self, key):
        self.screen.fill(BLACK)
        if not self.loaded:
            utils.write(self.screen, WHITE, "Loading...", screenx//2, screeny//2, "MIDDLE", 30)
        else:
            utils.write(self.screen, WHITE, "Press SPACE to start", screenx//2, screeny//2, "MIDDLE", 30)
        if key == pg.K_SPACE and self.loaded:
            self.start = True

        pg.display.flip()

    def mainloop(self):
        loader = threading.Thread(target=self.load_game)
        loader.daemon = True
        loader.start()
        while self.run:
            key = None
            mouse = False
            dt = time.perf_counter() - self.current_time
            print(self.clock.get_fps())
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
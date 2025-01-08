import pygame as pg
from settings import *
import utils
import entity
import time
from resource_loader import *
import threading
import time
import random

pg.init()

class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((screenx, screeny))
        self.clock = pg.time.Clock()
        self.offset_x = -screenx//2
        self.offset_y = -screeny//2
        self.run = True
        self.player = entity.Player("Player", 200, 0, 0, self.offset_x, self.offset_y)
        self.current_time = time.perf_counter()
        self.map = None
        self.map_offsetx = (player_starting[0]-1)*width
        self.map_offsety = (player_starting[1]-1)*height
        self.projectiles = []
        self.enemies = []

        self.loaded = False
        self.start = False
        self.menu_option = 0
        self.player_inventory = {}
        self.player_coins = 100 


    def random_spawn_enemy(self):
        a = random.randint(0, 300)
        if a == 50 and len(self.enemies) < 10:
            x = random.randint(int(self.player.x-1000), int(self.player.x+1000))
            y = random.randint(int(self.player.y-1000), int(self.player.y+1000))
            if utils.distant_from_player(x, y, self.player.x, self.player.y) > 500:
                self.enemies.append(entity.Enemy("Enemy", 100, x, y, self.offset_x, self.offset_y))

    def load_game(self):
        load_data()
        self.map = utils.map_reader("resource/map.csv")
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
        
        self.player.move(x, y)
        self.update_global_xy()

    def handle_games(self, dt, key, mouse):
        self.controller_handle(dt, key, mouse)
        self.random_spawn_enemy()
        self.player.process(dt)
        for p in self.projectiles:
            p.move(dt)

        for e in self.enemies:
            e.process(dt)
            if utils.distant_from_player(e.x, e.y, self.player.x, self.player.y) < 400:
                e.move((self.player.x - e.x) * dt, (self.player.y - e.y) * dt)
            for p in self.projectiles:
                if e.rect.colliderect(pg.Rect(p.x-self.offset_x-5, p.y-self.offset_y-5, 10, 10)):
                    e.hp -= 10
                    self.projectiles.remove(p)

            if e.rect.colliderect(self.player.rect):
                self.player.take_damage(10)
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
        self.screen.fill(BLACK)
        font_title = pg.font.Font(None, 60)
        font_options = pg.font.Font(None, 40)

    
        title_surface = font_title.render("RPG Game", True, WHITE)
        title_rect = title_surface.get_rect(center=(screenx // 2, screeny // 4))
        self.screen.blit(title_surface, title_rect)

    
        options = ["Start Game", "Help","Shop","Inventory","Quit"]
        for i, option in enumerate(options):
            color = WHITE if i == self.menu_option else GREY
            option_surface = font_options.render(option, True, color)
            option_rect = option_surface.get_rect(center=(screenx // 2, screeny // 2 + i * 50))
            self.screen.blit(option_surface, option_rect)

        pg.display.flip()

    
        if key == pg.K_UP:
           self.menu_option = (self.menu_option - 1) % len(options)  
        elif key == pg.K_DOWN:
           self.menu_option = (self.menu_option + 1) % len(options)  
        elif key == pg.K_RETURN: 
            if self.menu_option == 0:  
               self.start = True
            elif self.menu_option == 1:  
               self.show_help()
            elif self.menu_option == 2:  
               self.show_shop()
            elif self.menu_option == 3:
                self.show_inventory()
            elif self.menu_option == 4:
                self.run = False
    def show_shop(self):
        showing_shop = True
        font = pg.font.Font(None, 40)

        shop_items = [
            {"name": "Health Position", "price": 10},
            {"name": "Mana Position" , "price": 15},
            {"name": "Sword Upgrade", "price": 50},
        ]

        while showing_shop:
            self.screen.fill(BLACK)

            title_surface = font.render("===Shop===", True, WHITE)
            title_rect = title_surface.get_rect(center=(screenx //2, screeny//6))
            self.screen.blit(title_surface, title_rect)

            for i, item in enumerate(shop_items):
                color = WHITE if i == self.menu_option else GREY
                item_surface = font.render(f"{item['name']} - {item['price']} coins", True, color)
                item_rect = item_surface.get_rect(center=(screenx // 2, screeny // 3 + i * 50))
                self.screen.blit(item_surface, item_rect)

            coins_surface = font.render(f"Coins: {self.player_coins}", True, WHITE)
            coins_rect = coins_surface.get_rect(center=(screenx // 2, screeny - 50))
            self.screen.blit(coins_surface, coins_rect)

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                    showing_shop = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.menu_option = (self.menu_option - 1) % len(shop_items)
                    elif event.key == pg.K_DOWN:
                        self.menu_option = (self.menu_option + 1) % len(shop_items)
                    elif event.key == pg.K_RETURN:
                        selected_item = shop_items[self.menu_option]
                        if self.player_coins >= selected_item["price"]:
                            self.player_coins -= selected_item["price"]
                        
                        item_name = selected_item["name"]
                        if item_name in self.player_inventory:
                            self.player_inventory[item_name] += 1
                        else:
                            self.player_inventory[item_name] = 1
                        print(f"Bought {item_name}! Inventory: {self.player_inventory}")
                    else:
                        print("Not enough coins!")
                elif event.key == pg.K_ESCAPE:
                    showing_shop = False

    def show_inventory(self):
        showing_inventory = True
        font = pg.font.Font(None, 40)

        while showing_inventory:
            self.screen.fill(BLACK)

        
            title_surface = font.render("=== Inventory ===", True, WHITE)
            title_rect = title_surface.get_rect(center=(screenx // 2, screeny // 6))
            self.screen.blit(title_surface, title_rect)

        
            for i, (item_name, count) in enumerate(self.player_inventory.items()):
               item_surface = font.render(f"{item_name}: {count}", True, WHITE)
               item_rect = item_surface.get_rect(center=(screenx // 2, screeny // 3 + i * 40))
               self.screen.blit(item_surface, item_rect)

            pg.display.flip()

        
            for event in pg.event.get():
                if event.type == pg.QUIT:
                   self.run = False
                   showing_inventory = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:  
                       showing_inventory = False

                            
    def show_help(self):
        showing_help = True
        font = pg.font.Font(None, 40)
        lines = [
        "=== Help ===",
        "Use W, A, S, D to move the player.",
        "Use the mouse to aim and left-click to shoot.",
        "Press ENTER to return to the main menu.",
        ]
        while showing_help:
            self.screen.fill(BLACK)
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, WHITE)
                text_rect = text_surface.get_rect(center=(screenx // 2, screeny // 3 + i * 40))
                self.screen.blit(text_surface, text_rect)
            pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                   self.run = False
                   showing_help = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        showing_help = False

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
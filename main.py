import pygame as pg
from settings import *
import utils
import entity
import time
from resource_loader import *
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (169, 169, 169)
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
        self.menu_option = 0
        self.player_inventory = {}
        self.player_coins = 100 

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
from email.mime import image
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
pg.mixer.init()

class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((screenx, screeny))
        self.clock = pg.time.Clock()
        self.offset_x = -screenx//2
        self.offset_y = -screeny//2
        self.run = True
        self.current_time = time.perf_counter()
        self.map = None
        self.map2 = None
        self.map_offsetx = (player_starting[0]-1)*width
        self.map_offsety = (player_starting[1]-1)*height
        self.projectiles = []
        self.enemies = []
        self.progress = 0
        self.damage = 10
        
        self.image = pg.image.load("resource/img/background.png").convert_alpha()

        self.gun = None
        self.quest_npc = entity.Passive("John", 100, 10, 20, self.offset_x, self.offset_y, None, 50, 108)

        self.loaded = False
        self.start = False
        self.menu_option = 0
        self.current_screen = 0
        self.player_inventory = {}
        self.player_coins = 10 
        self.soundtracks = []
        self.volume = 0.5

    def play_background_music(self):
        pg.mixer.music.load(background_music)
        pg.mixer.music.set_volume(self.volume)
        pg.mixer.music.play(-1, 0.0)  

    def play_sound_effect(self, sound_file):
        sound = pg.mixer.Sound(sound_file)
        sound.set_volume(self.volume)
        sound.play()
       
    def random_spawn_enemy(self):
        a = random.randint(0, 300)
        if a == 50 and len(self.enemies) < 10:
            x = random.randint(int(self.player.x-1000), int(self.player.x+1000))
            y = random.randint(int(self.player.y-1000), int(self.player.y+1000))
            if utils.distant_from_player(x, y, self.player.x, self.player.y) > 500:
                self.enemies.append(entity.Enemy("Enemy", 100, x, y, self.offset_x, self.offset_y, self.enemy_sprite, 50, 50))
                # self.play_sound_effect(enemy_spawn_music)

    def load_game(self):
        load_data()
        self.progress = 30
        self.map = utils.map_reader("resource/map.csv")
        self.map2 = utils.block_reader("resource/map2.csv")
        self.image_game_over = pg.image.load("resource/img/death.jpg").convert_alpha()
        self.progress = 60
        self.player_sprite = load_player()
        self.enemy_sprite = load_enemy()
        self.player = entity.Player("Player", 200, 0, 0, self.offset_x, self.offset_y, self.player_sprite, 50, 108)
        self.gun = gun_map.get(1)
        self.progress = 100
        self.play_background_music() 

    def controller_handle(self, dt, key, mouse):
        mx, my = pg.mouse.get_pos()
        x, y = 0, 0
        if mouse:
            self.projectiles.append(entity.Bullets(self.player.x, self.player.y, utils.find_bullet_vector(self.player.x, self.player.y, mx+self.offset_x, my+self.offset_y)))
        press = pg.key.get_pressed()
        if press[pg.K_w]:
            y -= player_speed
        if press[pg.K_s]:
            y += player_speed
        if press[pg.K_a]:
            x -= player_speed
        if press[pg.K_d]:
            x += player_speed
    
        self.player.move(x, y, dt)
        self.update_global_xy()

    def handle_games(self, dt, key, mouse):
        self.player.check_rect_collide_block(self.map2)
        self.controller_handle(dt, key, mouse)
        self.random_spawn_enemy()
        self.player.process(dt)

        for p in self.projectiles:
            p.move(dt)
            if utils.distant_from_player(p.x, p.y, self.player.x, self.player.y) > 1000:
                self.projectiles.remove(p)

        if utils.distant_from_player(self.quest_npc.x, self.quest_npc.y, self.player.x, self.player.y) < 200:
            self.quest_npc.draw_speech(self.screen, "Hello, I am John. I have a quest for.")
            if key == pg.K_e:
                self.quest_npc.draw_speech(self.screen, "Thank you for accepting the quest.")

        for e in self.enemies:
            e.process(dt)
            if utils.distant_from_player(e.x, e.y, self.player.x, self.player.y) < 400:
                e.move(min((self.player.x - e.x), e_speed), min((self.player.y - e.y), e_speed), dt)
            elif utils.distant_from_player(e.x, e.y, self.player.x, self.player.y) > 1500:
                self.enemies.remove(e)
            for p in self.projectiles:
                if e.rect.colliderect(pg.Rect(p.x-self.offset_x-5, p.y-self.offset_y-5, 10, 10)):
                    e.hp -= self.damage
                    self.projectiles.remove(p)
                    i = random.randint(1, 2)
                    self.play_sound_effect(f"resource/sounds/enemy{i}_hit.mp3")
            
            e.check_rect_collide_block(self.map2)

            if e.rect.colliderect(self.player.rect):
                self.player.take_damage(20)
            if e.hp <= 0:
                self.player_coins += 1
                self.enemies.remove(e)

        if self.player.hp <= 0:
            self.play_sound_effect(death_music)
            self.play_sound_effect(blood_splatter)
            self.play_sound_effect(game_over_music)
            self.run_death_menu()

    def run_death_menu(self):
        pg.mixer.music.pause()
        font = pg.font.Font("resource/font/LilitaOne-Regular.ttf", 50)

        options = ["Restart Game", "Quit"]
        option_positions = [
            (self.screen.get_width() // 2, 300),  
            (self.screen.get_width() // 2, 400),  
        ]
        selected_index = 0 

        while True:
            self.screen.blit(self.image_game_over, (0, 0))
            mouse_x, mouse_y = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:  
                        selected_index = (selected_index - 1) % len(options)
                    elif event.key == pg.K_DOWN:  
                        selected_index = (selected_index + 1) % len(options)
                    elif event.key == pg.K_RETURN: 
                        if selected_index == 0:
                            self.restart_game()
                            pg.mixer.music.unpause()
                            return
                        elif selected_index == 1:
                            pg.quit()
                            exit()
                elif event.type == pg.MOUSEBUTTONDOWN:  
                    for i, (x, y) in enumerate(option_positions):
                        text_width = font.size(options[i])[0]
                        text_height = font.size(options[i])[1]
                        if x - text_width // 2 <= mouse_x <= x + text_width // 2 and \
                            y - text_height // 2 <= mouse_y <= y + text_height // 2:
                            if i == 0:  
                                self.restart_game()
                                pg.mixer.music.unpause()
                                return
                            elif i == 1:  
                                pg.quit()
                                exit()

            for i, (x, y) in enumerate(option_positions):
                text_color = RED if (
                    x - font.size(options[i])[0] // 2 <= mouse_x <= x + font.size(options[i])[0] // 2 and
                    y - font.size(options[i])[1] // 2 <= mouse_y <= y + font.size(options[i])[1] // 2
                ) or i == selected_index else WHITE

                option_text = font.render(options[i], True, text_color)
                self.screen.blit(option_text, (x - option_text.get_width() // 2, y - option_text.get_height() // 2))

            death_text = font.render("Game Over", True, WHITE)
            self.screen.blit(death_text, (self.screen.get_width() // 2 - death_text.get_width() // 2, 150))

            pg.display.flip()
            pg.time.delay(100)

    def restart_game(self):
        self.player.hp = self.player.max_hp  
        self.enemies.clear()  
        self.projectiles.clear() 
        self.player.x, self.player.y = 0, 0  
        self.offset_x = -screenx // 2
        self.offset_y = -screeny // 2

        self.random_spawn_enemy()
        
    def update_global_xy(self): 
        self.offset_x = self.player.x - screenx//2
        self.offset_y = self.player.y - screeny//2

    def layer2_builder(self):
        start_y = int(self.player.y // height + player_starting[1] - 13)
        end_y = int(self.player.y // height + player_starting[1] + 13)
        start_x = int(self.player.x // width + player_starting[0] - 13)
        end_x = int(self.player.x // width + player_starting[0] + 13)

        offset_x = self.offset_x + self.map_offsetx
        offset_y = self.offset_y + self.map_offsety
        half_width = width // 2
        half_height = height // 2

        for i in range(start_y, end_y):
            if 0 <= i < len(self.map2):
                for j in range(start_x, end_x):
                    if 0 <= j < len(self.map2[i]) and self.map2[i][j] != 0:
                        self.map2[i][j].update_rect(j * width - half_width - offset_x, i * height - half_height - offset_y)
                        block = self.map2[i][j].sprite
                        
                        if block:
                            self.screen.blit(block, (j * width - half_width - offset_x, i * height - half_height - offset_y))

    def draw(self):
        mx, my = pg.mouse.get_pos()
        self.screen.fill(BLACK)
        self.screen.blit(self.map, (-self.map_offsetx-self.offset_x-width//2, -self.map_offsety-self.offset_y-height//2))
        self.layer2_builder()
        self.player.draw(self.screen, self.offset_x, self.offset_y)
        self.quest_npc.draw(self.screen, self.offset_x, self.offset_y)
        if utils.distant_from_player(self.quest_npc.x, self.quest_npc.y, self.player.x, self.player.y) < 200:
            self.quest_npc.draw_speech(self.screen, "Hello, I am John. I have a quest for you.")

        for e in self.enemies:
            e.draw(self.screen, self.offset_x, self.offset_y)

        for p in self.projectiles:
            p.draw(self.screen, self.offset_x, self.offset_y)

        gun_angle = utils.find_gun_angle((1, 0), (mx-screenx//2, my-screeny//2))
        utils.blitRotate(self.screen, self.gun, (screenx//2, screeny//2), (-30, 0), gun_angle)

        pg.draw.rect(self.screen, WHITE, (blood_x, blood_y, blood_bar_width, blood_bar_height), border_radius=border_radius)

        blood_fill_width = blood_bar_width * (self.player.hp / self.player.max_hp)
        pg.draw.rect(
            self.screen, 
            RED, 
            (blood_x + 2, blood_y + 2, blood_fill_width - 4, blood_bar_height - 4), 
            border_radius=border_radius - 2 
        )
        
        pg.draw.circle(self.screen, WHITE, (blood_x, blood_y + blood_bar_height // 2), circle_radius)

        self.screen.blit(heart_image, (blood_x - circle_radius, blood_y + blood_bar_height // 2 - circle_radius))

        self.screen.blit(coin_image, (coin_x, coin_y))

        font = pg.font.Font("resource/font/LilitaOne-Regular.ttf", 30)
        coin_count_text = font.render(str(self.player_coins), True, WHITE)
        self.screen.blit(coin_count_text, (coin_x + coin_icon_size + 10, coin_y - 2))
    
        pg.display.flip()

    def menu(self, key, mouse):
        self.screen.blit(self.image, (0, 0))
        if not self.loaded:
            font = pg.font.Font("resource/font/LilitaOne-Regular.ttf", 40)
            loading_text = font.render("Loading...", True, WHITE)
            text_rect = loading_text.get_rect(center=(screenx // 2, screeny // 2 - 50))
            self.screen.blit(loading_text, text_rect)
            
            bar_width = 400
            bar_height = 40
            border_thickness = 4
            border_radius = 10
            bar_x = (screenx - bar_width) // 2
            bar_y = (screeny - bar_height) // 2 + 50

            pg.draw.rect(self.screen, WHITE, 
                 (bar_x - border_thickness, bar_y - border_thickness, 
                  bar_width + border_thickness * 2, bar_height + border_thickness * 2), 
                 border_radius=border_radius)

            pg.draw.rect(self.screen, Light_Blue, 
                 (bar_x, bar_y, bar_width, bar_height), 
                 border_radius=border_radius)

            pg.draw.rect(self.screen, WHITE, 
                 (bar_x, bar_y, bar_width * (self.progress / 100), bar_height), 
                 border_radius=border_radius)

            if self.progress == 100:
                if mouse or key == pg.K_RETURN:
                    self.loaded = True

        else:
            if self.current_screen == 0:
                font_title = pg.font.Font("resource/font/LilitaOne-Regular.ttf", 100)
                font_options = pg.font.Font("resource/font/LilitaOne-Regular.ttf", 40)

                title_surface = font_title.render("RPG Game", True, WHITE)
                title_rect = title_surface.get_rect(center=(screenx // 2, screeny // 2.7))
                self.screen.blit(title_surface, title_rect)

                options = ["Start Game", "Help","Setting","Quit"]
                option_rects = []

                for i, option in enumerate(options):
                    color = Light_Blue if i == self.menu_option else WHITE
                    option_surface = font_options.render(option, True, color)
                    option_rect = option_surface.get_rect(center=(screenx // 2, screeny // 2 + i * 70))
                    self.screen.blit(option_surface, option_rect)
                    option_rects.append(option_rect)     

                mouse_pos = pg.mouse.get_pos()  
                mouse_clicked = pg.mouse.get_pressed()[0]  

                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_pos):  
                        self.menu_option = i 
                        if mouse_clicked:  
                            if self.menu_option == 0:
                                self.start = True
                            elif self.menu_option == 1:
                                self.current_screen = 1
                            elif self.menu_option == 2:
                                self.current_screen = 2
                            elif self.menu_option == 3:
                                self.run = False

                if key == pg.K_UP:
                    self.menu_option = (self.menu_option - 1) % len(options)
                elif key == pg.K_DOWN:
                    self.menu_option = (self.menu_option + 1) % len(options)
                elif key == pg.K_RETURN:
                    if self.menu_option == 0:
                        self.start = True  
                    elif self.menu_option == 1:
                        self.current_screen = 1
                    elif self.menu_option == 2:
                        self.current_screen = 2
                    elif self.menu_option == 3:
                        self.run = False

            elif self.current_screen == 1:
                self.show_help(key)
            elif self.current_screen == 2:
                self.show_settings(key)

        pg.display.flip()

    def show_settings(self, key):
        font = pg.font.Font(None, 40)
        lines = [
            "=== Settings ===",
            f"Volume: {int(self.volume * 100)}%",
            "Use Arrow Keys to Adjust Volume",
            "Press ENTER to Return",
        ]
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screenx // 2, screeny // 3 + i * 40))
            self.screen.blit(text_surface, text_rect)

        if key == pg.K_LEFT:
            self.volume = max(0, self.volume - 0.05)
            pg.mixer.music.set_volume(self.volume)
        elif key == pg.K_RIGHT:
            self.volume = min(1, self.volume + 0.05)
            pg.mixer.music.set_volume(self.volume)
        elif key == pg.K_RETURN:
            self.current_screen = 0  # Return to main menu

        pg.display.flip()

    def show_shop(self):
        pass

    def show_inventory(self):
        pass

    def show_settings(self, key):
        if key == pg.K_ESCAPE:
            self.current_screen = 0
        pg.display.flip()
                            
    def show_help(self, key):
        font = pg.font.Font(None, 40)
        lines = [
        "=== Help ===",
        "Use W, A, S, D to move the player.",
        "Use the mouse to aim and left-click to shoot.",
        "Press ENTER to return to the main menu.",
        ]
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(screenx // 2, screeny // 3 + i * 40))
            self.screen.blit(text_surface, text_rect)
        if key == pg.K_ESCAPE:
            self.current_screen = 0
        pg.display.flip()

    def mainloop(self):
        loader = threading.Thread(target=self.load_game)
        loader.daemon = True
        loader.start() #nis ban mok pi na
        while self.run:
            key = None
            mouse = False
            dt = time.perf_counter() - self.current_time
            # print(self.clock.get_fps())
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
                self.menu(key, mouse)
                continue

            self.handle_games(dt, key, mouse)
            self.draw()
            
def main():
    game = Game()
    game.mainloop()
    pg.quit()

if __name__ == "__main__":
    main()
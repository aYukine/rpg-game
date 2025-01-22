import pygame as pg

# tiles
tiles_decoder = {}
block_decoder = {}
gun_map = {}

circle_radius = 15 
heart_image = pg.image.load('resource/img/heart.png')
heart_image = pg.transform.scale(heart_image, (circle_radius * 2, circle_radius * 2))

coin_icon_size = 30
coin_image = pg.image.load('resource/img/coin.png')
coin_image = pg.transform.scale(coin_image, (coin_icon_size, coin_icon_size))

pg.mixer.init()
background_music = "resource/sounds/background.mp3"
death_music = "resource/sounds/player_death.mp3"
enemy_spawn_music = "resource/sounds/enemy_spawn.mp3"
game_over_music = "resource/sounds/game_over.mp3"
blood_splatter = "resource/sounds/blood_splatter.mp3"

def load_data():
    grass = pg.image.load("resource/tiles/grass.png").convert_alpha()
    stone = pg.image.load("resource/tiles/stone.png").convert_alpha()
    grasstone1 = pg.image.load("resource/tiles/grassstone1.png").convert_alpha()
    grasstone2 = pg.image.load("resource/tiles/grassstone2.png").convert_alpha()
    grasstone3 = pg.image.load("resource/tiles/grassstone3.png").convert_alpha()
    grasstone4 = pg.image.load("resource/tiles/grassstone4.png").convert_alpha()
    grasstone5 = pg.image.load("resource/tiles/grassstone5.png").convert_alpha()
    grasstone6 = pg.image.load("resource/tiles/grassstone6.png").convert_alpha()
    grassstone7 = pg.image.load("resource/tiles/grassstone7.png").convert_alpha()
    grassstone8 = pg.image.load("resource/tiles/grassstone8.png").convert_alpha()

    water = pg.image.load("resource/tiles/water.png").convert_alpha()
    watergrass1 = pg.image.load("resource/tiles/watergrass1.png").convert_alpha()
    watergrass2 = pg.image.load("resource/tiles/watergrass2.png").convert_alpha()
    watergrass3 = pg.image.load("resource/tiles/watergrass3.png").convert_alpha()
    watergrass4 = pg.image.load("resource/tiles/watergrass4.png").convert_alpha()
    watergrass5 = pg.image.load("resource/tiles/watergrass5.png").convert_alpha()
    watergrass6 = pg.image.load("resource/tiles/watergrass6.png").convert_alpha()
    watergrass7 = pg.image.load("resource/tiles/watergrass7.png").convert_alpha()
    watergrass8 = pg.image.load("resource/tiles/watergrass8.png").convert_alpha()

    tiles_decoder[1] = grass
    tiles_decoder[2] = stone
    tiles_decoder[3] = grasstone1
    tiles_decoder[4] = grasstone2
    tiles_decoder[5] = grasstone3
    tiles_decoder[6] = grasstone4
    tiles_decoder[7] = grasstone5
    tiles_decoder[8] = grasstone6
    tiles_decoder[9] = grassstone7
    tiles_decoder[10] = grassstone8

    block_decoder[4] = water
    block_decoder[5] = watergrass1
    block_decoder[6] = watergrass2
    block_decoder[7] = watergrass3
    block_decoder[8] = watergrass4
    block_decoder[9] = watergrass5
    block_decoder[10] = watergrass6
    block_decoder[11] = watergrass7
    block_decoder[12] = watergrass8

    wall = pg.image.load("resource/blocks/wall.png").convert_alpha()
    tree1 = pg.image.load("resource/blocks/tree1.png").convert_alpha()
    tree2 = pg.image.load("resource/blocks/tree2.png").convert_alpha()

    block_decoder[1] = wall
    block_decoder[2] = tree1
    block_decoder[3] = tree2

    gun1 = pg.image.load("resource/gun/gun1.png").convert_alpha()
    gun_map[1] = gun1

def load_player():
    player = []
    for i in range(12):
        player.append(pg.image.load("resource/player/sprite_"+str(i)+".png").convert_alpha())
    return player

def load_enemy():
    enemy = []
    for i in range(12):
        enemy.append(pg.image.load("resource/enemy/sprite_"+str(i)+".png").convert_alpha())
    return enemy

def load_sound():
    pass
    # sounds  = []
    # sounds.append(pg.mixer.Sound("resource/sound/shot.wav"))
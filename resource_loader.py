import pygame as pg

# tiles

block_decoder = {}


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

    block_decoder[1] = grass
    block_decoder[2] = stone
    block_decoder[3] = grasstone1
    block_decoder[4] = grasstone2
    block_decoder[5] = grasstone3
    block_decoder[6] = grasstone4
    block_decoder[7] = grasstone5
    block_decoder[8] = grasstone6
    block_decoder[9] = grassstone7
    block_decoder[10] = grassstone8

    block_decoder[11] = water
    block_decoder[12] = watergrass1
    block_decoder[13] = watergrass2
    block_decoder[14] = watergrass3
    block_decoder[15] = watergrass4
    block_decoder[16] = watergrass5
    block_decoder[17] = watergrass6
    block_decoder[18] = watergrass7
    block_decoder[19] = watergrass8
import pygame as pg

# tiles
grass = pg.image.load("resource/tiles/grass.png")
stone = pg.image.load("resource/tiles/stone.png")


block_decoder = {1:grass, 2:stone}


def convert_images():
    global grass, stone
    grass = grass.convert_alpha()
    stone = stone.convert_alpha()
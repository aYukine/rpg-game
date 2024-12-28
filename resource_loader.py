import pygame as pg

# tiles

block_decoder = {}


def load_data():
    grass = pg.image.load("resource/tiles/grass.png")
    stone = pg.image.load("resource/tiles/stone.png")
    
    block_decoder[1] = grass
    block_decoder[2] = stone
    
    grass = grass.convert()
    stone = stone.convert()
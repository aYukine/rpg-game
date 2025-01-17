import pygame
import csv
from resource_loader import tiles_decoder, block_decoder
from entity import Block

def write(master, color, text, x, y, pos, size=10):
    font = pygame.font.Font(None, size)
    if pos == "TOPLEFT":
        master.blit(font.render(str(text), True, color), (x, y))
    if pos == "MIDDLE":
        width, height = font.size(text)
        master.blit(font.render(str(text), True, color), (x-(width/2), y-(height/2)))

def block_reader(filename):
    block_tiles = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            new_row = []
            for cell in row:
                if cell != '0':
                    block_img = block_decoder.get(int(cell))
                    block = Block(block_img)
                    new_row.append(block)
                else:
                    new_row.append(0)

            block_tiles.append(new_row)

    return block_tiles

def map_reader(filename):
    map_tiles = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            map_tiles.append([int(cell) for cell in row])
    rows = len(map_tiles)
    cols = len(map_tiles[0]) if rows else 0
    tile_width = tile_height = 50
    map_surface = pygame.Surface((cols * tile_width, rows * tile_height)).convert()

    for i, row in enumerate(map_tiles):
        for j, cell in enumerate(row):
            
            block = tiles_decoder.get(cell)
            if block:
                map_surface.blit(block, (j * tile_width, i * tile_height))

    return map_surface

def new_map_reader(filename):
    pass

def find_bullet_vector(px, py, mx, my):
    dx = mx - px
    dy = my - py
    distance = (dx**2 + dy**2)**0.5
    return (dx/distance, dy/distance)

def distant_from_player(x, y, px, py):
    return ((x-px)**2 + (y-py)**2)**0.5
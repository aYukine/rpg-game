import pygame
import csv
from resource_loader import block_decoder

def write(master, color, text, x, y, pos, size):
    font = pygame.font.Font(None, size)
    if pos == "TOPLEFT":
        master.blit(font.render(str(text), True, color), (x, y))
    if pos == "MIDDLE":
        width, height = font.size(text)
        master.blit(font.render(str(text), True, color), (x-(width/2), y-(height/2)))

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
            
            block = block_decoder.get(cell)
            if block:
                map_surface.blit(block, (j * tile_width, i * tile_height))

    return map_surface

def find_bullet_vector(px, py, mx, my):
    dx = mx - px
    dy = my - py
    distance = (dx**2 + dy**2)**0.5
    return (dx/distance, dy/distance)

def distant_from_player(x, y, px, py):
    return ((x-px)**2 + (y-py)**2)**0.5
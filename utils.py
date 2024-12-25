import pygame
import csv

def write(master, color, text, x, y, pos, size):
    font = pygame.font.Font(None, size)
    if pos == "TOPLEFT":
        master.blit(font.render(str(text), True, color), (x, y))
    if pos == "MIDDLE":
        width, height = font.size(text)
        master.blit(font.render(str(text), True, color), (x-(width/2), y-(height/2)))

def map_reader(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        map = []
        for row in reader:
            map.append([int(cell) for cell in row])
    return map

def find_bullet_vector(px, py, mx, my):
    dx = mx - px
    dy = my - py
    distance = (dx**2 + dy**2)**0.5
    return (dx/distance, dy/distance)

def distant_from_player(x, y, px, py):
    return ((x-px)**2 + (y-py)**2)**0.5
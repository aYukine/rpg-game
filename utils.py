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

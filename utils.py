import pygame
import csv
from resource_loader import tiles_decoder, block_decoder
from entity import Block
import math

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

def new_map_reader(filename, map_size=480,chunk_tile_size=24, tile_size=20):
    
    map_tiles = []
    with open(filename, "r") as f:
        for line in f:
            row = [int(cell) for cell in line.split()]
            map_tiles.append(row)

    rows = len(map_tiles)
    cols = len(map_tiles[0]) if rows else 0

    # Total number of chunks in the map
    num_chunks_x = map_size // (chunk_tile_size * tile_size)  # Number of chunks horizontally
    num_chunks_y = map_size // (chunk_tile_size * tile_size)  # Number of chunks vertically

    chunk_pixel_size = chunk_tile_size * tile_size  # Each chunk's size in pixels (e.g., 480x480)

    chunks = []

    # Process the map into chunks
    for chunk_row in range(num_chunks_y):
        for chunk_col in range(num_chunks_x):
            # Create a surface for the chunk
            chunk_surface = pygame.Surface((chunk_pixel_size, chunk_pixel_size)).convert_alpha()
            chunk_surface.fill((0, 0, 0, 0))  # Transparent background

            # Draw tiles onto the chunk surface
            for i in range(chunk_tile_size):
                for j in range(chunk_tile_size):
                    tile_row = chunk_row * chunk_tile_size + i
                    tile_col = chunk_col * chunk_tile_size + j

                    # Check if the tile is within map bounds
                    if tile_row < rows and tile_col < cols:
                        tile_id = map_tiles[tile_row][tile_col]
                        tile_image = block_decoder.get(tile_id)

                        if tile_image:
                            x = j * tile_size
                            y = i * tile_size
                            chunk_surface.blit(tile_image, (x, y))

            # Add the chunk surface to the list
            chunks.append(chunk_surface)

    return chunks

def find_bullet_vector(px, py, mx, my):
    dx = mx - px
    dy = my - py
    distance = (dx**2 + dy**2)**0.5
    return (dx/distance, dy/distance)

def distant_from_player(x, y, px, py):
    return ((x-px)**2 + (y-py)**2)**0.5

def blitRotate(surf, image, origin, pivot, angle):
    image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


def find_gun_angle(v1, v2):
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)

    if magnitude_v1 == 0 or magnitude_v2 == 0:
        raise ValueError("One of the vectors has zero magnitude, angle is undefined.")

    cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
    cos_theta = max(-1, min(1, cos_theta))
    
    angle_radians = math.acos(cos_theta)

    angle_degrees = math.degrees(angle_radians)

    cross_product = v1[0] * v2[1] - v1[1] * v2[0]

    if cross_product > 0:
        angle_degrees = 360 - angle_degrees

    return angle_degrees

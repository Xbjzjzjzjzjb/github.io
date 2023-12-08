import pygame
import random
import numpy as np
from opensimplex import OpenSimplex

# Initialize Pygame 
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200 
SCREEN_HEIGHT = 900

# Tile size
TILE_SIZE = 32

# Map dimensions
MAP_WIDTH = 200
MAP_HEIGHT = 200

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load images 
base_img = pygame.image.load('p.png').convert_alpha()
grass_img = pygame.image.load('g.png').convert_alpha()
water_img = pygame.image.load('w.png').convert_alpha()
mountain_img = pygame.image.load('m.png').convert_alpha()  
tree_img = pygame.image.load('t.png').convert_alpha()
empty_img = pygame.image.load('p.png').convert_alpha()
empty_img = pygame.transform.scale(empty_img, (TILE_SIZE, TILE_SIZE))
hill_img = pygame.image.load('h.png').convert_alpha()
hill_img = pygame.transform.scale(hill_img, (TILE_SIZE, TILE_SIZE))

# Scale tile images
grass_img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
water_img = pygame.transform.scale(water_img, (TILE_SIZE, TILE_SIZE))
mountain_img = pygame.transform.scale(mountain_img, (TILE_SIZE, TILE_SIZE))
tree_img = pygame.transform.scale(tree_img, (TILE_SIZE, TILE_SIZE))
desert_img = pygame.image.load('d.png').convert_alpha()
desert_img = pygame.transform.scale(desert_img, (TILE_SIZE, TILE_SIZE))
snow_img = pygame.image.load('s.png').convert_alpha()
snow_mountain_img = pygame.image.load('sm.png').convert_alpha()
snow_img = pygame.transform.scale(snow_img, (TILE_SIZE, TILE_SIZE))
snow_mountain_img = pygame.transform.scale(snow_mountain_img, (TILE_SIZE, TILE_SIZE))
snow_tree_img = pygame.image.load('st.png').convert_alpha()
snow_tree_img = pygame.transform.scale(snow_tree_img, (TILE_SIZE, TILE_SIZE))
snow_hill_img = pygame.image.load('sh.png').convert_alpha()
snow_hill_img = pygame.transform.scale(snow_hill_img, (TILE_SIZE, TILE_SIZE))

# Create empty tile map
world_map = [[empty_img for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]  

# Create simplex noise generator
gen = OpenSimplex(random.randint(0, 1000000))

# Generate desert locations
desert_size = 30  # Size of the desert seed
desert_count = 10  # Number of desert seeds
desert_locations = [(random.randint(0, MAP_WIDTH-desert_size), random.randint(MAP_HEIGHT//4, MAP_HEIGHT-desert_size)) for _ in range(desert_count)]  # Random locations not in snow region
desert_gen = OpenSimplex(random.randint(0, 1000000))  # Another noise generator for desert shapes

for row in range(MAP_HEIGHT):
    for col in range(MAP_WIDTH):
        # Use noise to get value
        value = (gen.noise2(col/20, row/20) + 1) / 2  

        # Check if this location is within a desert seed
        for desert_x, desert_y in desert_locations:
            if desert_x <= col < desert_x + desert_size and desert_y <= row < desert_y + desert_size:
                if (desert_gen.noise2(col/10, row/10) + 1) / 2 > 0.5:  # Use noise to decide whether this location within the seed is a desert
                    value = 0.8  # Overwrite the value so this location becomes a desert

        if row < MAP_HEIGHT / 4:  # The upper quarter of the map
            if value < 0.3:
                world_map[row][col] = snow_img
            elif value < 0.6:
                world_map[row][col] = snow_tree_img
            elif value < 0.7:
                world_map[row][col] = snow_hill_img
            else:
                world_map[row][col] = snow_mountain_img
        else:
            if value < 0.3:
                world_map[row][col] = water_img
            elif value < 0.5:
                world_map[row][col] = grass_img
            elif value < 0.6:
                world_map[row][col] = tree_img
            elif value < 0.7:
                world_map[row][col] = hill_img
            elif value < 0.8:  # Add this condition for deserts
                world_map[row][col] = desert_img
            else:
                world_map[row][col] = mountain_img

# Camera position
camera_x = MAP_WIDTH * TILE_SIZE / 2 - SCREEN_WIDTH / 2
camera_y = MAP_HEIGHT * TILE_SIZE / 2 - SCREEN_HEIGHT / 2


# Variables for mouse dragging
mouse_down = False  # Used to track whether the mouse button is being held down
last_mouse_pos = (0, 0)  # Used to track the last known mouse position

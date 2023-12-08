from settings import *

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
base_img = pygame.image.load('h.png').convert_alpha()
base_img = pygame.transform.scale(base_img, (TILE_SIZE, TILE_SIZE))
grass_img = pygame.image.load('g.png').convert_alpha()
water_img = pygame.image.load('w.png').convert_alpha()
mountain_img = pygame.image.load('m.png').convert_alpha()  
tree_img = pygame.image.load('t.png').convert_alpha()
hill_img = pygame.image.load('h.png').convert_alpha()
hill_img = pygame.transform.scale(hill_img, (TILE_SIZE, TILE_SIZE))

# Scale tile images
grass_img = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
water_img = pygame.transform.scale(water_img, (TILE_SIZE, TILE_SIZE))
mountain_img = pygame.transform.scale(mountain_img, (TILE_SIZE, TILE_SIZE))
tree_img = pygame.transform.scale(tree_img, (TILE_SIZE, TILE_SIZE))
desert_img = pygame.image.load('d.png').convert_alpha()
desert_img = pygame.transform.scale(desert_img, (TILE_SIZE, TILE_SIZE))
oasis_img = pygame.image.load('o.png').convert_alpha()
oasis_img = pygame.transform.scale(oasis_img, (TILE_SIZE, TILE_SIZE))
snow_img = pygame.image.load('s.png').convert_alpha()
snow_mountain_img = pygame.image.load('sm.png').convert_alpha()
snow_img = pygame.transform.scale(snow_img, (TILE_SIZE, TILE_SIZE))
snow_mountain_img = pygame.transform.scale(snow_mountain_img, (TILE_SIZE, TILE_SIZE))
snow_tree_img = pygame.image.load('st.png').convert_alpha()
snow_tree_img = pygame.transform.scale(snow_tree_img, (TILE_SIZE, TILE_SIZE))
snow_hill_img = pygame.image.load('sh.png').convert_alpha()
snow_hill_img = pygame.transform.scale(snow_hill_img, (TILE_SIZE, TILE_SIZE))
snow_pool_img = pygame.image.load('sp.png').convert_alpha()
snow_pool_img = pygame.transform.scale(snow_pool_img, (TILE_SIZE, TILE_SIZE))
floating_ice_img = pygame.image.load('fl.png').convert_alpha()
floating_ice_img = pygame.transform.scale(floating_ice_img, (TILE_SIZE, TILE_SIZE))
glacier_img = pygame.image.load('gl.png').convert_alpha()
glacier_img = pygame.transform.scale(glacier_img, (TILE_SIZE, TILE_SIZE))
tropical_forest_img = pygame.image.load('tf.png').convert_alpha()
tropical_forest_img = pygame.transform.scale(tropical_forest_img, (TILE_SIZE, TILE_SIZE))
tropical_hill_img = pygame.image.load('th.png').convert_alpha()
tropical_hill_img = pygame.transform.scale(tropical_hill_img, (TILE_SIZE, TILE_SIZE))
swampt_img = pygame.image.load('sw.png').convert_alpha()
swampt_img = pygame.transform.scale(swampt_img, (TILE_SIZE, TILE_SIZE))
volcano_img = pygame.image.load('v.png').convert_alpha()
volcano_img = pygame.transform.scale(volcano_img, (TILE_SIZE, TILE_SIZE))

# Create base tile map
world_map = [[base_img for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

orc_lair_img = pygame.image.load('or.png').convert_alpha()
orc_lair_img = pygame.transform.scale(orc_lair_img, (TILE_SIZE, TILE_SIZE))
# Create simplex noise generator
gen = OpenSimplex(random.randint(0, 1000000))
tree_wrap_prob = 0.5  

# Generate desert locations
desert_size = 30  # Size of the desert seed
desert_count = 10  # Number of desert seeds
desert_locations = [(random.randint(0, MAP_WIDTH-desert_size), random.randint(MAP_HEIGHT//4, MAP_HEIGHT-desert_size)) for _ in range(desert_count)]  
desert_gen = OpenSimplex(random.randint(0, 1000000))  # Another noise generator for desert shapes

world_map_terrain = [[None for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)] 
world_map_building = [[None for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)] 

height_gen = OpenSimplex(random.randint(0, 1000000))

class Orc:
    def __init__(self, x, y, hp, g, f):
        self.x = x
        self.y = y
        self.hp = hp
        self.g = g
        self.f = f

for row in range(MAP_HEIGHT):
    for col in range(MAP_WIDTH):
        height = (height_gen.noise2(col/10, row/10) + 1) / 2 
        value = (gen.noise2(col/20, row/20) + 1) / 2 

        for desert_x, desert_y in desert_locations:
            if desert_x <= col < desert_x + desert_size and desert_y <= row < desert_y + desert_size:
                if (desert_gen.noise2(col/10, row/10) + 1) / 2 > 0.5:  
                    value = 0.8 

        if row < MAP_HEIGHT * 2 / 8:
            if height < 0.2:
                world_map[row][col] = snow_pool_img
                world_map_terrain[row][col] = 'snow_pool'
            elif height < 0.25:
                world_map[row][col] = floating_ice_img
                world_map_terrain[row][col] = 'floating_ice'
            elif height < 0.5:
                world_map[row][col] = snow_img
                world_map_terrain[row][col] = 'snow' 
            elif height < 0.65:
                world_map[row][col] = snow_tree_img
                world_map_terrain[row][col] = 'snow_tree'              
            elif height < 0.75:
                world_map[row][col] = snow_hill_img
                world_map_terrain[row][col] = 'snow_hill'
            elif height < 0.87:
                world_map[row][col] = snow_mountain_img
                world_map_terrain[row][col] = 'snow_mountain'
            else:                
                world_map[row][col] = glacier_img
                world_map_terrain[row][col] = 'glacier'
        elif row < MAP_HEIGHT * 7 / 8:
            if value < 0.3:
                world_map[row][col] = water_img
                world_map_terrain[row][col] = 'water'
            elif value < 0.5:
                world_map[row][col] = grass_img
                world_map_terrain[row][col] = 'grass'
            elif value < 0.6:
                world_map[row][col] = tree_img
                world_map_terrain[row][col] = 'tree'
            elif value < 0.7:
                world_map[row][col] = hill_img
                world_map_terrain[row][col] = 'hill'
            elif value < 0.8:  
                world_map[row][col] = desert_img
                world_map_terrain[row][col] = 'desert'
            else:
                world_map[row][col] = mountain_img
                world_map_terrain[row][col] = 'mountain'
        else:
            if value < 0.3:
                world_map[row][col] = water_img
                world_map_terrain[row][col] = 'water'
            elif value < 0.6: 
                world_map[row][col] = tropical_forest_img 
                world_map_terrain[row][col] = 'tropical_forest' 
            elif value < 0.75:
                world_map[row][col] = swampt_img
                world_map_terrain[row][col] = 'swampt'
            elif value < 0.85:
                world_map[row][col] = tropical_hill_img
                world_map_terrain[row][col] = 'tropical_hill'
            else:
                world_map[row][col] = mountain_img
                world_map_terrain[row][col] = 'mountain'
        
        if world_map_terrain[row][col] == 'mountain':
            if random.random() < 0.01:
                world_map[row][col] = volcano_img
                world_map_terrain[row][col] = 'volcano'
                
        if world_map_terrain[row][col] == 'desert':
            if random.random() < 0.01:
                world_map[row][col] = oasis_img
                world_map_terrain[row][col] = 'oasis' 
                
        orc_lair_locations = []  # Empty list to store coordinates of orc lair locations

        if world_map_terrain[row][col] == 'hill':
            world_map[row][col] = hill_img
            if random.random() < 0.01:
                world_map[row][col] = orc_lair_img
                world_map_building[row][col] = 'orc_lair'
                orc_lair_locations.append((row, col))  # Store the location of each orc lair
                # span 3-5  orc
                num_orcs = random.randint(3, 5) 
                orcs = []
                for i in range(num_orcs):
                    hp = random.randint(20, 25)
                    g = random.randint(10, 15)
                    f = random.randint(1, 3)
                    lair_x, lair_y = orc_lair_locations[-1][0], orc_lair_locations[-1][1]
                    orc = Orc(lair_x, lair_y, hp, g, f)
                    orcs.append(orc)

                # orc save in orc_lair_locations
                orc_lair_locations.append((row, col, orcs))

# Camera position
camera_x = MAP_WIDTH * TILE_SIZE / 2 - SCREEN_WIDTH / 2
camera_y = MAP_HEIGHT * TILE_SIZE / 2 - SCREEN_HEIGHT / 2
camera_locked_to_player = True  # Add this line

# Variables for mouse dragging
mouse_down = False  # Used to track whether the mouse button is being held down
last_mouse_pos = (0, 0)  # Used to track the last known mouse position

last_terrain = None
last_building = None
terrain_events = {
    'desert': [
        "You're in a desert, it's hot and you're thirsty.",
        "The sand stretches as far as the eye can see. The sun blazes overhead."
    ],
    'oasis': [
        "You've found an oasis! Palm trees and a clear pond invite you to rest.",
        "Relief washes over you as you spot an oasis in the midst of the desert."
    ],
    'snow': [
        "It's cold and snowing, you need to find a shelter.",
        "You are surrounded by a blanket of white. The cold is biting."
    ],
    'snow_tree': [
        "You're in a snowy forest, visibility is low.",
        "Trees heavy with snow surround you. The air is chill and quiet."
    ],
    'snow_pool': [
        "You're at a snow pool, the ice seems thin here.",
        "You've come across a frozen pool. The ice is clear and thin."
    ],
    'floating_ice': [
        "You're on floating ice, you need to be careful not to fall into the freezing water.",
        "You're treading on thin ice, literally! You need to move carefully."
    ],
    'snow_hill': [
        "You're on a snowy hill, it's cold but the view is stunning.",
        "You're standing atop a snow-covered hill, the view is breathtaking but the cold is harsh."
    ],
    'snow_mountain': [
        "You're on top of a snowy mountain, it's very cold here.",
        "You've ascended a snow-capped mountain. The air is thin and the temperature, freezing."
    ],
    'glacier': [
        "You're on a glacier, the ground is slippery.",
        "You've found yourself on a massive glacier. It's a frozen world."
    ],
    'water': [
        "You're in water, you need to swim to the shore.",
        "You're swimming in water. You must find the shore soon."
    ],
    'grass': [
        "You're on a grass field, it's peaceful here.",
        "You're standing in a green field. It's quiet and serene."
    ],
    'tree': [
        "You're in a forest, there might be animals around.",
        "You're surrounded by trees. Sounds of wildlife echo around you."
    ],
    'hill': [
        "You're on a hill, you can see your surroundings.",
        "You're atop a hill, the view of your surroundings is clear."
    ],
    'mountain': [
        "You're on top of a mountain, you feel accomplished.",
        "You've climbed a mountain. You're on top of the world."
    ],
    'volcano': [
        "The ground rumbles beneath you, you are on a volcano!",
        "You're standing on the edge of a volcanic crater, the heat is overwhelming."
    ],
    'tropical_forest': [
        "You've entered a tropical forest. The air is humid and the sounds of wildlife surround you.",
        "The lush greenery of the tropical forest engulfs you. The forest teems with life."
    ],
    'swampt': [
        "You're trudging through a swamp. The ground is soggy and the air smells of decay and life intermingling.",
        "You're navigating a swamp. Each step squishes into the wet ground and you hear the distant croaking of frogs."
    ],
    'tropical_hill': [
        "You're on a tropical hill, surrounded by lush greenery and the song of birds.",
        "Climbing a tropical hill, you can see the vibrant flora spread out below."        
    ]
}

building_events = {
  'orc_lair': [
    "You encountered orcs!",
    "Orcs jump out for an ambush!"
  ]
}
old_building_events = {
  'orc_lair': [
    "The echoes of battle still linger in the orc lair, but the once fierce enemies have been vanquished. The ground is littered with the remains of defeated orcs, a testament to your victory.",
    "As you step into the orc lair, the stench of blood and sweat fills the air. The walls are adorned with signs of a fierce struggle, but the orcs have been defeated. You have triumphed over your enemies."
  ]
}

class Player:
    def __init__(self, x, y, hp, g, f):
        self.x = x
        self.y = y
        self.hp = hp
        self.g = g
        self.f = f

    def move(self, dx, dy):
        self.x = max(0, min(MAP_WIDTH - 1, self.x + dx))
        self.y = max(0, min(MAP_HEIGHT - 1, self.y + dy))

player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2, 100, 10, 8)

def move_camera_to_player():
    global camera_x, camera_y
    camera_x = player.x * TILE_SIZE - SCREEN_WIDTH // 2
    camera_y = player.y * TILE_SIZE - SCREEN_HEIGHT // 2
    camera_x = max(0, min(camera_x, MAP_WIDTH * TILE_SIZE - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, MAP_HEIGHT * TILE_SIZE - SCREEN_HEIGHT))

# Set initial camera position
move_camera_to_player()

# Main loop
running = True
building_land = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, -1)
            elif event.key == pygame.K_DOWN:
                player.move(0, 1)
            elif event.key == pygame.K_LEFT:
                player.move(-1, 0)
            elif event.key == pygame.K_RIGHT:
                player.move(1, 0)
            camera_locked_to_player = True  # Add this line

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_down = True
                last_mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouse_down = False
                
    if camera_locked_to_player:  # Add this line
        move_camera_to_player()
    terrain = world_map_terrain[player.y][player.x]  # Change this line to use world_map_terrain
    if terrain != last_terrain:  # If the terrain has changed since last check
        if terrain in terrain_events:
            print(random.choice(terrain_events[terrain]))
        last_terrain = terrain 

    if mouse_down:
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - last_mouse_pos[0]
        dy = mouse_pos[1] - last_mouse_pos[1]
        camera_x -= dx
        camera_y -= dy
        last_mouse_pos = mouse_pos
        camera_locked_to_player = False  # Add this line

        # Ensure camera doesn't go outside the map
        camera_x = max(0, min(camera_x, MAP_WIDTH * TILE_SIZE - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, MAP_HEIGHT * TILE_SIZE - SCREEN_HEIGHT))

    building = world_map_building[player.y][player.x] 
    if building != last_building:
        if building_land == True:
            if building in building_events:
                print(random.choice(building_events[building]))
        else:
            if building in building_events:
                print(random.choice(old_building_events[building]))
        last_building = building
        
        for building in building_events:
            if building == 'orc_lair':
                if len(orcs) > 0:
                    print(f"You encountered {len(orcs)} orcs!")
                else:
                    None          
                battle_active = True 
                while battle_active:
                    for orc in orcs:
                        player.ack = (player.g - orc.f)                       
                        orc.hp -= player.ack
                        print(f"You dealt {player.ack} damage to the orc!")
                        print(f"Orc HP {orc.hp} !")
                        if orc.hp <= 0:
                            orcs.remove(orc)
                            print(f"You defeated the orc!ober{len(orcs)} orcs!")
                            if len(orcs) == 0:
                                print("You have defeated all the orcs!")
                                battle_active = False
                                break                               

                        # orc and player fight
                        orc.ack = (orc.g - player.f)
                        player.hp -= orc.ack
                        print(f"The orc dealt {orc.ack} damage to you!")
                        print(f"You HP: {player.hp}!")

                        if player.hp <= 0:
                            print("You were defeated by the orc!")
                            battle_active = False
                            break

                    if len(orcs) == 0:
                        building_land = False
                        break

    # Draw tiles
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            x = col * TILE_SIZE - camera_x
            y = row * TILE_SIZE - camera_y
            if -TILE_SIZE <= x < SCREEN_WIDTH + TILE_SIZE and -TILE_SIZE <= y < SCREEN_HEIGHT + TILE_SIZE:
                screen.blit(base_img, (x, y))             
                img = world_map[row][col]
                screen.blit(img, (x, y))

    pygame.draw.rect(screen, (0, 0, 255), (player.x * TILE_SIZE - camera_x, player.y * TILE_SIZE - camera_y, TILE_SIZE, TILE_SIZE))
    pygame.display.flip()

pygame.quit()

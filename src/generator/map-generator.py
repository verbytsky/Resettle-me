import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Tile Types and Colors
WATER = 0
GRASS = 1

tile_colors = {
    WATER: (0, 0, 255),
    GRASS: (0, 255, 0)
}


# Generate a simplified Perlin-like noise map
def generate_noise_map(width, height, seed=0):
    random.seed(seed)
    noise_map = [[0 for _ in range(height)] for _ in range(width)]

    for x in range(width):
        for y in range(height):
            noise_map[x][y] = random.uniform(0, 1)

    return noise_map


# Generate noise map with a central mainland
def generate_mainland_noise_map(width, height, seed=0):
    random.seed(seed)
    noise_map = [[0 for _ in range(height)] for _ in range(width)]
    center_x, center_y = width // 2, height // 2

    for x in range(width):
        for y in range(height):
            base_noise = random.uniform(0, 1)
            distance_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

            distance_factor = 1 - distance_to_center / (math.sqrt(center_x ** 2 + center_y ** 2))

            # Modify the noise value based on distance to center
            noise_map[x][y] = base_noise * distance_factor

    return noise_map


# Smoothing function to make landmass more contiguous
def smooth_grid(grid):
    smoothed_grid = [[WATER for _ in range(32)] for _ in range(32)]

    for x in range(32):
        for y in range(32):
            land_neighbors = 0

            # Check the six neighbors for each hexagon
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]:
                new_x, new_y = x + dx, y + dy

                if 0 <= new_x < 32 and 0 <= new_y < 32:
                    if grid[new_x][new_y] == GRASS:
                        land_neighbors += 1

            # Change tile based on neighbors
            if grid[x][y] == WATER and land_neighbors >= 4:
                smoothed_grid[x][y] = GRASS
            elif grid[x][y] == GRASS and land_neighbors <= 2:
                smoothed_grid[x][y] = WATER
            else:
                smoothed_grid[x][y] = grid[x][y]

    return smoothed_grid


# Function to draw a hexagon at a given position
def draw_hexagon(x, y, s, tile_type):
    points = []
    for angle in range(0, 360, 60):
        angle_rad = math.radians(angle)
        point = (x + s * math.cos(angle_rad), y + s * math.sin(angle_rad))
        points.append(point)
    pygame.draw.polygon(screen, tile_colors[tile_type], points)


# Create a window of 800x600
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Map Generator")

# Side length of hexagon
s = 10.83

# Distances between hexagon centers
dx = 16.24
dy = 18.75

# Initialize grid
grid = [[WATER for _ in range(32)] for _ in range(32)]

# Generate initial map
noise_map = generate_mainland_noise_map(32, 32, seed=random.randint(0, 1000))
threshold = 0.3
for x in range(32):
    for y in range(32):
        if noise_map[x][y] > threshold:
            grid[x][y] = GRASS
grid = smooth_grid(grid)


# Tile Types and Colors with new biomes
WATER = 0
GRASS = 1
MOUNTAIN = 2
SNOW = 3
FOREST = 4
DESERT = 5  # New biome

tile_colors = {
    WATER: (0, 0, 255),
    GRASS: (0, 255, 0),
    MOUNTAIN: (128, 128, 128),
    SNOW: (255, 255, 255),
    FOREST: (34, 139, 34),
    DESERT: (244, 164, 96)  # New biome color
}

# ...

# Function to add biomes and climate zones
def add_biomes(grid):
    rows, cols = len(grid), len(grid[0])
    
    # Add Snow in the far north and far south
    for x in range(rows):
        for y in [0, 1, rows - 1, rows - 2]:
            grid[x][y] = SNOW
    
    # Add Mountains, Forests, and Deserts
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == GRASS:
                # Add Forests near Grass
                if random.uniform(0, 1) < 0.2:
                    grid[x][y] = FOREST
                
                # Add Mountains in clusters
                if random.uniform(0, 1) < 0.1:
                    grid[x][y] = MOUNTAIN
                
                # Add Deserts far from water
                water_neighbors = 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < rows and 0 <= new_y < cols:
                        if grid[new_x][new_y] == WATER:
                            water_neighbors += 1
                if water_neighbors == 0 and random.uniform(0, 1) < 0.2:
                    grid[x][y] = DESERT
    
    return grid

# ...

# After generating the initial map and smoothing it
grid = add_biomes(grid)

# ...
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Re-initialize grid to water tiles
            grid = [[WATER for _ in range(32)] for _ in range(32)]

            
            # Regenerate biomes after generating the new map
            grid = add_biomes(grid)
# Regenerate map on mouse click
            noise_map = generate_mainland_noise_map(32, 32, seed=random.randint(0, 1000))
            for x in range(32):
                for y in range(32):
                    if noise_map[x][y] > threshold:
                        grid[x][y] = GRASS
            grid = smooth_grid(grid)
            grid = add_biomes(grid)

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw hexagonal grid based on tile types
    for row in range(32):
        for col in range(32):
            x = col * dx
            y = row * dy

            # Stagger odd rows
            if col % 2 == 1:
                y += dy / 2

            tile_type = grid[col][row]
            draw_hexagon(x, y, s, tile_type)

    # Update the display
    pygame.display.update()


import pygame
import math

class Settlement:
    def __init__(self, x, y, tile_type):
        self.x = x  # X-coordinate of the settlement
        self.y = y  # Y-coordinate of the settlement
        self.tile_type = tile_type  # Type of tile where the settlement is located
        self.population = 100  # Initial population
        self.growth_rate = self.calculate_growth_rate()  # Population growth rate
    
    def calculate_growth_rate(self):
        # Calculate the growth rate based on the tile type
        growth_rate_by_tile = {
            "Grass": 1.2,
            "Mountain": 0.8,
            "Snow": 0.5,
            "Forest": 1.1,
            "Desert": 0.6
        }
        return growth_rate_by_tile.get(self.tile_type, 1.0)  # Default to 1.0 if tile type is not recognized
    
    def update_population(self):
        self.population *= self.growth_rate
    
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0, 128), (self.x, self.y), math.sqrt(self.population), 2)


# Initialize an empty list to hold all the settlements
settlements = []

# Inside the main game loop, add the following code to handle mouse clicks
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        x, y = event.pos
        grid_x, grid_y = x // 20, y // 20
        tile_type = grid[grid_x][grid_y]
        
        # Create a new Settlement object and add it to the settlements list
        new_settlement = Settlement(grid_x * 20 + 10, grid_y * 20 + 10, tile_type)
        settlements.append(new_settlement)

# Update the population for each settlement and draw them
for settlement in settlements:
    settlement.update_population()
    settlement.draw(screen)

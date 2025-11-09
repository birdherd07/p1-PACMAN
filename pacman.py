import pygame
from pacman_ai import PacmanAI
from score_tracker import ScoreTracker
import sys

# Initialize Pygame
pygame.init()

# ---------- Window Configuration ----------
WIDTH, HEIGHT = 500, 500
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PACMAN - AI Agent")

# Try to load icon (if exists)
try:
    icon = pygame.image.load('PACicon.png')
    pygame.display.set_icon(icon)
except Exception:
    pass  # Icon is optional

clock = pygame.time.Clock()

# ---------- Grid / Maze Configuration ----------
CELL = 25  # Each cell is 25x25 pixels
GRID_W, GRID_H = WIDTH // CELL, HEIGHT // CELL  # 20x20 grid

# Create maze: 0=open path, 1=wall
# Start with all open, then add walls
maze = [[0 for _ in range(GRID_W)] for _ in range(GRID_H)]

# Add border walls
for x in range(GRID_W):
    maze[0][x] = 1  # Top wall
    maze[GRID_H-1][x] = 1  # Bottom wall
for y in range(GRID_H):
    maze[y][0] = 1  # Left wall
    maze[y][GRID_W-1] = 1  # Right wall

# Add some internal walls to make it interesting
# Horizontal wall in middle with gaps
for x in range(3, GRID_W - 3):
    if x != GRID_W // 2 and x != GRID_W // 2 - 1:  # Leave gaps
        maze[GRID_H//2][x] = 1

# Vertical walls
for y in range(3, GRID_H - 3):
    if y != GRID_H // 2 and y != GRID_H // 2 - 1:  # Leave gaps
        maze[y][GRID_W//3] = 1
        maze[y][2*GRID_W//3] = 1

# ---------- Game Elements ----------
# Place pellets in all open spaces (except Pac-Man's start)
pellets = set()
for y in range(GRID_H):
    for x in range(GRID_W):
        if maze[y][x] == 0 and (x, y) != (1, 1):  # Not at Pac-Man start
            pellets.add((x, y))

# Score tracking
score_tracker = ScoreTracker(total_pellets=len(pellets))

# ---------- Pac-Man AI Agent ----------
pacman_start = (1, 1)
pacman = PacmanAI(start_pos=pacman_start, maze=maze)

# ---------- Helper Functions ----------
def nearest_pellet(pos, pellets_set):
    """Find nearest pellet using Manhattan distance"""
    if not pellets_set:
        return None
    return min(pellets_set, key=lambda p: abs(p[0]-pos[0]) + abs(p[1]-pos[1]))

def grid_to_pixel(cell):
    """Convert grid coordinates to pixel coordinates (center of cell)"""
    x, y = cell
    return x * CELL + CELL // 2, y * CELL + CELL // 2

def draw():
    """Draw the game state"""
    window.fill((0, 0, 0))  # Black background
    
    # Draw maze walls
    for y in range(GRID_H):
        for x in range(GRID_W):
            if maze[y][x] == 1:
                pygame.draw.rect(window, (0, 0, 255), (x*CELL, y*CELL, CELL, CELL))
                pygame.draw.rect(window, (0, 0, 150), (x*CELL, y*CELL, CELL, CELL), 2)
    
    # Draw pellets
    for (px, py) in pellets:
        cx, cy = grid_to_pixel((px, py))
        pygame.draw.circle(window, (255, 255, 255), (cx, cy), CELL//6)
    
    # Draw Pac-Man's path (optional visualization)
    if pacman.path:
        for i in range(len(pacman.path) - 1):
            start = grid_to_pixel(pacman.path[i])
            end = grid_to_pixel(pacman.path[i + 1])
            pygame.draw.line(window, (0, 255, 0), start, end, 2)
    
    # Draw Pac-Man
    cx, cy = grid_to_pixel(pacman.pos)
    pygame.draw.circle(window, (255, 255, 0), (cx, cy), CELL//2 - 2)
    
    # Draw score and stats
    score_tracker.draw(window, len(pellets), WIDTH, HEIGHT)
    
    pygame.display.flip()

# ---------- Main Game Loop ----------
# Find initial target
if pellets:
    target = nearest_pellet(pacman.pos, pellets)
    pacman.set_target(target)
    print(f"Initial target: {target}")

running = True
MOVE_DELAY = 200  # Milliseconds between moves
last_move_time = pygame.time.get_ticks()

print(f"Game started! Total pellets: {score_tracker.get_total_pellets()}")
print("Pac-Man will automatically navigate using BFS algorithm")
print("Press ESC to quit")

while running:
    current_time = pygame.time.get_ticks()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Space to pause/unpause
                MOVE_DELAY = 1000 if MOVE_DELAY == 200 else 200
                print(f"Speed changed: {'Slow' if MOVE_DELAY == 1000 else 'Normal'}")
    
    # Move Pac-Man at intervals
    if current_time - last_move_time > MOVE_DELAY:
        last_move_time = current_time
        
        # Check if Pac-Man reached a pellet
        if pacman.pos in pellets:
            pellets.remove(pacman.pos)
            score, pellets_eaten, remaining = score_tracker.eat_pellet(pacman.pos)
            print(f"Pellet eaten at {pacman.pos}! Score: {score}, Remaining: {remaining}")
            
            # Find new target if pellets remain
            if pellets:
                target = nearest_pellet(pacman.pos, pellets)
                pacman.set_target(target)
        
        # Move Pac-Man one step
        if not pacman.step() and pellets:
            # If no current path and pellets exist, find new target
            target = nearest_pellet(pacman.pos, pellets)
            if target:
                pacman.set_target(target)
    
    # Draw everything
    draw()
    clock.tick(60)  # 60 FPS

# Cleanup
score_tracker.print_stats()
pygame.quit()
sys.exit()
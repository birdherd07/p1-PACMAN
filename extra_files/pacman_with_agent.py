"""
Modified Pac-Man with Intelligent Agent Architecture
This version uses states, actions, and performance measures as requested
"""

import pygame
from pacman_ai import PacmanAI
from score_tracker import ScoreTracker
from agent_controller import IntelligentAgent  # NEW: Agent architecture
import sys

# Initialize Pygame
pygame.init()

# ---------- Window Configuration ----------
WIDTH, HEIGHT = 500, 500
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("PACMAN - Intelligent Agent")

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

# ---------- Pac-Man Setup ----------
pacman_start = (1, 1)
pacman_ai = PacmanAI(start_pos=pacman_start, maze=maze)  # Keep for BFS if needed

# NEW: Initialize Intelligent Agent
intelligent_agent = IntelligentAgent(maze, pacman_ai)
pacman_pos = pacman_start

# Mode selection (can be toggled with 'M' key)
USE_INTELLIGENT_AGENT = True  # Set to True to use agent architecture

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
    
    # Draw Pac-Man's path if using BFS mode
    if not USE_INTELLIGENT_AGENT and pacman_ai.path:
        for i in range(len(pacman_ai.path) - 1):
            start = grid_to_pixel(pacman_ai.path[i])
            end = grid_to_pixel(pacman_ai.path[i + 1])
            pygame.draw.line(window, (0, 255, 0), start, end, 2)
    
    # Draw Pac-Man
    cx, cy = grid_to_pixel(pacman_pos if USE_INTELLIGENT_AGENT else pacman_ai.pos)
    color = (255, 255, 0) if USE_INTELLIGENT_AGENT else (255, 200, 0)
    pygame.draw.circle(window, color, (cx, cy), CELL//2 - 2)
    
    # Draw mode indicator
    font = pygame.font.Font(None, 24)
    mode_text = "Mode: Intelligent Agent" if USE_INTELLIGENT_AGENT else "Mode: BFS Pathfinding"
    mode_surface = font.render(mode_text, True, (0, 255, 0))
    window.blit(mode_surface, (10, HEIGHT - 30))
    
    # Draw score and stats
    score_tracker.draw(window, len(pellets), WIDTH, HEIGHT)
    
    pygame.display.flip()

# ---------- Main Game Loop ----------
# Initialize for BFS mode
if not USE_INTELLIGENT_AGENT and pellets:
    target = nearest_pellet(pacman_ai.pos, pellets)
    pacman_ai.set_target(target)
    print(f"BFS Mode - Initial target: {target}")

running = True
MOVE_DELAY = 200  # Milliseconds between moves
last_move_time = pygame.time.get_ticks()

print(f"Game started! Total pellets: {score_tracker.get_total_pellets()}")
print(f"Using: {'INTELLIGENT AGENT with states/actions/performance' if USE_INTELLIGENT_AGENT else 'BFS pathfinding'}")
print("Controls:")
print("  ESC - Quit")
print("  SPACE - Change speed")
print("  M - Toggle between Intelligent Agent and BFS modes")

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
            elif event.key == pygame.K_m:
                # Toggle between modes
                USE_INTELLIGENT_AGENT = not USE_INTELLIGENT_AGENT
                if USE_INTELLIGENT_AGENT:
                    pacman_pos = pacman_ai.pos  # Sync position
                else:
                    pacman_ai.pos = pacman_pos  # Sync position
                    if pellets:
                        target = nearest_pellet(pacman_ai.pos, pellets)
                        pacman_ai.set_target(target)
                print(f"Switched to: {'Intelligent Agent' if USE_INTELLIGENT_AGENT else 'BFS Pathfinding'}")
    
    # Move Pac-Man at intervals
    if current_time - last_move_time > MOVE_DELAY:
        last_move_time = current_time
        
        if USE_INTELLIGENT_AGENT:
            # INTELLIGENT AGENT MODE: Use states, actions, and performance measures
            
            # Agent makes decision based on current state
            old_pos = pacman_pos
            pacman_pos = intelligent_agent.decide_move(pacman_pos, pellets)
            
            # Check if Pac-Man ate a pellet
            if pacman_pos in pellets:
                pellets.remove(pacman_pos)
                score, pellets_eaten, remaining = score_tracker.eat_pellet(pacman_pos)
                print(f"[AGENT] Pellet eaten at {pacman_pos}! Score: {score}, Remaining: {remaining}")
        
        else:
            # BFS MODE: Original pathfinding approach
            
            # Check if Pac-Man reached a pellet
            if pacman_ai.pos in pellets:
                pellets.remove(pacman_ai.pos)
                score, pellets_eaten, remaining = score_tracker.eat_pellet(pacman_ai.pos)
                print(f"[BFS] Pellet eaten at {pacman_ai.pos}! Score: {score}, Remaining: {remaining}")
                
                # Find new target if pellets remain
                if pellets:
                    target = nearest_pellet(pacman_ai.pos, pellets)
                    pacman_ai.set_target(target)
            
            # Move Pac-Man one step
            if not pacman_ai.step() and pellets:
                # If no current path and pellets exist, find new target
                target = nearest_pellet(pacman_ai.pos, pellets)
                if target:
                    pacman_ai.set_target(target)
    
    # Check for victory
    if len(pellets) == 0:
        print("\n🎉 VICTORY! All pellets collected!")
        if USE_INTELLIGENT_AGENT:
            print(intelligent_agent.get_performance_summary())
        running = False
    
    # Draw everything
    draw()
    clock.tick(60)  # 60 FPS

# Cleanup
score_tracker.print_stats()
if USE_INTELLIGENT_AGENT:
    print("\nAgent Performance Summary:")
    print(intelligent_agent.get_performance_summary())
pygame.quit()
sys.exit()

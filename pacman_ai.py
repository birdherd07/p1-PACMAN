# pacman_ai.py
from collections import deque

class PacmanAI:
    """
    Grid-based Pac-Man agent using BFS shortest-path search.
    Maze: 2D list of ints -> 0=open, 1=wall
    Positions are integer grid coords: (x, y)
    """
    def __init__(self, start_pos, maze):
        self.pos = start_pos
        self.maze = maze
        self.path = []  # list of grid cells to walk through
        self.visited_cells = set()  # Track visited cells for visualization

    def _neighbors(self, x, y):
        """Get valid neighboring cells (not walls, within bounds)"""
        for dx, dy in ((1,0), (-1,0), (0,1), (0,-1)):
            nx, ny = x + dx, y + dy
            # Check if inside bounds and not a wall
            if 0 <= ny < len(self.maze) and 0 <= nx < len(self.maze[0]) and self.maze[ny][nx] == 0:
                yield nx, ny

    def bfs(self, start, goal):
        """
        Breadth-First Search to find shortest path from start to goal.
        Returns a list of grid cells from start→goal (inclusive) or [] if none.
        """
        if start == goal:
            return [start]
        
        queue = deque([(start, [])])
        seen = {start}
        
        while queue:
            (x, y), path = queue.popleft()
            
            for nx, ny in self._neighbors(x, y):
                if (nx, ny) in seen:
                    continue
                    
                if (nx, ny) == goal:
                    # Found the goal! Return complete path
                    return path + [(x, y), (nx, ny)]
                
                queue.append(((nx, ny), path + [(x, y)]))
                seen.add((nx, ny))
        
        return []  # No path found

    def set_target(self, target):
        """Compute a fresh path to the target pellet."""
        self.path = self.bfs(self.pos, target)
        if self.path:
            print(f"Found path from {self.pos} to {target}: {len(self.path)} steps")
        else:
            print(f"No path found from {self.pos} to {target}")

    def step(self):
        """Advance one grid cell along current path."""
        if self.path:
            # First element might be current position, skip it
            if self.path[0] == self.pos:
                self.path.pop(0)
            
            # Move to next position in path
            if self.path:
                old_pos = self.pos
                self.pos = self.path.pop(0)
                self.visited_cells.add(old_pos)
                return True
        return False

    def get_position(self):
        """Get current position"""
        return self.pos

    def has_path(self):
        """Check if Pac-Man has a path to follow"""
        return len(self.path) > 0
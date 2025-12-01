# pacman_ai.py
from collections import deque
from game_agent import GameAgent, AgentAction
import random

class PacmanAI (GameAgent):
    """
    Grid-based Pac-Man agent using BFS shortest-path search.
    Maze: 2D list of ints -> 0=open, 1=wall
    Positions are integer grid coords: (x, y)
    """
    def __init__(self, start_pos, maze):
        self.pos = start_pos
        self.prev_pos = start_pos
        self.start_pos = start_pos
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
                # Avoid repeats in path or moving too close to ghosts
                if (nx, ny) in seen or self._adjacent_agent((nx, ny)):
                    continue
                    
                if (nx, ny) == goal:
                    # Found the goal! Return complete path
                    return path + [(x, y), (nx, ny)]
                
                queue.append(((nx, ny), path + [(x, y)]))
                seen.add((nx, ny))
        
        return []  # No path found

    def set_targets(self, targets):
        """Compute a path to each of the target pellets."""
        paths = []
        for target in targets:
            path = self.bfs(self.pos, target)
            if path:
                paths.append(path)

        return paths
    
    def _performance_measure(self, paths):
        """ 
        Return a list of scores, measured for maximizing efficiency (shorter length) and penalizing revisits to visited cells. 
        :param paths: List of possible paths the agent can take.
        """
        scored_points = []
        for path in paths:
            if path:
                penalty = len(self.visited_cells.intersection(set(path))) * 3
                oscillation_penalty = 100 if self.prev_pos in path else 0
                scored_points.append(500 - len(path) - penalty - oscillation_penalty)
        return scored_points

    def step(self, current_state, targets):
        """Advance one grid cell along current path."""
        action, percept = self.pick_action(current_state)

        if action == AgentAction.MOVE or action == AgentAction.AVOID:
            paths = self.set_targets(targets)
            if paths:
                # Score potential moves
                performance_scores = self._performance_measure(paths)
                # Update path to best scored path
                best_index = performance_scores.index(max(performance_scores))
                self.path = paths[best_index]

                if self.path:
                    print(f"Found path from {self.pos} to {self.path[-1]}: {len(self.path)} steps")
                else:
                    print(f"No path found from {self.pos} to {targets}")

                # First element might be current position, skip it
                if self.path[0] == self.pos:
                    self.path.pop(0)
                
                # Move to next position in path
                if self.path:
                    self.prev_pos = self.pos
                    self.pos = self.path.pop(0)
                    self.visited_cells.add(self.prev_pos)
        # elif action == AgentAction.AVOID:
        #     # Move away from other agents
        #     valid_moves = []
        #     for neigh in self._neighbors_list():
        #         if not self._adjacent_agent(neigh):
        #             valid_moves.append(neigh)
        #     if valid_moves:
        #         self.prev_pos = self.pos
        #         self.visited_cells.add(self.prev_pos)
        #         self.pos = valid_moves[random.randint(0, (len(valid_moves) - 1))]


    def get_position(self):
        """Get current position"""
        return self.pos

    def has_path(self):
        """Check if Pac-Man has a path to follow"""
        return len(self.path) > 0
    
    def reset_position(self):
        super().reset_position()
        #Clear old path
        self.path = []
import pygame
import heapq
from typing import Tuple, List, Dict, Optional

class Ghost:
    """
    A Pac-Man style ghost able to navigate a 2D maze.
    Uses an A* pathfinding algorithm to chase Pac-Man.
    """
    # Define the possible movements: (dx, dy)
    # Up, Down, Left, Right
    MOVE_COST = 1
    DIRECTIONS = [
        (0, -1),  # Up
        (0, 1),   # Down
        (-1, 0),  # Left
        (1, 0)    # Right
    ]
    
    def __init__(self, name, start_pos, maze):
        """
        Initializes the Ghost.
        :param name: the name of this Ghost
        :param start_pos: Initial X and Y-coordinate on the grid.
        :param maze: the 2D maze to navigate.
        """
        self.name = name
        self.maze = maze
        self.pos = start_pos
        self.image = pygame.image.load('assets/ghost.png')
        self.current_path: List[Tuple[int, int]] = []
        
    def get_position(self):
        """Returns the ghost's current grid coordinates."""
        return self.pos
    
    def manhattan_distance(self, p1, p2):
        """Calculates the Manhattan distance heuristic (h(n))."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def find_path(self, start, end):
        """
        Finds the shortest path in a 2D grid maze using the A* algorithm.
        :param start: Ghost's (x, y) coordinates.
        :param end: Pac-man's (x, y) coordinates.
        :return: A list of (x, y) coordinates representing the path, or None if no path is found.
        """
        rows, cols = len(self.maze), len(self.maze[0])
        
        # Priority Queue: Stores (f_cost, g_cost, x, y)
        # The smallest f_cost is always prioritized.
        # g_cost is included for tie-breaking, though not strictly required for correctness.
        open_list: List[Tuple[int, int, int, int]] = []
        
        # g_costs: Stores the actual cost from the start to all visited nodes
        g_costs: Dict[Tuple[int, int], int] = {start: 0}
        
        # parents: Stores the path reconstruction
        parents: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {start: None}
        
        # Calculate the initial f_cost and push to the priority queue
        h_start = self.manhattan_distance(start, end)
        heapq.heappush(open_list, (h_start, 0, start[0], start[1])) # (f_cost, g_cost, x, y)

        while open_list:
            # Get the node with the lowest f_cost
            f_cost, g_cost, current_x, current_y = heapq.heappop(open_list)
            current_node = (current_x, current_y)
            
            # Goal Check
            if current_node == end:
                # Reconstruct the path and return it
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parents[current_node]
                return path[:-1][::-1] # Reverse to get path from start to end

            # Explore neighbors
            for dx, dy in self.DIRECTIONS:
                neighbor_x, neighbor_y = current_x + dx, current_y + dy
                neighbor_node = (neighbor_x, neighbor_y)
                
                # 1. Bounds and Wall Check
                if not (0 <= neighbor_x < cols and 0 <= neighbor_y < rows):
                    continue  # Out of bounds
                if self.maze[neighbor_y][neighbor_x] == 1:
                    continue  # Is a wall
                    
                # Calculate new g_cost (cost from start to neighbor)
                new_g_cost = g_cost + self.MOVE_COST
                
                # 2. Check if a better path to the neighbor is found
                # Use `get(neighbor_node, float('inf'))` to treat unvisited nodes as infinite cost
                if new_g_cost < g_costs.get(neighbor_node, float('inf')):
                    
                    # This is the shortest path found so far. Record it.
                    g_costs[neighbor_node] = new_g_cost
                    parents[neighbor_node] = current_node
                    
                    # Calculate the new f_cost
                    h_neighbor = self.manhattan_distance(neighbor_node, end)
                    f_cost_neighbor = new_g_cost + h_neighbor
                    
                    # Add/Update the neighbor in the priority queue
                    heapq.heappush(open_list, (f_cost_neighbor, new_g_cost, neighbor_x, neighbor_y))

        # Path not found
        return None

    def move_to_pacman(self, pacman_pos):
        """
        Calculates the path to Pac-Man, moves the ghost one step along it.
        :param pacman_pos: Pac-Man's X and Y-coordinate (target).
        """
        current_coords = self.get_position()
        # 1. Update Path (Only when the previous path is complete or Pac-Man has moved significantly)
        if not self.current_path or self.current_path[-1] != pacman_pos:
            self.current_path = self.find_path(current_coords, pacman_pos)

        # 2. Execute Move
        if self.current_path:
            # Update the ghost's position to the next grid tile
            self.pos = self.current_path.pop(0)
            #print(f"{self.name} moved to ({self.pos}) along the path.")
        #else:
            #print(f"{self.name} is at or cannot find a path to Pac-Man.")
            
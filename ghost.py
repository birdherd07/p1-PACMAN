import pygame
import random
import heapq
from enum import Enum
from typing import Tuple, List, Dict

class GhostState(Enum):
    NORMAL = 0 # Not close to pac-man for a long time
    SCARED = 1 # Close to pac-man for a while

class GhostActions(Enum):
    MOVE = 0 # Move in one of the four movement directions
    STOP = 1 # Do not move

class Ghost:
    # Define the possible actions: (dx, dy)
    MOVE_COST = 1
    MOVES = [
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
        :param flee: whether the ghost will flee from pac-man when close.
        """
        self.name = name
        self.maze = maze
        self.pos = start_pos
        self.image = pygame.image.load('assets/ghost.png')
        self.scared = 0
            
    def get_position(self):
        """Returns the ghost's current grid coordinates."""
        return self.pos
    
    def _get_state(self, pacman_pos):
        """Updates and returns the current state of the Ghost.
            Ghost will have a higher probablility of being scared the longer it is close to pac-man.
            Ghost will become less scared when not close to pac-man."""
        current_pos = self.get_position()
        for i in self.MOVES:
            if (current_pos[0] + i[0], current_pos[1] + i[1]) == pacman_pos:
                if self.scared < 5:
                    self.scared += 1
                if self.scared >= 3:
                    return GhostState.SCARED
                else:
                    return GhostState.NORMAL
        if self.scared > 0:
            self.scared -= 1        
        if self.scared >= 3:
            return GhostState.SCARED
        else:
            return GhostState.NORMAL

class RandomGhost(Ghost):
    """
    A Pac-Man style ghost that chooses a direction to go at random.
    """
        
    def choose_best_action(self, pacman_pos):
        rows, cols = len(self.maze), len(self.maze[0])
        current_x, current_y = self.get_position()

        possible_moves = []
        # Explore neighbors
        for dx, dy in self.MOVES:
            neighbor_x, neighbor_y = current_x + dx, current_y + dy
            
            # 1. Bounds and Wall Check
            if not (0 <= neighbor_x < cols and 0 <= neighbor_y < rows):
                continue  # Out of bounds
            if self.maze[neighbor_y][neighbor_x] != 0:
                continue  # Is a wall or another ghost

            possible_moves.append((neighbor_x, neighbor_y))
        if possible_moves:
            self.pos = possible_moves[random.randint(0, (len(possible_moves) - 1))]
            return GhostActions.MOVE
        else:
            return GhostActions.STOP


class ChaseGhost(Ghost):
    """
    A Pac-Man style ghost that uses an A* pathfinding algorithm to chase or intercept Pac-Man.
    When state is normal, chooses the shortest path.
    When state is scared, chooses the longest path.
    """
    
    def __init__(self, name, start_pos, maze):
        """
        Initializes the Ghost.
        :param name: the name of this Ghost
        :param start_pos: Initial X and Y-coordinate on the grid.
        :param maze: the 2D maze to navigate.
        :param intercept: whether or not the ghost will try to cut pac-man off from ahead.
        """
        self.name = name
        self.maze = maze
        self.pos = start_pos
        self.image = pygame.image.load('assets/ghost.png')
        self.current_path: List[Tuple[int, int]] = []
        self.scared = 0

    def intercept_positions(self, pacman_pos):
        """
        Return a list of valid positions that are two spaces ahead of pac-man in each direction.
        """    
        valid_positions = []
        for i in self.MOVES:
            adjacent = (pacman_pos[0] + (i[0] * 2), pacman_pos[1] + (i[1] * 2))
            if adjacent[0] < len(self.maze) and adjacent[1] < len(self.maze) and self.maze[adjacent[1]][adjacent[0]] == 0:
                valid_positions.append(adjacent)
        return valid_positions
    
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
            for dx, dy in self.MOVES:
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

    def score_actions(self, state, paths):
        if not paths:
            return None
        # Choose the longest path to pac-man
        if state == GhostState.SCARED:
            return max(paths, key=len)
        # Choose the shortest path
        else: #state == NORMAL
            return min(paths, key=len)

    def choose_best_action(self, pacman_pos):
        """
        Calculates the best path to Pac-Man based on state, moves the ghost one step along it.
        :param pacman_pos: Pac-Man's X and Y-coordinate (target).
        """
        # 1. Get State
        state = self._get_state(pacman_pos)
        current_coords = self.get_position()
        # 2. Find possible paths: to pacman and to intercept it from each direction
        paths = []
        coords = self.intercept_positions(pacman_pos)
        coords.append(pacman_pos)
        for coord in coords:
            paths.append(self.find_path(current_coords, coord))
        # 3. Pick a path based on state
        self.current_path = self.score_actions(state, paths)
        # 2. Execute Action
        if self.current_path:
            # Move action: Update the ghost's position to the next grid tile. If next tile has a ghost, move to the next closest space (if available)
            next_pos = self.current_path.pop(0)

            while self.maze[next_pos[1]][next_pos[0]] == 2:
                try:
                    next_pos = self.current_path.pop(0)
                except IndexError as e:
                    return
            self.pos = next_pos
            return GhostActions.MOVE
        else:
            # No paths: Stop
            return GhostActions.STOP
            
import pygame
import random
import heapq
from typing import Optional, Tuple, List, Dict
from game_agent import *

class RandomGhost(GameAgent):
    """
    A Pac-Man style ghost that moves straight until it hits an obstacle, then turns in a random direction.
    """

    def __init__(self, name, start_pos, maze):
        """
        Initializes the Ghost.
        Stores the ghost's last known direction.
        """
        super().__init__(start_pos, maze)
        self.name = name
        self.direction = self.DIRECTIONS[3]
        self.image = pygame.image.load('assets/randghost.png')

    def move(self, dirs):
        """
        Attempt to keep moving in the same direction. If obstacles, turn in a random direction.
        """
        rows, cols = len(self.maze), len(self.maze[0])
        current_x, current_y = self.get_position()
        neighbor_x, neighbor_y = current_x + self.direction[0], current_y + self.direction[1]
        # Move in the same direction
        if (0 <= neighbor_x < cols) and (0 <= neighbor_y < rows) and self.maze[neighbor_y][neighbor_x] == 0:
            self.pos = (neighbor_x, neighbor_y)
        else:
            # Find the directions that the ghost can move to
            valid_dirs = []
            for dx, dy in dirs:
                if self.maze[current_y + dy][current_x + dx] == 0:
                    valid_dirs.append((dx, dy))
            # Choose a random new direction
            if dirs:
                self.direction = valid_dirs[random.randint(0, (len(valid_dirs) - 1))]
                self.pos = (current_x + self.direction[0], current_y + self.direction[1])
        
    def pick_action(self, pacman_pos, game_state):
        """ 
        Pick an action based on the current percept, state and rules.
        """
        action, valid_dirs = super().pick_action(game_state)

        if action == AgentAction.MOVE or action == AgentAction.AVOID:
            # Walls and other agents are treated the same by this simple agent
            self.move(valid_dirs)

        return action

class ChaseGhost(GameAgent):
    """
    A Pac-Man style ghost that uses an A* pathfinding algorithm to chase or intercept Pac-Man.
    Chooses the best path based on a performance measure of path length.
    """
    
    def __init__(self, name, start_pos, maze):
        """
        Initializes the Ghost.
        Stores the ghost's last known path.
        """
        super().__init__(start_pos, maze)
        self.name = name
        self.current_path: List[Tuple[int, int]] = []
        self.image = pygame.image.load('assets/chaseghost.png')
        
    def intercept_positions(self, pacman_pos):
        """
        Return a list of valid intercept positions that are two spaces ahead of pac-man in each direction, plus pac-man's current position.
        """    
        valid_positions = []
        valid_positions.append(pacman_pos)
        for i in self.DIRECTIONS:
            adjacent = (pacman_pos[0] + (i[0] * 2), pacman_pos[1] + (i[1] * 2))
            if adjacent[0] < len(self.maze) and adjacent[1] < len(self.maze) and self.maze[adjacent[1]][adjacent[0]] == 0:
                valid_positions.append(adjacent)
        return valid_positions
    
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
                return path[::-1] # Reverse to get path from start to end

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

    def pick_action(self, pacman_pos, game_state):
        """ 
        Pick the best scored action based on the current percept, state and rules.
        """
        action, valid_dirs = super().pick_action(game_state)
        position = self.get_position()

        if action == AgentAction.MOVE or action == AgentAction.AVOID:
            # Calculate moves
            valid_goals = self.intercept_positions(pacman_pos)
            potential_moves = []
            for goal in valid_goals:
                potential_moves.append(self.find_path(position, goal))
            # Score potential moves
            performance_scores = self._performance_measure(potential_moves)
            # Update path to best scored path
            best_index = performance_scores.index(max(performance_scores))
            self.current_path = potential_moves[best_index]
            if self.current_path:
                # Update the ghost's position to the next grid tile in path.
                next_pos = self.current_path.pop(0)
                if position == next_pos and self.current_path:
                    next_pos = self.current_path.pop(0)
                
                if self.maze[next_pos[1]][next_pos[0]] == 2:
                    # Move in a valid direction not occupied by other ghost (if available)
                    dirs = []
                    for dx, dy in valid_dirs:
                        if self.maze[position[1] + dy][position[0] + dx] == 0:
                            dirs.append((position[0] + dx, position[1] + dy))
                    if dirs:
                        next_pos = dirs[random.randint(0, (len(dirs) - 1))]

                self.pos = next_pos

        return action
    
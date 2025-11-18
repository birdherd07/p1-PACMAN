import pygame
import random
import heapq
from enum import Enum
from typing import Optional, Tuple, List, Dict

class GhostAction(Enum):
    MOVE = 0
    STOP = 1

class GhostState(Enum):
    CLEAR = 0 # Can move in at least one direction
    BLOCKED = 1 # Surrounded on all sides

class GhostAgent:
    """ Parent class for the two ghost types. """
    MOVE_COST = 1

    # The four directions
    DIRECTIONS = [
        (0, -1),  # Up
        (0, 1),   # Down
        (-1, 0),  # Left
        (1, 0)    # Right
    ]

    State = Tuple[GhostState, str]
    # Rule Table: Maps State (Percept) -> Action
    RULE_TABLE: Dict[State, GhostAction]= {
        # Condition 1: Chasing pac-man and clear to keep moving
        (GhostState.CLEAR, "Chasing") : GhostAction.MOVE,
        
        # Condition 2: Chasing but blocked on all directions
        (GhostState.BLOCKED, "Chasing") : GhostAction.STOP,

        # Conditons 3 - 4 : Caught pac-man
        (GhostState.CLEAR, "Caught") : GhostAction.STOP,

        (GhostState.BLOCKED, "Caught") : GhostAction.STOP
    }

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

    def _perceive(self, pacman_pos):
        """
        Check the ghost's current surroundings.
        """
        rows, cols = len(self.maze), len(self.maze[0])

        # Check if the ghost has caught pac-man 
        if (self.get_position() == pacman_pos):
            pacman_percept = "Caught"
        else:
            pacman_percept = "Chasing"

        # Check neighboring spaces
        current_x, current_y = self.get_position()
        neighbors = []
        valid_dirs = []
        for dx, dy in self.DIRECTIONS:
            neighbor_x, neighbor_y = current_x + dx, current_y + dy
            # Bounds check
            if 0 <= neighbor_x < cols and 0 <= neighbor_y < rows:
                neighbors.append(self.maze[neighbor_y][neighbor_x])
                valid_dirs.append((dx, dy))

        return (neighbors, pacman_percept), valid_dirs
        
    def _state(self, perceive):
        """ Return the agent's state based on the current percept """
        neighs, percept = perceive
        # Check if blocked in all directions
        if all(i != 0 for i in neighs):
            state = GhostState.BLOCKED
        else:
            state = GhostState.CLEAR
        return (state, percept)
    
    def _rule_to_action(self, state):
        """ Get the rule's action for the current state """
        return self.RULE_TABLE.get(state)
            
    def get_position(self):
        """Returns the ghost's current grid coordinates."""
        return self.pos
        
    def manhattan_distance(self, p1, p2):
        """Calculates the Manhattan distance heuristic (h(n))."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class RandomGhost(GhostAgent):
    """
    A Pac-Man style ghost that moves in a line until it hits an obstacle, then turns in a random direction.
    """

    def __init__(self, name, start_pos, maze):
        """
        Initializes the Ghost.
        Stores the ghost's last known direction.
        """
        super().__init__(name, start_pos, maze)
        self.direction = self.DIRECTIONS[0]

    def find_path(self, dirs):
        # Attempt to keep moving in the same direction
        rows, cols = len(self.maze), len(self.maze[0])
        current_x, current_y = self.get_position()
        neighbor_x, neighbor_y = current_x + self.direction[0], current_y + self.direction[1]

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
        
    def pick_action(self, pacman_pos):
        """ 
        Pick an action based on the current percept, state and rules.
        """
        percept, valid_dirs = self._perceive(pacman_pos)
        state = self._state(percept)
        action = self._rule_to_action(state)
        if action == GhostAction.MOVE:
            # Try to move in the current direction, else turn in a random valid direction
            self.find_path(valid_dirs)

        return action

class ChaseGhost(GhostAgent):
    """
    A Pac-Man style ghost that uses an A* pathfinding algorithm to chase or intercept Pac-Man.
    Chooses the best path based on a performance measure of path length.
    """
    
    def __init__(self, name, start_pos, maze):
        """
        Initializes the Ghost.
        Stores the ghost's last known path.
        """
        super().__init__(name, start_pos, maze)
        self.current_path: List[Tuple[int, int]] = []
        
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
    
    def performance_measure(self, paths):
        """ Score paths by length. Shortest paths to pac-man score highest. """
        scores = []
        longest = len(max(paths, key=len))
        for path in paths:
            scores.append(abs(len(path) - longest))
        return scores

    def pick_action(self, pacman_pos):
        """ 
        Pick the best scored action based on the current percept, state and rules.
        """
        percept, valid_dirs = self._perceive(pacman_pos)
        state = self._state(percept)
        action = self._rule_to_action(state)

        if action == GhostAction.MOVE:
            # Calculate moves
            valid_goals = self.intercept_positions(pacman_pos)
            position = self.get_position()
            potential_moves = []
            for goal in valid_goals:
                potential_moves.append(self.find_path(position, goal))
            # Score potential moves
            performance_scores = self.performance_measure(potential_moves)
            # Update path to best scored path
            best_index = performance_scores.index(max(performance_scores))
            self.current_path = potential_moves[best_index]
            if self.current_path:
                # Update the ghost's position to the next grid tile in path. If next tile has a ghost, move to the next closest space (if available)
                next_pos = self.current_path.pop(0)

                while self.maze[next_pos[1]][next_pos[0]] == 2:
                    try:
                        next_pos = self.current_path.pop(0)
                    except IndexError as e:
                        return
                self.pos = next_pos

        return action
    
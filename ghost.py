import pygame
import random
from game_agent import *

class Ghost(GameAgent):
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

    def move(self):
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
            # Choose a random new direction
            valid_dirs = self._neighbors_list()
            if valid_dirs:
                new_pos = valid_dirs[random.randint(0, (len(valid_dirs) - 1))]
                self.direction = (new_pos[0] - self.pos[0], new_pos[1] - self.pos[1])
                self.pos = new_pos
        
    def step(self, game_state):
        """ 
        Pick an action based on the current percept, state and rules.
        """
        action = self.pick_action(game_state)

        if action == AgentAction.MOVE or action == AgentAction.AVOID:
            self.move()

        return action
    
    def reset_position(self):
        """ Return agent to start position and reset its direction. """
        super().reset_position()
        # Reset old direction
        self.direction = self.DIRECTIONS[3]
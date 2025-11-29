from enum import Enum
from typing import Tuple, Dict

class AgentAction(Enum):
    """
    Possible actions for an agent to take.
    """
    MOVE = 0 # Move towards goal
    AVOID = 1 # Move away from obstacle
    STOP = 2 # Do not move

class AgentState(Enum):
    """
    Possible states based on the environment.
    """
    CLEAR = 0 # No obstructions
    NEAR_AGENT = 1 # Next to at least one other agent
    BLOCKED = 2 # Blocked on all sides

class GameState(Enum):
    """
    Possible states of completion of the game's goal.
    """
    ACTING = 0 # Agent has not reached goal yet
    GOAL = 1 # Agent has reached goal

class GameAgent:
    """ 
    Parent class for game agents: Pac-man and Ghosts. 
    """
    MOVE_COST = 1 # Cost to move one space

    DIRECTIONS = [
        (0, -1),  # Up
        (0, 1),   # Down
        (-1, 0),  # Left
        (1, 0)    # Right
    ]

    State = Tuple[AgentState, GameState]
    # Rule Table: Maps State -> Action
    RULE_TABLE: Dict[State, AgentAction]= {
        # Rule 1: Clear path, not at goal -> Move towards goal
        (AgentState.CLEAR, GameState.ACTING) : AgentAction.MOVE,

        # Rule 2: Next to agent, not at goal -> Avoid agent
        (AgentState.NEAR_AGENT, GameState.ACTING) : AgentAction.AVOID,
        
        # Rule 3: Blocked on all sides, not at goal -> Do not move
        (AgentState.BLOCKED, GameState.ACTING) : AgentAction.STOP,

        # Rule 4: Can move, at goal -> Do not move
        (AgentState.CLEAR,  GameState.GOAL) : AgentAction.STOP,

        # Rule 5: Next to agent, at goal -> Do not move
        (AgentState.NEAR_AGENT, GameState.GOAL) : AgentAction.STOP,

        # Rule 6: Blocked on all sides, at goal -> Do not move
        (AgentState.BLOCKED, GameState.GOAL) : AgentAction.STOP
    }

    def __init__(self, start_pos, maze):
        """
        Initializes the Agent.
        :param start_pos: Initial X and Y-coordinate on the grid.
        :param maze: the 2D maze to navigate.
        """
        self.maze = maze
        self.start_pos = start_pos
        self.pos = start_pos

    def _perceive(self):
        """
        Check the Agent's current surroundings and return a list of valid neighbors and directions.
        """
        rows, cols = len(self.maze), len(self.maze[0])

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

        return neighbors, valid_dirs
        
    def _state(self, neighs):
        """ 
        Returns the agent's state based on the current percept 
        :param neighs: the perceived neighboring spaces of the agent
        """
        # Blocked in all directions by walls or other agents
        if all(i != 0 for i in neighs):
            state = AgentState.BLOCKED
        elif 2 in neighs: # Next to at least one agent
            state = AgentState.NEAR_AGENT
        else:
            state = AgentState.CLEAR
        return state
    
    def _rule_to_action(self, state):
        """ 
        Returns the rule-based action for the current state from the rule_table.
        :param state: The agent's state and goal status. 
        """
        return self.RULE_TABLE.get(state)
            
    def get_position(self):
        """ Returns the ghost's current grid coordinates. """
        return self.pos
        
    def reset_position(self):
        """Sets this agent's position to its starting position."""
        self.pos = self.start_pos
    
    def _performance_measure(self, paths):
        """ 
        Return a list of scores, measured for maximizing efficiency (shorter length). 
        :param paths: List of possible paths the agent can take.
        """
        scored_points = []
        for path in paths:
            scored_points.append(500-len(path))
        return scored_points
    
    def manhattan_distance(self, p1, p2):
        """Calculates the Manhattan distance heuristic (h(n))."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def pick_action(self, game_state):
        """ 
        Pick the best action based on the current percept, state and rules.
        """
        neighbors, valid_dirs = self._perceive()
        agent_state = self._state(neighbors)
        action = self._rule_to_action((agent_state, game_state))

        return action, valid_dirs
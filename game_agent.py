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
    NEAR_AGENT = 1 # Near to at least 1 other agent
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

        # Rule 2: Near agent, not at goal -> Avoid agent
        (AgentState.NEAR_AGENT, GameState.ACTING) : AgentAction.AVOID,
        
        # Rule 3: Blocked on all sides, not at goal -> Do not move
        (AgentState.BLOCKED, GameState.ACTING) : AgentAction.STOP,

        # Rule 4: Can move, at goal -> Do not move
        (AgentState.CLEAR,  GameState.GOAL) : AgentAction.STOP,

        # Rule 5: Near agent, at goal -> Do not move
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
    
    def _neighbors_list(self):
        """Get all valid neighboring cells within bounds"""
        rows, cols = len(self.maze), len(self.maze[0])
        x, y = self.get_position()

        # List of adjacent spaces the agent can move to
        neighs = []
        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            # Bounds check
            if 0 <= nx < cols and 0 <= ny < rows and self.maze[ny][nx] == 0:
                neighs.append((nx, ny))
        return neighs  
    
    def _adjacent_agent(self, pos):
        """
        Return whether a cell is next to an agent.
        :param pos: The cell to check.
        """
        rows, cols = len(self.maze), len(self.maze[0])
        x, y = pos

        for dx, dy in self.DIRECTIONS:
            nx, ny = x + dx, y + dy
            # Bounds check
            if 0 <= nx < cols and 0 <= ny < rows and self.maze[ny][nx] == 2:
                return True
        return False 
    
    def manhattan_distance(self, p1, p2):
        """Calculates the Manhattan distance heuristic (h(n))."""
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def _perceive(self):
        """Check the Agent's current surroundings within 2 spaces and return the number of other agents detected."""
        rows, cols = len(self.maze), len(self.maze[0])
        x, y = self.get_position()
        num_agents = 0

        # Check all spaces within 2 spaces
        for r_offset in range(-2, 3):  # From -2 to 2 (inclusive)
            for c_offset in range(-2, 3):  # From -2 to 2 (inclusive)
                # Skip the central cell itself
                if r_offset == 0 and c_offset == 0:
                    continue

                ny = y + r_offset
                nx = x + c_offset

                # Check if the neighbor coordinates are within the grid boundaries
                if 0 <= ny < rows and 0 <= nx < cols and self.maze[ny][nx] == 2:
                    num_agents += 1
        return num_agents
        
    def _state(self, agents, neighs):
        """ 
        Returns the agent's state based on the current percept 
        :param percept: the perceived neighboring spaces of the agent
        """
        # Blocked in all adjacent spaces by walls or other agents
        if len(neighs) == 0:
            state = AgentState.BLOCKED
        elif agents > 0: # At least one agent is within 2 spaces
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
    
    def pick_action(self, game_state):
        """ 
        Pick the best action based on the current percept, state and rules.
        """
        percept = self._perceive()
        agent_state = self._state(percept, self._neighbors_list())
        action = self._rule_to_action((agent_state, game_state))

        return action
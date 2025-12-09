"""
Intelligent Agent Controller for Pac-Man
Implements the agent architecture with states, actions, and performance measures
Based on the Intelligent Agent slides (vacuum cleaner example)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple, List, Optional, Set

class Action(Enum):
    """Possible actions for Pac-Man"""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    STOP = (0, 0)

@dataclass
class GameState:
    """
    Represents the current state of the game from Pac-Man's perspective
    This is what the agent "perceives" about its environment
    """
    pacman_pos: Tuple[int, int]
    pellet_north: bool
    pellet_south: bool
    pellet_east: bool
    pellet_west: bool
    ghost_nearby: bool
    ghost_distance: int
    pellets_remaining: int
    nearest_pellet_distance: int
    
    def __str__(self):
        """String representation for debugging"""
        directions = []
        if self.pellet_north: directions.append("N")
        if self.pellet_south: directions.append("S")
        if self.pellet_east: directions.append("E")
        if self.pellet_west: directions.append("W")
        
        return f"State(pos={self.pacman_pos}, pellets_in:{directions}, ghost:{self.ghost_distance})"

class IntelligentAgent:
    """
    Implements the intelligent agent architecture for Pac-Man
    Uses states, actions, and performance measures to make decisions
    """
    
    def __init__(self, maze, pacman_ai):
        """
        Initialize the intelligent agent
        
        Args:
            maze: 2D list representing the maze (0=open, 1=wall)
            pacman_ai: Reference to the PacmanAI object for pathfinding
        """
        self.maze = maze
        self.pacman_ai = pacman_ai
        self.previous_state = None
        self.performance_history = []
        
    def perceive(self, pacman_pos: Tuple[int, int], 
                 pellets: Set[Tuple[int, int]], 
                 ghosts: List[Tuple[int, int]] = None) -> GameState:
        """
        Perceive the environment and create a state representation
        
        Args:
            pacman_pos: Current position of Pac-Man
            pellets: Set of remaining pellet positions
            ghosts: List of ghost positions (if any)
            
        Returns:
            GameState object representing the current situation
        """
        x, y = pacman_pos
        
        # Check for pellets in each direction
        pellet_north = (x, y-1) in pellets
        pellet_south = (x, y+1) in pellets
        pellet_east = (x+1, y) in pellets
        pellet_west = (x-1, y) in pellets
        
        # Calculate ghost proximity
        ghost_nearby = False
        ghost_distance = float('inf')
        if ghosts:
            for gx, gy in ghosts:
                dist = abs(x - gx) + abs(y - gy)  # Manhattan distance
                ghost_distance = min(ghost_distance, dist)
                if dist <= 3:  # Ghost is nearby if within 3 cells
                    ghost_nearby = True
        
        # Find nearest pellet distance
        nearest_pellet_distance = float('inf')
        if pellets:
            for px, py in pellets:
                dist = abs(x - px) + abs(y - py)
                nearest_pellet_distance = min(nearest_pellet_distance, dist)
        
        return GameState(
            pacman_pos=pacman_pos,
            pellet_north=pellet_north,
            pellet_south=pellet_south,
            pellet_east=pellet_east,
            pellet_west=pellet_west,
            ghost_nearby=ghost_nearby,
            ghost_distance=ghost_distance,
            pellets_remaining=len(pellets),
            nearest_pellet_distance=nearest_pellet_distance
        )
    
    def evaluate_action(self, state: GameState, action: Action, 
                       next_pos: Tuple[int, int], pellets: Set) -> float:
        """
        Performance measure: evaluate how good an action is
        
        Args:
            state: Current game state
            action: Action to evaluate
            next_pos: Position after taking the action
            pellets: Set of pellet positions
            
        Returns:
            Score for the action (higher is better)
        """
        score = 0
        
        # Reward for eating a pellet
        if next_pos in pellets:
            score += 10  # High reward for getting a pellet
            
        # Penalty for moving to empty space
        elif action != Action.STOP:
            score -= 1  # Small penalty to encourage efficiency
            
        # Large penalty for getting too close to ghost
        if state.ghost_nearby and state.ghost_distance <= 2:
            score -= 50  # Avoid ghosts
            
        # Bonus for moving toward nearest pellet
        if state.nearest_pellet_distance > 0:
            dx, dy = action.value
            new_x, new_y = state.pacman_pos[0] + dx, state.pacman_pos[1] + dy
            
            # Check if this action reduces distance to nearest pellet
            old_dist = state.nearest_pellet_distance
            new_dist = float('inf')
            for px, py in pellets:
                new_dist = min(new_dist, abs(new_x - px) + abs(new_y - py))
            
            if new_dist < old_dist:
                score += 2  # Reward for moving closer to pellets
                
        return score
    
    def choose_action(self, state: GameState, pellets: Set) -> Action:
        """
        Choose the best action based on the current state
        
        Args:
            state: Current game state
            pellets: Set of remaining pellets
            
        Returns:
            Best action to take
        """
        x, y = state.pacman_pos
        best_action = Action.STOP
        best_score = float('-inf')
        
        # Evaluate each possible action
        for action in Action:
            if action == Action.STOP:
                continue  # Only stop if no other good options
                
            dx, dy = action.value
            next_x, next_y = x + dx, y + dy
            
            # Check if move is valid (not into wall, within bounds)
            if not self._is_valid_position(next_x, next_y):
                continue
                
            # Evaluate this action
            score = self.evaluate_action(state, action, (next_x, next_y), pellets)
            
            if score > best_score:
                best_score = score
                best_action = action
        
        # Record performance for learning/debugging
        self.performance_history.append(best_score)
        
        return best_action
    
    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is valid (not a wall and within bounds)"""
        if 0 <= y < len(self.maze) and 0 <= x < len(self.maze[0]):
            return self.maze[y][x] == 0
        return False
    
    def decide_move(self, pacman_pos: Tuple[int, int], 
                   pellets: Set[Tuple[int, int]], 
                   ghosts: List[Tuple[int, int]] = None) -> Tuple[int, int]:
        """
        Main decision function: perceive, think, and act
        
        Args:
            pacman_pos: Current Pac-Man position
            pellets: Set of pellet positions
            ghosts: List of ghost positions
            
        Returns:
            Next position for Pac-Man to move to
        """
        # 1. PERCEIVE: Create state from perceptions
        state = self.perceive(pacman_pos, pellets, ghosts)
        
        # 2. THINK: Choose best action based on state
        action = self.choose_action(state, pellets)
        
        # 3. ACT: Convert action to next position
        dx, dy = action.value
        next_pos = (pacman_pos[0] + dx, pacman_pos[1] + dy)
        
        # Debug output
        print(f"State: {state}")
        print(f"Chosen Action: {action.name} -> Position: {next_pos}")
        print(f"Performance Score: {self.performance_history[-1] if self.performance_history else 0}")
        
        self.previous_state = state
        return next_pos
    
    def get_performance_summary(self):
        """Get a summary of the agent's performance"""
        if not self.performance_history:
            return "No performance data yet"
        
        avg_score = sum(self.performance_history) / len(self.performance_history)
        return f"Average performance: {avg_score:.2f}, Total decisions: {len(self.performance_history)}"


# Example usage showing how to integrate with existing code
if __name__ == "__main__":
    # Example maze (0=open, 1=wall)
    example_maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    
    # Example usage
    from pacman_ai import PacmanAI
    
    pacman_ai = PacmanAI((1, 1), example_maze)
    agent = IntelligentAgent(example_maze, pacman_ai)
    
    # Example pellets
    pellets = {(2, 1), (3, 1), (3, 3)}
    
    # Get decision
    current_pos = (1, 1)
    next_pos = agent.decide_move(current_pos, pellets)
    print(f"Agent decides to move from {current_pos} to {next_pos}")

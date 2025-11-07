# PACMAN AI Agent - Group Project 1

## Team Members
- **Liu** - Pac-Man AI Pathfinding (BFS Algorithm)
- **Rachel** - Maze Design and Ghosts
- **Yogitha** - Score Tracking System

## Project Overview
This project implements an intelligent PACMAN game where the PACMAN character acts as an autonomous agent using AI search algorithms to navigate the maze and collect pellets.

## Liu's Contribution: Pac-Man AI Pathfinding

### Implementation Details
- **Algorithm Used**: Breadth-First Search (BFS)
- **File**: `pacman_ai.py`
- **Key Features**:
  - Automatic pathfinding to nearest pellet
  - Guaranteed shortest path in unweighted maze
  - Dynamic path recalculation when pellet is eaten
  - Collision avoidance with walls

### How the BFS Algorithm Works
1. **Start**: Pac-Man's current position
2. **Goal**: Nearest pellet (using Manhattan distance)
3. **Process**:
   - Uses a queue to explore cells level by level
   - Marks visited cells to avoid cycles
   - Returns the shortest path when goal is found
4. **Movement**: Pac-Man follows the computed path step-by-step

## Rachel: Maze and Ghosts

### Implementation Details
- **Algorithm Used**: A* Algorithm
- **Files**: `level.py, ghost.py`
- **Key Features**:
  - Pathfinding shortest path to Pac-Man and random movement
  - 2D Maze representation
  - Custom level sprites

### How the A* Algorithm Works
1. **Start**: Ghost's current position
2. **Goal**: Pac-Man's current position
3. **Process**:
   - Uses a priority queue to explore cells with lowest cost
   - manhattan_distance: The heuristic function, h(n). It calculates the distance by only allowing movement along the grid axes (horizontal and vertical).
   - g_costs: A dictionary storing the shortest actual distance g(n) from the start node to every other reachable node.
   - Loop Logic: The core loop continuously extracts the lowest-f(n) node, checks if it's the goal, and then explores its neighbors. It updates a neighbor's path only if a shorter g(n) is discovered.

### Code Structure
```python
class PacmanAI:
    - __init__(): Initialize with starting position and maze
    - bfs(): Core search algorithm
    - set_target(): Compute path to target pellet
    - step(): Move one cell along the path

class GhostAgent:
   - class GhostState(Enum): Defines the two possible ghost states
   - class GhostAction(Enum): Defintes the two types of ghost actions
   - class RandomGhost(Ghost): A type of Ghost that keeps moving in one direction until blocked, then turns randomly.
   - class ChaseGhost(Ghost): A type of Ghost that chases or intercepts Pac-man depending on state
    - __init__(): Initialize with name, starting position and maze
    - _get_state(): Update and return the current state
    - intercept_positions(): Return a list of valid positions to pac-man or two spaces ahead in any direction
    - find_path(): A* algorithm
    - performance_measure(): Score the available paths based on length
    - pick_action(): Get the percept, state and rule-based action, execute the best scored action

class Level:
    - __init__(): Initialize maze layout and tile sprites for display
```

## Running the Game

### Prerequisites
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Mac/Linux
# or
.venv\Scripts\activate  # On Windows

pip install pygame
```

### Run the Game
```bash
python3 pacman.py
```

### Controls
- **ESC**: Quit game
- **SPACE**: Toggle speed (slow/normal)
- The Pac-Man moves automatically using AI

## Technical Details

### Maze Representation
- 2D array where:
  - `0` = Open path (Pac-Man can move)
  - `1` = Wall (blocked)

### Search Algorithm Choice
**Why BFS?**
- Guarantees shortest path in unweighted graphs
- Complete: will find solution if it exists
- Optimal for our grid-based maze
- Time Complexity: O(V + E) where V=cells, E=connections

### Challenges Faced and Solutions
1. **Challenge**: Coordinating grid coordinates with pixel rendering
   - **Solution**: Created `grid_to_pixel()` helper function

2. **Challenge**: Smooth movement visualization
   - **Solution**: Added configurable move delay (200ms default)

3. **Challenge**: Path recalculation efficiency
   - **Solution**: Only recalculate when pellet is eaten

## AI/LLM Usage Documentation

### Tools Used
- **ChatGPT**: Initial project setup, environment configuration
- **Claude**: Code refinement, BFS implementation, documentation
- **Gemini**: Maze generation, A* implementation

### Specific AI Assistance

#### Environment Setup
- **Prompt**: "How to install pygame on macOS with Apple Silicon?"
- **AI Response**: Provided step-by-step Homebrew and SDL2 installation
- **Modification**: Adapted for our specific Python 3.14 environment

#### BFS Algorithm
- **Prompt**: "Implement BFS pathfinding for Pac-Man in a 2D grid"
- **AI Response**: Basic BFS template
- **Modification**: Added neighbor validation, path reconstruction, and integration with game loop

#### Code Debugging
- **Prompt**: "Why is 'SDL.h' file not found when installing pygame?"
- **AI Response**: Explained SDL2 dependency issue on macOS
- **Modification**: Installed SDL2 via Homebrew before pygame

#### Maze generation
- **Prompt**: "Generate a 25 x 25 pac-man style maze, where a 1 represents a wall and a 0 represents an empty space"
- **AI Response**: Generated maze
- **Modification**: Fixed boundary of maze in 2 rows

#### A* algorithm
- **Prompt**: "Please generate a python A* pathfinding algorithm for a 2d maze"
- **AI Response**: Explained A* algorithm and provided implementation with driver
- **Modification**: Removed driver, customized function parameters to fit within class

#### Design of Ghost rules and actions
- **Prompt**: "In python, what is the optimal way to design a set of rules and actions for a reflex agent?"
- **AI Response**: Provided vacuum cleaner example, using a dictionary as a rule table with a tuple as key
- **Modification**: Customized dictionary rules to fit the Ghost class


### Validation Process
1. Tested each AI-generated function independently
2. Verified pathfinding correctness with print statements
3. Ensured proper maze boundary checking
4. Validated pellet collection and score updates

## Performance Metrics
- Pac-Man successfully navigates to all pellets
- Always takes shortest path (BFS guarantee)
- Average completion time: ~30 seconds for 20x20 maze
- No pathfinding failures observed

## Future Improvements
- [ ] Implement A* algorithm for comparison
- [ ] Optimize path recalculation
- [ ] Add difficulty levels
- [ ] Implement power-ups
- [ ] Make unique ghost behavior

## Testing Instructions
1. Run `python3 pacman.py`
2. Observe Pac-Man automatically navigating
3. Verify shortest path is taken
4. Check score increases by 10 per pellet
5. Confirm "YOU WIN!" appears when all pellets collected

## Repository Structure
```
p1-PACMAN/
├── pacman.py        # Main game file
├── pacman_ai.py     # BFS pathfinding logic (Liu's work)
├── README.md        # This file
├── requirements.txt # Python dependencies
└── .venv/          # Virtual environment
```

## Conclusion
The project successfully demonstrates AI agent design using rational decision-making through BFS search algorithm. The Pac-Man agent autonomously navigates the maze, always choosing the optimal path to collect pellets efficiently.
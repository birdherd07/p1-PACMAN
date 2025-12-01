# PACMAN AI Agent - Group Project 1

## Team Members
- **Liu** - Pac-Man AI Pathfinding (BFS Algorithm)
- **Yogitha** - Score Tracking System
- **Rachel** - Maze, Agent and Ghost design

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
2. **Goal**: Nearest pellets (using Manhattan distance)
3. **Process**:
   - Uses a queue to explore cells level by level
   - Marks visited cells to avoid cycles and avoids ghosts
   - Returns the shortest path when goal is found
4. **Movement**: Pac-Man follows the computed path step-by-step

## Yogitha's Contribution: Score Tracking System
### Implementation Details
- **File**: `score_tracker.py`
- **Key Features**:
  - Real-time score calculation and tracking
  - Pellet consumption monitoring
  - Visual score display on game screen
  - Win condition detection
  - Game statistics reporting

### How the Score Tracker Works
1. **Initialization**: Tracks total pellets and configurable pellet value (default: 10 points)
2. **Pellet Collection**: Updates score and pellet count when Pac-Man eats a pellet
3. **Display**: Renders score and remaining pellets on screen in real-time
4. **Win Detection**: Displays "YOU WIN!" message when all pellets are collected
5. **Statistics**: Provides final game statistics upon completion

### Features
- **Configurable Scoring**: Pellet value can be customized (default: 10 points per pellet)
- **Real-time Updates**: Score updates immediately when pellets are collected
- **Visual Feedback**: Score and pellet count displayed prominently on screen
- **Progress Tracking**: Shows remaining pellets (e.g., "Pellets: 15/20")
- **Win Detection**: Automatically detects and displays win condition

## Rachel: Level, GameAgent, Ghost

### Implementation Details
- **Files**: `level.py, game_agent.py, ghost.py`
- **Key Features**:
  - GameAgent class defining game and agent states, agent actions, and a rule table
  - Maze navigation in the Ghost class
  - Collision detection and handling if a ghost catches pac-man
  - 2D maze representation
  - Custom level sprites

### How the GameAgent Class Works
1. **Pick_action**: Called when an agent needs to decide on an action
2. **Percept**: The agent detects surroundings within 2 spaces
3. **State**: Uses percept information to return an AgentState
4. **Rule to Action**: Uses Game and Agent states to return an AgentAction from the rule table
5. **Agent Action**: Pick_action's returned action determines the agent's behavior

### Code Structure
```python
class PacmanAI:
    - __init__(): Initialize with starting position and maze
    - bfs(): Core search algorithm
    - set_targets(): Compute path to nearest target pellets
    - _performance_measure(): Score potential paths by efficiency.
    - step(): Move one cell along the path

class ScoreTracker:
    - __init__(): Initialize with total pellets and pellet value
    - eat_pellet(): Update score when pellet is eaten
    - get_score(): Retrieve current score
    - get_pellets_eaten(): Get count of eaten pellets
    - draw(): Render score and pellet info on screen
    - print_stats(): Display final game statistics

class GameAgent:
    - class AgentAction(Enum): Defintes the agent actions (Move, Avoid, Stop)
    - class AgentState(Enum): Defines the agent states (Clear, Near_Agent, Blocked)
    - class GameState(Enum): Defines the game states (Acting, Goal)
    - RULE_TABLE: Maps each possible combination of AgentState and GameState to an AgentAction.
    - __init__(): Initialize with name, starting position and maze
    - neighbors_list(): Return neighbors of the agent position
    - _adjacent_agent(): Return True if a cell is adjacent to an agent, else False
    - _perceive(): Returns the number of agents within two spaces
    - _state(): Returns AgentState based on the percept
    - _rule_to_action(): Returns AgentAction for AgentState and GameState
    - pick_action(): Return AgentAction based on Agent and Game state
   
class Ghost:
    - move(): Find a valid direction to move in
    - step(): Move the agent one step

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

3. **Challenge**: Ghost evasion
   - **Solution**: Recalculate path at each step, verify path does not lead next to ghosts

## AI/LLM Usage Documentation

### Tools Used
- **ChatGPT**: Initial project setup, environment configuration
- **Claude**: Code refinement, BFS implementation, documentation
- **Gemini**: Maze generation, A* implementation, Agent rules design

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
- **Modification**: Removed driver, customized function parameters to fit within class. Used simpler pathfinding in final Ghost class to better imitate Ghost behavior.

#### Design of Agent rules and actions
- **Prompt**: "In python, what is the optimal way to design a set of rules and actions for an intelligent agent?"
- **AI Response**: Provided vacuum cleaner example, using a dictionary as a rule table with a tuple as key
- **Modification**: Customized dictionary rules to fit the game_agent class

### Validation Process
1. Tested each AI-generated function independently
2. Verified pathfinding correctness with print statements
3. Ensured proper maze boundary checking
4. Validated pellet collection and score updates

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
├── game_agent.py    # Parent class for pac-man and ghost agents
├── pacman_ai.py     # BFS pathfinding logic (Liu's work)
├── level.py         # Level maze file
├── ghost.py         # Ghost logic file
├── score_tracker.py # Score tracking system (Yogitha's work)
├── README.md        # This file
├── assets           # Folder containing game sprites
├── requirements.txt # Python dependencies
└── .venv/          # Virtual environment
```

## Conclusion
The project successfully demonstrates AI agent design using rational decision-making through a BFS search algorithm. The Pac-Man agent autonomously navigates the maze, always choosing the optimal path to collect pellets efficiently.
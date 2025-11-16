# PACMAN AI Agent - Group Project 1

## Team Members
- **Liu** - Pac-Man AI Pathfinding (BFS Algorithm)
- **Rachel** - Maze Design and Game Framework
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

### Code Structure
```python
class PacmanAI:
    - __init__(): Initialize with starting position and maze
    - bfs(): Core search algorithm
    - set_target(): Compute path to target pellet
    - step(): Move one cell along the path
```

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

### Code Structure
```python
class ScoreTracker:
    - __init__(): Initialize with total pellets and pellet value
    - eat_pellet(): Update score when pellet is eaten
    - get_score(): Retrieve current score
    - get_pellets_eaten(): Get count of eaten pellets
    - draw(): Render score and pellet info on screen
    - print_stats(): Display final game statistics
```

### Features
- **Configurable Scoring**: Pellet value can be customized (default: 10 points per pellet)
- **Real-time Updates**: Score updates immediately when pellets are collected
- **Visual Feedback**: Score and pellet count displayed prominently on screen
- **Progress Tracking**: Shows remaining pellets (e.g., "Pellets: 15/20")
- **Win Detection**: Automatically detects and displays win condition

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
- [ ] Add ghost AI (random walk or chase behavior)
- [ ] Optimize path recalculation
- [ ] Add difficulty levels
- [ ] Implement power-ups

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
├── score_tracker.py # Score tracking system (Yogitha's work)
├── README.md        # This file
├── requirements.txt # Python dependencies
└── .venv/          # Virtual environment
```

## Conclusion
The project successfully demonstrates AI agent design using rational decision-making through BFS search algorithm. The Pac-Man agent autonomously navigates the maze, always choosing the optimal path to collect pellets efficiently.
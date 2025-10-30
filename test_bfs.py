#!/usr/bin/env python3
"""
Test script for BFS algorithm
Run this to verify your pathfinding works correctly
"""

from pacman_ai import PacmanAI

def print_maze_with_path(maze, path, start, goal):
    """Visualize the maze with the path"""
    height = len(maze)
    width = len(maze[0])
    
    # Create display grid
    display = []
    for y in range(height):
        row = []
        for x in range(width):
            if maze[y][x] == 1:
                row.append('█')  # Wall
            else:
                row.append(' ')  # Open space
        display.append(row)
    
    # Mark path
    for x, y in path:
        if (x, y) != start and (x, y) != goal:
            display[y][x] = '·'
    
    # Mark start and goal
    if start:
        display[start[1]][start[0]] = 'S'
    if goal:
        display[goal[1]][goal[0]] = 'G'
    
    # Print
    print("\nMaze with Path:")
    print("=" * (width * 2 + 1))
    for row in display:
        print('|' + ''.join(row) + '|')
    print("=" * (width * 2 + 1))

def test_simple_maze():
    """Test on a simple 5x5 maze"""
    print("Testing Simple 5x5 Maze")
    print("-" * 30)
    
    # Create a simple maze (0=open, 1=wall)
    maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]
    
    start = (1, 1)
    goal = (3, 3)
    
    # Create Pac-Man AI
    pacman = PacmanAI(start, maze)
    
    # Find path
    path = pacman.bfs(start, goal)
    
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print(f"Path found: {path}")
    print(f"Path length: {len(path)} steps")
    
    print_maze_with_path(maze, path, start, goal)
    
    return len(path) > 0

def test_complex_maze():
    """Test on a more complex 10x10 maze"""
    print("\nTesting Complex 10x10 Maze")
    print("-" * 30)
    
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    start = (1, 1)
    goal = (8, 8)
    
    pacman = PacmanAI(start, maze)
    path = pacman.bfs(start, goal)
    
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print(f"Path found: {path}")
    print(f"Path length: {len(path)} steps")
    
    print_maze_with_path(maze, path, start, goal)
    
    return len(path) > 0

def test_no_path():
    """Test when no path exists"""
    print("\nTesting No Path Scenario")
    print("-" * 30)
    
    # Maze with blocked goal
    maze = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1],  # Goal is blocked
        [1, 1, 1, 1, 1]
    ]
    
    start = (1, 1)
    goal = (3, 3)  # This position is a wall!
    
    pacman = PacmanAI(start, maze)
    path = pacman.bfs(start, goal)
    
    print(f"Start: {start}")
    print(f"Goal: {goal} (blocked by wall)")
    print(f"Path found: {path}")
    print(f"Expected: Empty path []")
    
    return len(path) == 0

def run_all_tests():
    """Run all test cases"""
    print("=" * 40)
    print("BFS PATHFINDING TEST SUITE")
    print("=" * 40)
    
    tests = [
        ("Simple Maze", test_simple_maze),
        ("Complex Maze", test_complex_maze),
        ("No Path", test_no_path)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"ERROR in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("TEST RESULTS SUMMARY")
    print("=" * 40)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(passed for _, passed in results)
    print("\n" + ("All tests passed! ✓" if all_passed else "Some tests failed ✗"))
    
    return all_passed

if __name__ == "__main__":
    run_all_tests()
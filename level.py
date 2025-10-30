import pygame
"""Class containing the level's maze and tile types"""
class Level(object):
    def __init__(self):
        self.tiles = [pygame.image.load('assets/pellet.png'), pygame.image.load('assets/wall.png'), pygame.image.load('assets/empty.png')]
        self.maze = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                     [1,2,0,0,0,1,0,0,0,1,0,0,0,0,1],
                     [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
                     [1,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
                     [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
                     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                     [1,0,1,0,1,1,0,1,0,1,1,0,1,0,1],
                     [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
                     [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
                     [1,0,1,0,0,0,0,1,0,0,0,0,1,0,1],
                     [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
                     [1,0,0,0,0,1,0,0,0,1,0,0,0,0,1],
                     [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
                     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    def clear_tile(self, row, col):
        if col < len(self.maze[0]) and row < len(self.maze) and self.maze[row][col] != 1:
            self.maze[row][col] = 2
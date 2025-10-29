import pygame
import level

pygame.init()
tile_size = 32
offset = 64
window_size = width, height = 608, 608
window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
pygame.display.set_caption("PACMAN")
icon = pygame.image.load('assets/PACicon.png')
pygame.display.set_icon(icon)

font = pygame.font.Font('assets/BitCountGridSingle.ttf', 20)
test_text = font.render('TEST TEXT', True, (255, 255, 255))

level = level.Level()
pellets = sum(x.count(0) for x in level.maze)

position = [1, 1]
keep_running = True

while keep_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_running = False

    window.fill((0, 0, 0))

    #maze display
    for row in range(len(level.maze)):
        for col in range(len(level.maze[row])):
            x = (col * tile_size) + offset
            y = (row * tile_size) + offset
            window.blit(level.tiles[level.maze[row][col]], (x, y))

    #test sprites and text (delete later)
    window.blit(pygame.image.load('assets/ghost.png'), (0, 0))
    window.blit(pygame.image.load('assets/pacman.png'), ((position[0] * tile_size) + offset, (position[1] * tile_size) + offset))
    window.blit(test_text, (1 * tile_size, 0))

    pygame.display.flip()

pygame.quit()
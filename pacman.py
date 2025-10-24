import pygame

pygame.init()
window_size = width, height = 500, 500
window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
pygame.display.set_caption("PACMAN")
icon = pygame.image.load('PACicon.png')
pygame.display.set_icon(icon)

keep_running = True
while keep_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_running = False
        
    window.fill((0, 0, 0))

    pygame.display.update()

pygame.quit()
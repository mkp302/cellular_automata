import pygame
import sys

pygame.init()
window_size = (800, 800)
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

import pygame
import sys

pygame.init()
window_size = (800, 800)
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

N = 10
pallette = {"bg": (0, 0, 0), "cell_bg": (36, 107, 31), "grid-lines": (209, 203, 69)}


def draw_grid():
    outer_padding = 40
    cell_padding = 10
    grid_thickness = 2
    screen_width, screen_height = screen.get_size()
    w = screen_width - 2 * outer_padding
    h = screen_height - 2 * cell_padding
    s = min(
        (w - (N + 1) * grid_thickness - 2 * cell_padding) / N,
        (h - (N + 1) * grid_thickness - 2 * cell_padding) / N,
    )
    cell_width = s
    cell_height = s

    screen.fill(pallette["bg"])

    grid_width = N * s + (N + 1) * grid_thickness + 2 * cell_padding
    grid_height = N * s + (N + 1) * grid_thickness + 2 * cell_padding
    x0 = (screen_width - grid_width) // 2
    y0 = (screen_height - grid_height) // 2

    for i in range(N + 1):
        # vertical lines
        x = x0 + cell_padding + i * (s + grid_thickness)

        pygame.draw.rect(
            screen,
            pallette["grid-lines"],
            (x, y0 + cell_padding, grid_thickness, grid_height - 2 * cell_padding),
        )
        # horizontal lines
        y = y0 + cell_padding + i * (s + grid_thickness)
        pygame.draw.rect(
            screen,
            pallette["grid-lines"],
            (x0 + cell_padding, y, grid_width - 2 * cell_padding, grid_thickness),
        )


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_grid()
    pygame.display.flip()

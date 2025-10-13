from scenes.base_scene import BaseScene
from models.grid import Grid
import pygame


class SimulationScene(BaseScene):
    def __init__(self, context):
        self.context = context
        self.grid = Grid(17, 5, 10)

    def render(self):
        outer_padding = 5
        cell_padding = 2
        grid_thickness = 2
        screen_width = self.context.window_size[0]
        screen_height = self.context.window_size[1]

        screen = self.context.screen
        palette = self.context.palette

        hud_height = int(screen_height * 0.1)
        side_bar_width = int(screen_width * 0.2)

        hud_rect = pygame.Rect(0, 0, screen_width, hud_height)
        sidebar_rect = pygame.Rect(
            0, hud_height, side_bar_width, screen_width - hud_height
        )
        grid_rect = pygame.Rect(
            side_bar_width,
            hud_height,
            screen_width - side_bar_width,
            screen_height - hud_height,
        )

        N = self.grid.N
        w = grid_rect.width - 2 * outer_padding
        h = grid_rect.height - 2 * outer_padding
        s = min(
            (w - (N + 1) * grid_thickness - 2 * cell_padding) / N,
            (h - (N + 1) * grid_thickness - 2 * cell_padding) / N,
        )
        screen.fill(palette["bg"])
        pygame.draw.rect(screen, (255, 0, 0), sidebar_rect)
        pygame.draw.rect(screen, (0, 255, 0), hud_rect)
        grid_width = N * s + (N + 1) * grid_thickness + 2 * cell_padding
        grid_height = N * s + (N + 1) * grid_thickness + 2 * cell_padding
        x0 = grid_rect.left + (screen_width - grid_width - grid_rect.left) // 2
        y0 = grid_rect.top + (screen_height - grid_height - grid_rect.top) // 2

        for i in range(N + 1):
            # vertical lines
            x = x0 + cell_padding + i * (s + grid_thickness)
            y = y0 + cell_padding + i * (s + grid_thickness)

            pygame.draw.rect(
                screen,
                palette["grid-lines"],
                (x, y0 + cell_padding, grid_thickness, grid_height - 2 * cell_padding),
            )
            # horizontal lines
            pygame.draw.rect(
                screen,
                palette["grid-lines"],
                (x0 + cell_padding, y, grid_width - 2 * cell_padding, grid_thickness),
            )

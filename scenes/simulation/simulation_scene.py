from scenes.base_scene import BaseScene
from models.grid import Grid
from scenes.worldmap.world_map_scene import WorldMapScene
from models.enviroment import Enviroment
from scenes.simulation.sidebar import Sidebar
import pygame
import pygame_gui
import math
import random


class SimulationScene(BaseScene):
    def __init__(self, context):
        self.context = context
        self.grid = Grid(17, 5, 10)
        self.enviroment = Enviroment()
        self.dragging_wind = False
        self.sidebar = Sidebar(self.context, self.enviroment, self.grid)
        self.tree_img = pygame.image.load("assets/tree.png").convert_alpha()
        self.tree_img_2 = pygame.image.load("assets/2tree.png").convert_alpha()
        self.tree_img_3 = pygame.image.load("assets/3tree.png").convert_alpha()

    def draw_grid(self):
        outer_padding = 5
        cell_padding = 2
        grid_thickness = 2
        screen = self.context.screen
        screen_width = screen.width
        screen_height = screen.height

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

        for row in range(N):
            for col in range(N):
                x = x0 + cell_padding + grid_thickness + col * (s + grid_thickness)
                y = y0 + cell_padding + grid_thickness + row * (s + grid_thickness)
                self.draw_cell(self.grid.cells[row + 1][col + 1], x, y, s)

    def draw_cell(self, cell, x, y, s):
        surface = self.context.screen
        if cell.burning == 3:
            pygame.draw.rect(self.context.screen, (0, 0, 0), (x, y, s, s))
            return

        pygame.draw.rect(
            self.context.screen, self.context.palette["cell_bg"], (x, y, s, s)
        )

        if cell.tree_density > 0.75:
            tree_scaled = pygame.transform.smoothscale(self.tree_img, (s, s))
            surface.blit(tree_scaled, (x, y))
        elif cell.tree_density > 0.50:
            tree_scaled_2 = pygame.transform.smoothscale(self.tree_img_2, (s, s))
            surface.blit(tree_scaled_2, (x, y))
        elif cell.tree_density > 0.25:
            tree_scaled_3 = pygame.transform.smoothscale(self.tree_img_3, (s, s))
            surface.blit(tree_scaled_3, (x, y))
        if cell.burning == 2:
            rect = pygame.Rect(x, y, s, s)
            self.draw_flame_overlay(
                self.context.screen, rect, self.enviroment.wind_speed
            )

    def draw_flame_overlay(
        self, surface, cell_rect, wind=(0.0, 0.0), intensity=1.0, t=0
    ):

        flame_height = int(cell_rect.height * 0.9 * intensity)
        base_width = cell_rect.width * 0.4
        shear = wind[0] * 0.5  # wind shear strength
        cx = cell_rect.x + cell_rect.width // 2
        cy = cell_rect.y + cell_rect.height - 5  # base of the flame

        flame_surf = pygame.Surface(
            (cell_rect.width, cell_rect.height), pygame.SRCALPHA
        )

        points = []
        num_segments = 20

        for i in range(num_segments + 1):
            y = cell_rect.height - (i / num_segments) * flame_height
            flicker = random.uniform(-3, 3)
            x_offset = flicker + shear * (cell_rect.height - y)
            width_factor = 1 - i / num_segments
            x = cell_rect.width / 2 - base_width * width_factor / 2 + x_offset
            points.append((x, y))

        for i in range(num_segments, -1, -1):
            y = cell_rect.height - (i / num_segments) * flame_height
            flicker = random.uniform(-3, 3)
            x_offset = flicker + shear * (cell_rect.height - y)
            width_factor = 1 - i / num_segments
            x = cell_rect.width / 2 + base_width * width_factor / 2 + x_offset
            points.append((x, y))

        # Gradient fill — bottom to top (yellow → orange → red → transparent)
        gradient_colors = [
            (180, 50, 10, 180),
            (255, 100, 20, 160),
            (255, 180, 50, 120),
            (255, 255, 100, 60),
            # (100, 20, 5, 0),
        ]

        # Draw layered gradient polygons for smooth fade
        for i, color in enumerate(gradient_colors):
            scale = 1 - (i / len(gradient_colors)) * 0.5
            scaled_points = [
                (
                    x * scale + (1 - scale) * cell_rect.width / 2,
                    y * scale + (1 - scale) * cell_rect.height / 2,
                )
                for x, y in points
            ]
            pygame.draw.polygon(flame_surf, color, scaled_points)

        # Blit to main surface with alpha
        surface.blit(
            flame_surf,
            (cell_rect.x, cell_rect.y),
            special_flags=pygame.BLEND_PREMULTIPLIED,
        )

    def render(self):
        self.draw_grid()
        self.sidebar.render()

    def handle(self, event):
        self.sidebar.handle(event)

    def update(self):
        self.grid.update_cells()

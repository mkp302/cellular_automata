from scenes.base_scene import BaseScene
from models.grid import Grid
from scenes.worldmap.world_map_scene import WorldMapScene
from models.enviroment import Enviroment
from scenes.simulation.sidebar import Sidebar
import pygame
from datetime import timedelta
import matplotlib.pyplot as plt


class SimulationScene(BaseScene):
    def __init__(self, context):
        self.context = context
        self.grid = Grid(300, 5, 10)
        self.enviroment = Enviroment()
        self.dragging_wind = False
        self.sidebar = Sidebar(self.context, self.enviroment, self.grid)
        self.tree_img = pygame.image.load("assets/tree.png").convert_alpha()
        self.tree_img_2 = pygame.image.load("assets/2tree.png").convert_alpha()
        self.tree_img_3 = pygame.image.load("assets/3tree.png").convert_alpha()

    def draw_grid(self):
        outer_padding = 0
        cell_padding = 0
        grid_thickness = 0
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
        s = h // N
        screen.fill(palette["bg"])
        # grid_width = N * s + (N + 1) * grid_thickness + 2 * cell_padding
        # grid_height = N * s + (N + 1) * grid_thickness + 2 * cell_padding
        x0 = grid_rect.left + 100  # + (screen_width - grid_width - grid_rect.left) // 2
        y0 = grid_rect.top  # + (screen_height - grid_height - grid_rect.top) // 2

        for row in range(N):
            for col in range(N):
                x = x0 + col * s
                y = y0 + cell_padding + row * s
                self.draw_cell(self.grid.cells[row + 1][col + 1], x, y, s)

    def draw_cell(self, cell, x, y, s):
        # color = plt.cm.terrain
        surface = self.context.screen
        if cell.burning == 3:
            pygame.draw.rect(self.context.screen, (0, 0, 0), (x, y, s, s))
            return

        if cell.burning == 0:
            pygame.draw.rect(self.context.screen, (0, 0, 255), (x, y, s, s))
            return
        # r, g, b, a = color(cell.elevation / 255)
        pygame.draw.rect(
            self.context.screen, self.context.palette["cell_bg"], (x, y, s, s)
        )

        if cell.burning == 2:
            pygame.draw.rect(self.context.screen, (255, 0, 0), (x, y, s, s))

    def render(self):
        self.draw_grid()
        self.sidebar.render()

    def handle(self, event):
        self.sidebar.handle(event)

    def update(self):
        self.context.sim_time += timedelta(minutes=30)
        self.enviroment.update(self.context.sim_time)

        self.grid.update_cells(
            self.enviroment.wind_speed,
            self.enviroment.temperature,
            self.enviroment.humidity,
        )
        self.sidebar.update()

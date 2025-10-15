from scenes.base_scene import BaseScene
from models.grid import Grid
from scenes.worldmap.world_map_scene import WorldMapScene
from models.enviroment import Enviroment
import pygame
import pygame_gui
import math


def angle_to_vector(theta):
    return math.cos(theta), math.sin(theta)


def update_wind_from_mouse(mouse_pos, arrow_center):
    mx, my = mouse_pos
    cx, cy = arrow_center
    angle = math.atan2(my - cy, mx - cx)
    return angle, angle_to_vector(angle)


class SimulationScene(BaseScene):
    def __init__(self, context):
        self.context = context
        self.grid = Grid(17, 5, 10)
        self.manager = pygame_gui.UIManager(context.screen.get_size())
        self.compass_img = pygame.image.load("assets/compass.png").convert_alpha()
        self.enviroment = Enviroment()
        self.dragging_wind = False

    def draw_grid(self): ...
    def draw_cell(self): ...
    def draw_wind_arrow(self, surface, center, angle, length=60, color=(0, 0, 0)):

        x, y = center
        end_x = x + math.cos(angle) * length
        end_y = y + math.sin(angle) * length
        pygame.draw.line(surface, color, (x, y), (end_x, end_y), 4)
        # arrowhead
        left = (
            end_x - 10 * math.cos(angle - math.pi / 6),
            end_y - 10 * math.sin(angle - math.pi / 6),
        )
        right = (
            end_x - 10 * math.cos(angle + math.pi / 6),
            end_y - 10 * math.sin(angle + math.pi / 6),
        )
        pygame.draw.polygon(surface, color, [(end_x, end_y), left, right])

    def draw_sidebar(self, rect):
        compass_label = pygame_gui.elements.UITextBox(
            html_text="Wind",
            relative_rect=rect,
            manager=self.manager,
        )

        randomize_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(30, 20, 100, 20),
            text="Randomize",
            manager=self.manager,
        )
        self.manager.draw_ui(self.context.screen)
        self.manager.update(10)
        compass = pygame.transform.smoothscale(
            self.compass_img, (rect.width, rect.width)
        )
        self.context.screen.blit(compass, (0, rect.top + 40))
        self.draw_wind_arrow(
            self.context.screen,
            (rect.width // 2, rect.width + 40),
            self.enviroment.wind_angle,
        )

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
        self.draw_sidebar(sidebar_rect)

    def handle(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.mod == pygame.KMOD_NONE:
                print(
                    "No modifier keys were in a pressed state when this event occurred."
                )
                world_map = WorldMapScene(self.context)
                self.context.scene_manager.push(world_map)
            else:
                if event.mod & pygame.KMOD_LSHIFT:
                    print("Left shift was in a pressed state when this event occurred.")
                if event.mod & pygame.KMOD_RSHIFT:
                    print(
                        "Right shift was in a pressed state when this event occurred."
                    )
                if event.mod & pygame.KMOD_SHIFT:
                    print(
                        "Left shift or right shift or both were in a pressed state when this event occurred."
                    )
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dragging_wind = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_wind = False

        if self.dragging_wind:
            pos = pygame.mouse.get_pos()
            self.enviroment.wind_angle, self.enviroment.wind_speed = (
                update_wind_from_mouse(pos, (100, 100))
            )

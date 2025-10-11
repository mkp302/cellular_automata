import pygame
import pygame_gui
import sys

pygame.init()
window_size = (800, 800)
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

hud_height = int(window_size[1] * 0.2)
side_bar_width = int(window_size[0] * 0.2)

hud_rect = pygame.Rect(0, 0, window_size[0], hud_height)
sidebar_rect = pygame.Rect(0, hud_height, side_bar_width, window_size[0] - hud_height)
grid_rect = pygame.Rect(
    side_bar_width,
    hud_height,
    window_size[0] - side_bar_width,
    window_size[1] - hud_height,
)

manager = pygame_gui.UIManager(window_size)

N = 10
pallette = {"bg": (0, 0, 0), "cell_bg": (36, 107, 31), "grid-lines": (209, 203, 69)}
hello_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(30, 20, 100, 20), text="Say Hello", manager=manager
)


def calc_region_sizes():
    window_size = screen.get_size()
    hud_height = int(window_size[1] * 0.2)
    side_bar_width = int(window_size[0] * 0.2)

    hud_rect = pygame.Rect(0, 0, window_size[0], hud_height)
    sidebar_rect = pygame.Rect(
        0, hud_height, side_bar_width, window_size[0] - hud_height
    )
    grid_rect = pygame.Rect(
        side_bar_width,
        hud_height,
        window_size[0] - side_bar_width,
        window_size[1] - hud_height,
    )
    return hud_rect, sidebar_rect, grid_rect


def draw_grid(region):
    outer_padding = 5
    cell_padding = 2
    grid_thickness = 2
    screen_width = region.width
    screen_height = region.height
    w = screen_width - 2 * outer_padding
    h = screen_height - 2 * outer_padding
    s = min(
        (w - (N + 1) * grid_thickness - 2 * cell_padding) / N,
        (h - (N + 1) * grid_thickness - 2 * cell_padding) / N,
    )
    cell_width = s
    cell_height = s
    screen.fill(pallette["bg"])
    pygame.draw.rect(screen, (255, 0, 0), sidebar_rect)
    pygame.draw.rect(screen, (0, 255, 0), hud_rect)
    grid_width = N * s + (N + 1) * grid_thickness + 2 * cell_padding
    grid_height = N * s + (N + 1) * grid_thickness + 2 * cell_padding
    x0 = (screen_width - grid_width) // 2 + region.left
    y0 = (screen_height - grid_height) // 2 + region.top

    for i in range(N + 1):
        # vertical lines
        x = x0 + cell_padding + i * (s + grid_thickness)
        y = y0 + cell_padding + i * (s + grid_thickness)

        pygame.draw.rect(
            screen,
            pallette["grid-lines"],
            (x, y0 + cell_padding, grid_thickness, grid_height - 2 * cell_padding),
        )
        # horizontal lines
        pygame.draw.rect(
            screen,
            pallette["grid-lines"],
            (x0 + cell_padding, y, grid_width - 2 * cell_padding, grid_thickness),
        )

    # for row in range(N):
    # for col in range(N):

    # x = x0 + cell_padding + grid_thickness + col * (s + grid_thickness)
    # y = y0 + cell_padding + grid_thickness + row * (s + grid_thickness)
    # pygame.draw.rect(screen, pallette["cell_bg"], (x, y, s, s))


print(grid_rect.top)
print(grid_rect.left)
clock = pygame.time.Clock()
while True:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            print("resize")
            hud_rect, sidebar_rect, grid_rect = calc_region_sizes()
            print(grid_rect)
        manager.process_events(event)
    manager.update(time_delta)

    draw_grid(grid_rect)
    manager.draw_ui(screen)
    pygame.display.flip()

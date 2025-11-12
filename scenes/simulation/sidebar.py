import math
import pygame
import pygame_gui


def angle_to_vector(theta):
    return math.cos(theta), -1 * math.sin(theta)


def update_wind_from_mouse(mouse_pos, arrow_center):
    mx, my = mouse_pos
    cx, cy = arrow_center
    angle = math.atan2(my - cy, mx - cx)
    return angle, angle_to_vector(angle)


def draw_wind_arrow(surface, center, angle, length=100, color=(0, 0, 0)):

    x, y = center
    end_x = x + math.cos(angle) * length
    end_y =  y - math.sin(angle) * length
    pygame.draw.line(surface, color, (x, y), (end_x, end_y), 4)

    left = (
        end_x - 10 * math.cos(angle - math.pi / 6),
        end_y + 10 * math.sin(angle - math.pi / 6),
    )
    right = (
        end_x - 10 * math.cos(angle + math.pi / 6),
        end_y + 10 * math.sin(angle + math.pi / 6),
    )
    pygame.draw.polygon(surface, color, [(end_x, end_y), left, right])


class Sidebar:

    def __init__(self, context, environment, grid):
        self.context = context
        self.grid = grid
        self.manager = self.context.ui_manager
        self.compass_img = pygame.image.load("assets/compass.png").convert_alpha()
        self.environment = environment
        self.dragging_wind = False
        self.create_elements()

    def create_elements(self):

        window_size = self.context.screen.get_size()
        sidebar_top = int(window_size[1] * 0.1)
        sidebar_width = int(window_size[0] * 0.2)
        sidebar_rect = pygame.Rect(
            0, sidebar_top, sidebar_width, window_size[1] - sidebar_top
        )

        x = 0
        y = sidebar_top
        y_padding = 20

        self.compass_label = pygame_gui.elements.UITextBox(
            html_text="Wind",
            relative_rect=pygame.Rect(0, sidebar_top, sidebar_width, 40),
            manager=self.manager,
        )
        y += 40 + y_padding
        self.compass = pygame.transform.smoothscale(
            self.compass_img, (sidebar_rect.width, sidebar_rect.width)
        )
        self.compass_rect = pygame.Rect(0, y, sidebar_width, sidebar_width)
        print("Compass Rect")
        print(self.compass_rect)
        print("Center")
        print(self.compass_rect.center)
        print(self.compass.get_size())

        y += sidebar_rect.width + y_padding
        input_width = sidebar_width // 2
        label_height = 30
        self.time_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, 0), (400, label_height)),
            text=f"{self.context.sim_time.strftime("%B %d, %Y %I:%M %p")}",
            manager=self.manager,
        )

        self.wind_x_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x, y), (40, label_height)),
            text="X:",
            manager=self.manager,
        )
        self.wind_x_input = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x + 45, y), (input_width - 45, label_height)),
            text=f"{self.environment.wind_speed[0]}",
            manager=self.manager,
        )

        self.wind_y_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x + input_width, y), (40, label_height)),
            text="Y:",
            manager=self.manager,
        )
        self.wind_y_input = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (x + input_width + 45, y), (input_width - 45, label_height)
            ),
            text=f"{self.environment.wind_speed[0]}",
            manager=self.manager,
        )
        y += label_height + y_padding
        self.temp_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x, y), (80, label_height)),
            text="Temp:",
            manager=self.manager,
        )
        self.temp_input = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x + 85, y), (sidebar_width - 85, label_height)),
            text=f"{self.environment.temperature} °C",
            manager=self.manager,
        )

        y += label_height + y_padding
        self.humid_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x, y), (100, label_height)),
            text="Dew Point :",
            manager=self.manager,
        )
        self.humid_input = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (x + 105, y), (sidebar_width - 105, label_height)
            ),
            text = f"{self.environment.dew_point}",
            manager=self.manager,
        )
        y += label_height + y_padding
        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((x, y), (100, label_height)),
            text="speed:",
            manager=self.manager,
        )
        self.speed_input = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (x + 105, y), (sidebar_width - 105, label_height)
            ),
            manager=self.manager,
            start_value=0,
            value_range=(0, 100),
        )

        y += label_height + y_padding
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y), (sidebar_width, 40)),
            text="Play",
            manager=self.manager,
        )

        y += label_height + y_padding
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((x, y), (sidebar_width, 40)),
            text="Reset",
            manager=self.manager,
        )

    def render(self):
        window_size = self.context.screen.get_size()
        sidebar_top = int(window_size[1] * 0.1)
        sidebar_width = int(window_size[0] * 0.2)

        sidebar_rect = pygame.Rect(
            0, sidebar_top, sidebar_width, window_size[1] - sidebar_top
        )
        self.manager.draw_ui(self.context.screen)
        self.manager.update(10)
        self.context.screen.blit(self.compass, (0, self.compass_rect.top))
        draw_wind_arrow(
            self.context.screen,
            self.compass_rect.center,
            self.environment.wind_angle,
        )
    def update(self):
        self.time_label.set_text(f"{self.context.sim_time.strftime("%B %d, %Y %I:%M %p")}")
        self.wind_x_input.set_text(f"{self.environment.wind_speed[0]:.2f}")
        self.wind_y_input.set_text(f"{self.environment.wind_speed[1]:.2f}")
        self.temp_input.set_text(f"{self.environment.temperature:.2f} °C")
        self.humid_input.set_text(f"{self.environment.dew_point:.2f} °C")

    def handle(self, event):
     
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.reset_button:
                self.grid.reset()
            if event.ui_element == self.play_button:
                if self.context.running == False:
                    self.play_button.set_text("Pause")
                    self.context.running = True
                else:
                    self.play_button.set_text("Play")
                    self.context.running = False
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.speed_input:
                    try:
                        speed = event.value
                        if speed >= 100:
                            self.context.speed = 1
                        elif speed <= 0:
                            self.context.speed = 100
                        else:
                            self.context.speed = 100 - speed
                    except:
                        ...
    

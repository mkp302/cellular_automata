from config import Config
import pygame


class Context:
    def __init__(self):
        self.config = Config("config.json")
        self.config.load()
        width = self.config.get("window", "width", default=800)
        height = self.config.get("window", "height", default=800)
        self.window_size = (width, height)
        self.running = True
        self.current_scene = None
        self.palette = {
            "bg": (0, 0, 0),
            "cell_bg": (36, 107, 31),
            "grid-lines": (209, 203, 69),
        }
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

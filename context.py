from config import Config
from scenes.scene_manager import SceneManager
from scenes.simulation.simulation_scene import SimulationScene
import pygame
import pygame_gui
import xarray


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
        self.screen = pygame.display.set_mode(self.window_size)
        self.ui_manager = pygame_gui.UIManager(self.screen.get_size())
        sim_scene = SimulationScene(self)
        self.scene_manager = SceneManager()
        self.scene_manager.push(sim_scene)
        self.grid = None

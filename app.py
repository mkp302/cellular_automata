import pygame

# import pygame_gui
import sys
from context import Context
from scenes.scene_manager import SceneManager
from scenes.simulation.simulation_scene import SimulationScene


def main():
    pygame.init()
    context = Context()
    scene_manager = SceneManager(SimulationScene(context))
    window_size = context.window_size
    print(window_size)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        scene_manager.top().render()
        pygame.display.flip()


main()

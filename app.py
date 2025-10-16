import pygame

# import pygame_gui
import sys
from context import Context
from scenes.simulation.simulation_scene import SimulationScene


def main():
    pygame.init()
    context = Context()
    scene_manager = context.scene_manager
    window_size = context.screen.get_size()
    print(window_size)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                window_size = context.screen.get_size()
                context.window_size = window_size
            scene_manager.top().handle(event)
            context.ui_manager.process_events(event)

        scene_manager.top().render()
        pygame.display.flip()


main()

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
    t = 0
    loop = 0
    pygame.display.set_caption("Forest Fire Cellular Automata")
    while True:
        time_delta = clock.tick(60) / 1000.0
        t += time_delta
        loop += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            scene_manager.top().handle(event)
            context.ui_manager.process_events(event)

        context.ui_manager.update(time_delta)
        if context.running and loop % context.speed == 0:
            scene_manager.top().update()

        scene_manager.top().render()
        pygame.display.flip()


main()

from scenes.base_scene import BaseScene
import pygame


class WorldMapScene(BaseScene):
    def __init__(self, context):
        self.context = context

    def render(self):
        self.context.screen.fill((255, 0, 0))

    def handle(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.mod == pygame.KMOD_NONE:
                print(
                    "No modifier keys were in a pressed state when this event occurred."
                )
                self.context.scene_manager.pop()
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

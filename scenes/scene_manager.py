class SceneManager:
    def __init__(self, scene):
        self.scene_stack = []
        self.scene_stack.append(scene)

    def push(self, scene): ...
    def pop(self): ...
    def top(self):
        if len(self.scene_stack) > 0:
            return self.scene_stack[-1]

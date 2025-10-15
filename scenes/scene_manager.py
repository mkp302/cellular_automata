class SceneManager:
    def __init__(self):
        self.scene_stack = []

    def push(self, scene):
        self.scene_stack.append(scene)

    def pop(self):
        return self.scene_stack.pop()

    def top(self):
        if len(self.scene_stack) > 0:
            return self.scene_stack[-1]

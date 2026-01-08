from abc import ABC


class Component(ABC):
    def __init__(self):
        self.game_object = None

    def update(self, dt):
        pass

    def on_added(self):
        pass

    def draw(self, screen):
        pass

    def event_handler(self, event):
        pass

    def kill(self):
        pass

    def get_component(self, component_type):
        if self.game_object:
            return self.game_object.get_component(component_type)
        return None

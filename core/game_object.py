from typing import Optional

from core.component import Component


class GameObject:
    instances = None

    def __init__(self, components: Optional[list[Component]]=None):
        self.children: list[GameObject] = []
        self.parent: GameObject | None = None
        self.components = []

        if GameObject.instances is None:
            GameObject.instances = []
        GameObject.instances.append(self)

        if components is not None:
            for component in components:
                self.add_component(component)

    def add_child(self, child: "GameObject"):
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: "GameObject"):
        self.children.remove(child)
        child.parent = None

    def add_component(self, component: Component):
        component.game_object = self
        self.components.append(component)

        if hasattr(component, "on_added") and callable(component.on_added):
            component.on_added()

        return component

    def init_components(self):
        for component in self.components:
            if hasattr(component, "on_added") and callable(component.on_added):
                component.on_added()

    def get_component(self, component_type):
        for c in self.components:
            if isinstance(c, component_type):
                return c
        return None

    def update(self, dt):
        for c in self.components:
            if hasattr(c, "update"):
                c.update(dt)

        for child in self.children:
            if hasattr(child, "update"):
                child.update(dt)

    def draw(self, screen):
        for c in self.components:
            if hasattr(c, "draw"):
                c.draw(screen)

        for child in self.children:
            if hasattr(child, "draw"):
                child.draw(screen)

    def event_handler(self, event):
        for c in self.components:
            if hasattr(c, "event_handler"):
                c.event_handler(event)

        for child in self.children:
            if hasattr(child, "event_handler"):
                child.event_handler(event)

    def kill(self):
        # сначала дети
        for child in self.children[:]:
            child.kill()

        # компоненты
        for c in self.components:
            if hasattr(c, "kill"):
                c.kill()
        self.components.clear()

        # убрать из parent
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

        # убрать из instances
        if self in GameObject.instances:
            GameObject.instances.remove(self)

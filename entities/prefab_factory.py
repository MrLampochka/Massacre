from components.ai_control import AIControl
from components.bar import Bar
from components.boundary import BoundaryClamp, BoundaryKill
from components.collision import Collision
from components.health import Health
from components.movement import Movement
from components.player_control import PlayerControl
from components.sprite import Sprite
from components.transform import Transform
from components.weapon import Weapon
from core.game_object import GameObject
from core.utils import merge_dicts

COMPONENT_REGISTRY = {
    "health": Health,
    "bar": Bar,
    "weapon": Weapon,
    "movement": Movement,
    "transform": Transform,
    "sprite": Sprite,
    "player_control": PlayerControl,
    "ai_control": AIControl,
    "health_bar": Bar,
    "reload_bar": Bar,
    "collision": Collision,
    "boundary_clamp": BoundaryClamp,
    "boundary_kill": BoundaryKill,
}

class PrefabFactory:
    def __init__(self, context, prefabs):
        self.context = context
        self.prefabs = prefabs

    def spawn(self, name, **overrides):
        if name is None:
            raise ValueError("Prefab name is None")
        cfg = merge_dicts(self._resolve_prefab(name), overrides)

        entity = GameObject()

        for comp_name, comp_cfg in cfg.get("components", {}).items():
            self._create_component(entity, comp_name, comp_cfg)

        entity.init_components()
        return entity

    def _resolve_prefab(self, name, chain=None):
        if name is None:
            raise ValueError("Prefab name is None")
        chain = chain or []
        if name in chain:
            raise ValueError(f"Circular prefab extends detected: {' -> '.join(chain + [name])}")
        if name not in self.prefabs:
            raise KeyError(f"Prefab '{name}' not found")

        cfg = self.prefabs[name]
        parents = cfg.get("extends")

        base_cfg = {}
        if parents:
            parents_list = parents if isinstance(parents, (list, tuple)) else [parents]
            for parent_name in parents_list:
                parent_cfg = self._resolve_prefab(parent_name, chain + [name])
                base_cfg = merge_dicts(base_cfg, parent_cfg)

        cfg_without_extends = {k: v for k, v in cfg.items() if k != "extends"}
        return merge_dicts(base_cfg, cfg_without_extends)

    def _create_component(self, entity, name, cfg):
         if cfg is None:
             return
         if cls := COMPONENT_REGISTRY.get(name):
             entity.add_component(cls(context=self.context, **cfg.copy()))
         else:
             raise Exception(f"Unknown component {name}")

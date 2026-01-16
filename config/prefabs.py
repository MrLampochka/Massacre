import pygame as pg

image = pg.Surface((10, 10), pg.SRCALPHA)
pg.draw.circle(image, (0, 255, 0), (5, 5), 5)

PREFABS = {
    "default": {
        "name": "Default Unit",
        "cost": 50,
        "kind": "controlled_unit",
        "components": {
            "health": {
                "value": 100,
                "dying_time": 1,
                "dying_speed": -50,
                "dying_direction": pg.Vector2(0, 1),
            },
            "player_control": {
                "left_btn_cb": None,
                "right_btn_cb": None,
                "left_btn_hold_cb": None,
                "right_btn_hold_cb": None,
            },
            "weapon": {
                "reload_time": 0.1,
                "collision_list": [],
                "attack": {
                    "type": "projectile",
                    "spread": 0,
                    "bullet_name": "bullet",
                    "damage": 25,
                },
            },
            "transform": {
                "scale": None,
                "pos": None,
                "rotation": 0,
            },
            "movement": {
                "speed": 500,
                "velocity": None,
                "direction": None,
            },
            "sprite": {"image": None, "size": (32, 32), "color": "purple"},
            "reload_bar": {
                "bg_color": (64, 64, 64),
                "color": "orange",
                "source": "weapon",
                "size": (20, 5),
                "offset": pg.Vector2(0, -25),
                "rev": True,
            },
            "health_bar": {
                "bg_color": (64, 64, 64),
                "source": "health",
                "rev": False,
                "color": "green",
                "size": (20, 5),
                "offset": pg.Vector2(0, -30),
            },
            "boundary_clamp": {"padding": 0},
        },
    },
    "bullet": {
        "name": "Default Unit",
        "cost": 50,
        "kind": "projectile",
        "components": {
            "transform": {
                "scale": None,
                "pos": None,
                "rotation": 0,
            },
            "movement": {
                "speed": 500,
                "velocity": None,
                "direction": None,
            },
            "sprite": {"image": image, "size": (8, 8), "color": "blue"},
            "boundary_kill": {"padding": 50},
            "collision": {
                "collision_list": [],
                "on_collision": None,
                "kill_self": True,
                "first_only": True,
            },
        },
    },
    "tower": {
        "extends": "default",
        "name": "Default Unit",
        "cost": 50,
        "kind": "building",
        "components": {
            "ai_control": {
                "detect_radius": 500,
                "attack_radius": 500,
                "search_time": 0.2,
                "default_direction": pg.Vector2(0, 0),
            },
            "transform": {
                "scale": None,
                "pos": None,
                "rotation": 0,
            },
            "sprite": {"image": None, "size": (32, 32), "color": "orange"},
            "reload_bar": {
                "bg_color": (64, 64, 64),
                "color": "orange",
                "source": "weapon",
                "size": (20, 5),
                "offset": pg.Vector2(0, -25),
                "rev": True,
            },
            "health_bar": {
                "bg_color": (64, 64, 64),
                "source": "health",
                "rev": False,
                "color": "green",
                "size": (20, 5),
                "offset": pg.Vector2(0, -30),
            },
            "boundary_clamp": {"padding": 0},
            "player_control": None,
            "movement": None,
        },
    },
    "warrior": {
        "name": "Soldier",
        "kind": "unit",
        "cost": 5,
        "components": {
            "health": {
                "value": 100,
                "dying_time": 1,
                "dying_speed": -50,
                "dying_direction": pg.Vector2(0, 1),
            },
            "weapon": {
                "reload_time": 0.4,
                "attack": {
                    "type": "projectile",
                    "spread": 15,
                    "bullet_name": "bullet",
                    "damage": 5,
                },
            },
            "transform": {
                "scale": None,
                "pos": None,
                "rotation": 0,
            },
            "movement": {
                "speed": 200,
                "velocity": None,
                "direction": None,
            },
            "sprite": {"image": None, "size": (32, 32), "color": "purple"},
            "reload_bar": {
                "bg_color": (64, 64, 64),
                "color": "orange",
                "source": "weapon",
                "size": (20, 5),
                "offset": pg.Vector2(0, -25),
                "rev": True,
            },
            "health_bar": {
                "bg_color": (64, 64, 64),
                "source": "health",
                "rev": False,
                "color": "green",
                "size": (20, 5),
                "offset": pg.Vector2(0, -30),
            },
            "boundary_clamp": {"padding": 0},
            "ai_control": {
                "detect_radius": 400,
                "attack_radius": 200,
                "search_time": 0.1,
                "default_direction": pg.Vector2(0, 0),
            },
        },
    },
    "sniper": {
        "name": "Sniper",
        "kind": "unit",
        "cost": 10,
        "components": {
            "health": {
                "value": 100,
                "dying_time": 1,
                "dying_speed": -50,
                "dying_direction": pg.Vector2(0, 1),
            },
            "weapon": {
                "reload_time": 2,
                "attack": {
                    "type": "ray",
                    "spread": 0,
                    "damage": 25,
                    "ray_length": 400,
                    "ray_width": 4,
                    "ray_draw_time": 0.5,
                    "ray_color": (255, 0, 0),
                },
            },
            "transform": {
                "scale": None,
                "pos": None,
                "rotation": 0,
            },
            "movement": {
                "speed": 200,
                "velocity": None,
                "direction": None,
            },
            "sprite": {"image": None, "size": (32, 32), "color": "purple"},
            "reload_bar": {
                "bg_color": (64, 64, 64),
                "color": "orange",
                "source": "weapon",
                "size": (20, 5),
                "offset": pg.Vector2(0, -25),
                "rev": True,
            },
            "health_bar": {
                "bg_color": (64, 64, 64),
                "source": "health",
                "rev": False,
                "color": "green",
                "size": (20, 5),
                "offset": pg.Vector2(0, -30),
            },
            "boundary_clamp": {"padding": 0},
            "ai_control": {
                "detect_radius": 400,
                "attack_radius": 200,
                "search_time": 0.1,
                "default_direction": pg.Vector2(0, 0),
            },
        },
    },
    "tank": {
        "name": "Tank",
        "kind": "unit",
        "cost": 100,
        "components": {
            "health": {
                "value": 500,
                "dying_time": 1,
                "dying_speed": -50,
                "dying_direction": pg.Vector2(0, 1),
            },
            "weapon": {
                "reload_time": 5,
                "attack": {
                    "bullet_name": "bullet",
                    "type": "explosive",
                    "spread": 0,
                    "damage": 100,
                    "explosion_radius": 150,
                },
            },
            "transform": {
                "scale": None,
                "pos": None,
                "rotation": 0,
            },
            "movement": {
                "speed": 50,
                "velocity": None,
                "direction": None,
            },
            "sprite": {"image": None, "size": (32, 32), "color": "purple"},
            "reload_bar": {
                "bg_color": (64, 64, 64),
                "color": "orange",
                "source": "weapon",
                "size": (20, 5),
                "offset": pg.Vector2(0, -25),
                "rev": True,
            },
            "health_bar": {
                "bg_color": (64, 64, 64),
                "source": "health",
                "rev": False,
                "color": "green",
                "size": (20, 5),
                "offset": pg.Vector2(0, -30),
            },
            "boundary_clamp": {"padding": 0},
            "ai_control": {
                "detect_radius": 400,
                "attack_radius": 200,
                "search_time": 0.1,
                "default_direction": pg.Vector2(0, 0),
            },
        },
    },
    "brawler": {
        "name": "Brawler",
        "kind": "unit",
        "cost": 10,
        "components": {
            "health": {
                "value": 100,
                "dying_time": 1,
                "dying_speed": -50,
                "dying_direction": pg.Vector2(0, 1),
            },
            "weapon": {
                "reload_time": 0.8,
                "attack": {
                    "type": "melee",
                    "spread": 0,
                    "damage": 25,
                    "attack_radius": 15,
                },
            },
            "transform": {
                "scale": None,
                "pos": None,
                "rotation": 0,
            },
            "movement": {
                "speed": 200,
                "velocity": None,
                "direction": None,
            },
            "sprite": {"image": None, "size": (32, 32), "color": "purple"},
            "reload_bar": {
                "bg_color": (64, 64, 64),
                "color": "orange",
                "source": "weapon",
                "size": (20, 5),
                "offset": pg.Vector2(0, -25),
                "rev": True,
            },
            "health_bar": {
                "bg_color": (64, 64, 64),
                "source": "health",
                "rev": False,
                "color": "green",
                "size": (20, 5),
                "offset": pg.Vector2(0, -30),
            },
            "boundary_clamp": {"padding": 0},
            "ai_control": {
                "detect_radius": 400,
                "attack_radius": 15,
                "search_time": 0.1,
                "default_direction": pg.Vector2(0, 0),
            },
        },
    },
}


def unit_prefabs_sorted(max_count=None):
    units = [{name: cfg} for name, cfg in PREFABS.items() if cfg.get("kind") == "unit"]
    sorted_units = sorted(
        units, key=lambda item: list(item.values())[0].get("cost", float("inf"))
    )
    return sorted_units[:max_count] if max_count is not None else sorted_units

# Настройка экрана
from core.unit import Warrior, Shooter, HeavyShooter

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1400, 800)
FULLSCREEN_SIZE = 1920, 1080
FULLSCREEN = False
SCREEN_FILL = "gray"
WINDOW_CAPTION = 'Game'
GUI_PADDING = 25
FPS = 120

# Звуки
PUNCH_SOUND = 'sound/punch.mp3'
RIFLE_SOUND = 'sound/shot.mp3'
SNIPER_SOUND = 'sound/sshot.mp3'

# Игровое поле
UNIT_SIZE = 50, 50
GAME_FIELD_POS = X_INDENT, Y_INDENT = 50, 160 + GUI_PADDING
SPAWN_RANGE = SCREEN_HEIGHT - (Y_INDENT * 2)

# Игроки
PLAYER_HEALTH = 10000
PLAYER_START_COINS = 10
PLAYER_COIN_TIME = 10
PLAYER_FIRST_POS = (X_INDENT, Y_INDENT)
PLAYER_SECOND_POS = (SCREEN_WIDTH - X_INDENT, Y_INDENT)

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 122, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BUTTON_COLOR = (0, 0, 0)
BLACK = (0, 0, 0)

# HealthBar
HEALTH_BAR_COLOR = RED
RELOAD_BAR_COLOR = ORANGE
BACKGROUND_BAR_COLOR = BLACK
BAR_HEIGHT = 2

# Other
UNIT_KILLING_TIME = 3000
AMMO_KILLING_TIME = 300
AMMO_SIZE = 5, 5

VISIBLE_RADIUS = SPAWN_RANGE

units_list = [
    {
        "name": "Воин",
        "cost": 5,
        "unit": {
            "class": Warrior,
            "kwargs": dict(
                size=UNIT_SIZE,
                damage=10,
                health=100,
                reload_time=1000,
                speed=0.5,
                attack_radius=50,
                visible_radius=VISIBLE_RADIUS,
                sound=PUNCH_SOUND,
            )
        }

    },
    {
        "name": "Стрелок",
        "cost": 10,
        "unit": {
            "class": Shooter,
            "kwargs": dict(
                size=UNIT_SIZE,
                damage=20,
                health=100,
                reload_time=1000,
                speed=0.5,
                attack_radius=VISIBLE_RADIUS,
                visible_radius=VISIBLE_RADIUS,
                sound=RIFLE_SOUND,
            )
        }
    },
    {
        "name": "Тяжелый воин",
        "cost": 20,
        "unit": {
            "class": Warrior,
            "kwargs": dict(
                size=UNIT_SIZE,
                damage=10,
                health=500,
                reload_time=1000,
                speed=0.7,
                attack_radius=50,
                visible_radius=600,
                sound=PUNCH_SOUND,
            )
        }
    },
    {
        "name": "Снайпер",
        "cost": 15,
        "unit": {
            "class": HeavyShooter,
            "kwargs": dict(
                size=UNIT_SIZE,
                damage=200,
                health=100,
                reload_time=3000,
                speed=0.6,
                attack_radius=600,
                visible_radius=600,
                sound=SNIPER_SOUND,
            )
        }
    },
    {
        "name": "СУПЕР",
        "cost": 100,
        "unit": {
            "class": Warrior,
            "kwargs": dict(
                size=UNIT_SIZE,
                damage=2000,
                health=10000,
                reload_time=100,
                speed=2,
                attack_radius=100,
                visible_radius=600,
                sound=PUNCH_SOUND,
            )
        }
    },
]

# units_list = [
#     {
#         "name": "Воин",
#         "cost": 5,
#         "unit": dict(
#             class_name=Warrior,
#             size=UNIT_SIZE,
#             damage=10,
#             health=100,
#             reload_time=1000,
#             speed=0.5,
#             attack_radius=50,
#             visible_radius=600,
#             sound=PUNCH_SOUND,
#         )
#     },
#     {
#         "name": "Стрелок",
#         "cost": 10,
#         "unit": dict(
#             class_name=Warrior,
#             size=UNIT_SIZE,
#             damage=20,
#             health=100,
#             reload_time=1000,
#             speed=0.5,
#             attack_radius=300,
#             visible_radius=600,
#             sound=RIFLE_SOUND,
#         )
#     },
#     {
#         "name": "Тяжелый воин",
#         "cost": 20,
#         "unit": dict(
#             size=UNIT_SIZE,
#             damage=10,
#             health=500,
#             reload_time=1000,
#             speed=0.7,
#             attack_radius=50,
#             visible_radius=600,
#             sound=PUNCH_SOUND,
#         )
#     },
#     {
#         "name": "Снайпер",
#         "cost": 15,
#         "unit": dict(
#             size=UNIT_SIZE,
#             damage=200,
#             health=100,
#             reload_time=3000,
#             speed=0.6,
#             attack_radius=600,
#             visible_radius=600,
#             sound=SNIPER_SOUND,
#         )
#     },
#     {
#         "name": "СУПЕР",
#         "cost": 100,
#         "unit": dict(
#             size=UNIT_SIZE,
#             damage=2000,
#             health=10000,
#             reload_time=100,
#             speed=2,
#             attack_radius=100,
#             visible_radius=600,
#             sound=PUNCH_SOUND,
#         )
#     },
# ]

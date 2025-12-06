import os

from core.old.units_old import Warrior, Shooter, HeavyShooter
# Global settings
os.environ["SDL_VIDEO_CENTERED"] = "1"
DEBUG = False
COLLISION = False # May very decrease fps!!!
# Настройка экрана
MENU_SCREEN = MENU_SCREEN_SIZE, DEFAULT_MENU_SCREEN_SIZE = (MENU_SCREEN_WIDTH, MENU_SCREEN_HEIGHT), (DEFAULT_MENU_SCREEN_WIDTH, DEFAULT_MENU_SCREEN_HEIGHT) = (600, 400), (600, 400)
MAIN_SCREEN = MAIN_SCREEN_SIZE, DEFAULT_MAIN_SCREEN_SIZE = (MAIN_SCREEN_WIDTH, MAIN_SCREEN_HEIGHT), (DEFAULT_MAIN_SCREEN_WIDTH, DEFAULT_MAIN_SCREEN_HEIGHT) = (1280, 720), (1280, 720)

FULLSCREEN_SIZE = 1920, 1080
FULLSCREEN = True
SCREEN_FILL = "gray"
MENU_WINDOW_CAPTION = "Game Menu"
MAIN_WINDOW_CAPTION = 'Game'
GUI_PADDING = 10
FPS = 60

# Звуки
PUNCH_SOUND = '../../assets/sound/punch.mp3'
RIFLE_SOUND = '../../assets/sound/shot.mp3'
SNIPER_SOUND = '../../assets/sound/sshot.mp3'

# Игровое поле
UNIT_SIZE = 50, 50
GAME_FIELD_POS = X_INDENT, Y_INDENT = 50, 160 + GUI_PADDING
SPAWN_RANGE = MAIN_SCREEN_HEIGHT - (Y_INDENT * 2)

# Игроки
PLAYER_HEALTH = 10000
PLAYER_START_COINS = 10000
PLAYER_COIN_TIME = 10000
PLAYER_FIRST_POS = (X_INDENT, Y_INDENT)
PLAYER_SECOND_POS = (MAIN_SCREEN_WIDTH - X_INDENT, Y_INDENT)

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

# {
#     "name": "СУПЕР",
#     "cost": 100,
#     "unit": {
#         "class": Warrior,
#         "kwargs": dict(
#             size=UNIT_SIZE,
#             damage=2000,
#             health=10000,
#             reload_time=100,
#             speed=2,
#             attack_radius=100,
#             visible_radius=600,
#             sound=PUNCH_SOUND,
#             inventory={}
#         )
#     }
# },

# gun_list = [
#     {
#         "name": "Пистолет",
#         "cost": 100,
#         "gun": {
#             "class": Rifle,
#             "kwargs": {
#                 "damage": 100,
#                 "clip": 7,
#                 "reload_time": 1000,
#                 "fire_rate": 100,
#             }
#         }
#     }
# ]
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
GAMES = []
from core.utils import Point

SPAWN_POSITIONS = {
    "LEFT": {
        "tower": Point(
            points=[(50, 50), (50, 150), (50, 250), (50, 350), (50, 450)],
        ),
        "unit": Point(
            area=((100, 200), (100, 450)),
        ),
    },
    "RIGHT": {
        "tower": Point(
            points=[(1200, 50), (1200, 150), (1200, 250), (1200, 350), (1200, 450)],
        ),
        "unit": Point(
            area=((1200, 200), (0, 450)),
        ),
    },
}

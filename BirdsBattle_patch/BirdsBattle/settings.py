import os

WIDTH = 1280
HEIGHT = 720
FPS = 60

WORLD_WIDTH = 2600
GROUND_Y = 625

TITLE = "Birds Battle"
SAVE_FILE = "progress.json"

GRAVITY = 900.0
MAX_PULL = 155
LAUNCH_POWER = 7.0
AIR_DRAG = 0.999
GROUND_FRICTION = 0.985

BG_COLOR = (135, 206, 250)
GROUND_COLOR = (104, 176, 74)
UI_DARK = (29, 36, 49)
UI_LIGHT = (240, 245, 255)
ACCENT = (255, 190, 60)

MATERIALS = {
    "wood": {"hp": 120, "density": 1.0, "color": (166, 108, 60), "score": 300},
    "stone": {"hp": 240, "density": 1.8, "color": (120, 125, 135), "score": 500},
    "glass": {"hp": 65, "density": 0.7, "color": (115, 215, 230), "score": 400},
}

BIRD_COLORS = {
    "Red": (220, 60, 55),
    "Speed": (245, 220, 70),
    "Bomb": (45, 50, 58),
    "Split": (70, 150, 235),
    "Giant": (155, 80, 195),
}

ROOT = os.path.dirname(os.path.abspath(__file__))
LEVEL_DIR = os.path.join(ROOT, "levels")
ASSET_DIR = os.path.join(ROOT, "assets")

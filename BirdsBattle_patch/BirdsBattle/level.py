import json, os
from block import Block
from enemy import Gremlin
from settings import LEVEL_DIR

def load_level(number):
    path = os.path.join(LEVEL_DIR, f"level{number}.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    blocks = [Block(**b) for b in data["blocks"]]
    enemies = [Gremlin(**e) for e in data["enemies"]]
    return data, blocks, enemies

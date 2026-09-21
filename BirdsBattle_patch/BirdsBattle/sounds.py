import os, pygame
from settings import ASSET_DIR

class SoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return
        for name in ["launch","impact","destroy","explosion","victory","defeat","button"]:
            for ext in ("wav","ogg","mp3"):
                path = os.path.join(ASSET_DIR, "sounds", f"{name}.{ext}")
                if os.path.exists(path):
                    try:
                        self.sounds[name] = pygame.mixer.Sound(path)
                    except pygame.error:
                        pass
                    break

    def play(self, name):
        if self.enabled and name in self.sounds:
            try: self.sounds[name].play()
            except pygame.error: pass

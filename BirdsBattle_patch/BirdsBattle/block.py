import pygame
from settings import MATERIALS, GROUND_Y
from physics import circle_rect_collision

class Block:
    def __init__(self, x, y, w, h, material="wood"):
        self.x, self.y = float(x), float(y)
        self.w, self.h = int(w), int(h)
        self.material = material
        info = MATERIALS[material]
        self.max_hp = info["hp"]
        self.hp = float(self.max_hp)
        self.color = info["color"]
        self.score = info["score"]
        self.vy = 0.0
        self.destroyed = False
        self.flash = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt):
        if self.destroyed:
            return
        self.flash = max(0, self.flash - dt)
        if self.y + self.h < GROUND_Y:
            self.vy += 650 * dt
            self.y += self.vy * dt
            if self.y + self.h >= GROUND_Y:
                self.y = GROUND_Y - self.h
                self.vy *= -0.18
        else:
            self.vy *= 0.8

    def damage(self, amount):
        self.hp -= amount
        self.flash = 0.1
        if self.hp <= 0:
            self.destroyed = True
            return True
        return False

    def draw(self, surf, camera):
        if self.destroyed:
            return
        sx, sy = camera.world_to_screen(self.x, self.y)
        r = pygame.Rect(sx, sy, self.w, self.h)
        c = tuple(min(255, v+35) for v in self.color) if self.flash > 0 else self.color
        pygame.draw.rect(surf, c, r, border_radius=5)
        pygame.draw.rect(surf, (70,70,80), r, 2, border_radius=5)
        ratio = max(0, self.hp/self.max_hp)
        if ratio < 0.7:
            pygame.draw.line(surf, (70,70,75), (sx+8, sy+7), (sx+self.w-8, sy+self.h-7), 3)
        if ratio < 0.35:
            pygame.draw.line(surf, (70,70,75), (sx+self.w-10, sy+6), (sx+10, sy+self.h-8), 3)

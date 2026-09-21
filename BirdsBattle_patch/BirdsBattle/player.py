import pygame, math
from bird import Bird
from physics import predicted_points, clamp
from settings import MAX_PULL, LAUNCH_POWER, BIRD_COLORS

class SlingshotPlayer:
    def __init__(self, game):
        self.game = game
        self.anchor = pygame.Vector2(245, 510)
        self.dragging = False

    def spawn_next(self):
        if self.game.current_bird or not self.game.bird_queue:
            return
        kind = self.game.bird_queue.pop(0)
        self.game.current_bird = Bird(kind, self.anchor.x, self.anchor.y)

    def handle_event(self, event):
        b = self.game.current_bird
        if not b: return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            wx = mx + self.game.camera.x
            if not b.launched and math.hypot(wx-b.x, my-b.y) <= b.radius+18:
                self.dragging = True
        elif event.type == pygame.MOUSEMOTION and self.dragging and not b.launched:
            mx, my = event.pos
            wx = mx + self.game.camera.x
            v = pygame.Vector2(wx, my) - self.anchor
            if v.length() > MAX_PULL:
                v.scale_to_length(MAX_PULL)
            b.x, b.y = self.anchor.x + v.x, self.anchor.y + v.y
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            pull = self.anchor - pygame.Vector2(b.x, b.y)
            b.launch(pull.x*LAUNCH_POWER, pull.y*LAUNCH_POWER)
            self.game.sounds.play("launch")

    def draw(self, surf):
        b = self.game.current_bird
        ax, ay = self.game.camera.world_to_screen(self.anchor.x, self.anchor.y)
        # back fork
        pygame.draw.line(surf, (92,57,35), (ax-12, ay+55), (ax-7,ay), 14)
        pygame.draw.line(surf, (92,57,35), (ax+12, ay+55), (ax+7,ay), 14)
        if b and not b.launched:
            bx, by = self.game.camera.world_to_screen(b.x, b.y)
            pygame.draw.line(surf, (65,40,28), (ax-9,ay), (bx,by), 6)
            pygame.draw.line(surf, (65,40,28), (ax+9,ay), (bx,by), 6)
            if self.dragging:
                vel = ((self.anchor.x-b.x)*LAUNCH_POWER, (self.anchor.y-b.y)*LAUNCH_POWER)
                for px, py in predicted_points((b.x,b.y), vel, 18, 0.09):
                    sx, sy = self.game.camera.world_to_screen(px,py)
                    if 0 <= sx <= surf.get_width() and 0 <= sy <= surf.get_height():
                        pygame.draw.circle(surf, (255,255,255), (sx,sy), 3)
        # front fork
        pygame.draw.circle(surf, (78,48,30), (ax-8,ay), 8)
        pygame.draw.circle(surf, (78,48,30), (ax+8,ay), 8)

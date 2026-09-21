import pygame, math
from settings import GROUND_Y

class Gremlin:
    def __init__(self, x, y, hp=100):
        self.x, self.y = float(x), float(y)
        self.radius = 24
        self.max_hp = hp
        self.hp = float(hp)
        self.dead = False
        self.hit_timer = 0.0
        self.death_timer = 0.0
        self.phase = (x+y) * 0.01

    def update(self, dt):
        self.hit_timer = max(0, self.hit_timer-dt)
        if self.dead:
            self.death_timer += dt

    def damage(self, amount):
        if self.dead:
            return False
        self.hp -= amount
        self.hit_timer = 0.18
        if self.hp <= 0:
            self.dead = True
            return True
        return False

    def draw(self, surf, camera, time_s):
        if self.dead and self.death_timer > 0.8:
            return
        bob = math.sin(time_s*4 + self.phase) * 3 if not self.dead else -self.death_timer*25
        sx, sy = camera.world_to_screen(self.x, self.y + bob)
        scale = max(0.05, 1.0 - self.death_timer) if self.dead else 1.0
        rad = max(2, int(self.radius*scale))
        color = (130, 230, 85) if self.hit_timer <= 0 else (255, 245, 100)
        pygame.draw.circle(surf, color, (sx, int(sy)), rad)
        if not self.dead:
            pygame.draw.circle(surf, (30,35,30), (sx-8, int(sy)-4), 4)
            pygame.draw.circle(surf, (30,35,30), (sx+8, int(sy)-4), 4)
            pygame.draw.arc(surf, (35,45,35), (sx-9, int(sy)+4, 18, 10), 0.1, 3.0, 2)
            # ears
            pygame.draw.polygon(surf, color, [(sx-18,int(sy)-12),(sx-30,int(sy)-24),(sx-22,int(sy)-2)])
            pygame.draw.polygon(surf, color, [(sx+18,int(sy)-12),(sx+30,int(sy)-24),(sx+22,int(sy)-2)])

    def alive_for_win(self):
        return not self.dead

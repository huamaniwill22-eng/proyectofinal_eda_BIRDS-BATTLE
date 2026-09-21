import random
import pygame

class Particle:
    def __init__(self, x, y, color, speed=180, life=0.8, size=5):
        a = random.uniform(0, 6.283)
        s = random.uniform(speed*0.35, speed)
        self.x, self.y = x, y
        self.vx = __import__("math").cos(a) * s
        self.vy = __import__("math").sin(a) * s - 80
        self.life = life
        self.max_life = life
        self.color = color
        self.size = random.randint(2, size)

    def update(self, dt):
        self.life -= dt
        self.vy += 450 * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.985

    def draw(self, surf, camera):
        if self.life <= 0:
            return
        sx, sy = camera.world_to_screen(self.x, self.y)
        scale = max(0.25, self.life/self.max_life)
        pygame.draw.circle(surf, self.color, (sx, sy), max(1, int(self.size*scale)))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, color, amount=14, speed=180, size=5):
        for _ in range(amount):
            self.particles.append(Particle(x, y, color, speed, random.uniform(0.4, 0.9), size))

    def update(self, dt):
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]

    def draw(self, surf, camera):
        for p in self.particles:
            p.draw(surf, camera)

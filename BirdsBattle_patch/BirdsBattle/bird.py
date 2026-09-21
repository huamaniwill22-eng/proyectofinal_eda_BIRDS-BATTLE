import pygame, math
from settings import *
from physics import circle_rect_collision, impact_energy, normalized

class Bird:
    def __init__(self, kind, x, y, mini=False):
        self.kind = kind
        self.x, self.y = float(x), float(y)
        self.vx = self.vy = 0.0
        self.radius = 14 if mini else (28 if kind == "Giant" else 20)
        self.mass = 2.6 if kind == "Giant" else (2.0 if kind == "Bomb" else 1.0)
        if mini: self.mass = 0.55
        self.active = False
        self.launched = False
        self.finished = False
        self.ability_used = False
        self.rest_time = 0.0
        self.mini = mini

    def launch(self, vx, vy):
        self.vx, self.vy = vx, vy
        self.active = self.launched = True

    def ability(self, game):
        if not self.active or self.finished or self.ability_used or self.mini:
            return
        self.ability_used = True
        if self.kind == "Speed":
            nx, ny = normalized(self.vx, self.vy)
            self.vx += nx * 500
            self.vy += ny * 500
            game.particles.burst(self.x, self.y, BIRD_COLORS[self.kind], 18, 250, 5)
            game.sounds.play("launch")
        elif self.kind == "Bomb":
            game.explode(self.x, self.y, 150, 230)
        elif self.kind == "Split":
            for off in (-160, 160):
                b = Bird("Split", self.x, self.y, mini=True)
                b.launch(self.vx, self.vy + off)
                game.extra_birds.append(b)
            game.particles.burst(self.x, self.y, BIRD_COLORS[self.kind], 16, 200, 5)

    def update(self, dt, game):
        if not self.active or self.finished:
            return
        self.vy += GRAVITY * dt
        self.vx *= AIR_DRAG
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Ground
        if self.y + self.radius >= GROUND_Y:
            self.y = GROUND_Y - self.radius
            if abs(self.vy) > 80:
                game.particles.burst(self.x, self.y, (175,140,95), 8, 120, 4)
            self.vy *= -0.32
            self.vx *= GROUND_FRICTION

        # Blocks
        for block in game.blocks:
            if block.destroyed: continue
            hit, dx, dy = circle_rect_collision(self.x, self.y, self.radius, block.rect)
            if hit:
                speed = math.hypot(self.vx, self.vy)
                dmg = max(0, (speed - 80) * 0.26 * self.mass)
                if dmg > 4:
                    broke = block.damage(dmg)
                    game.register_block_hit(block, broke, speed)
                if abs(dx) > abs(dy):
                    self.vx *= -0.35
                    self.x += 3 if dx > 0 else -3
                else:
                    self.vy *= -0.35
                    self.y += 3 if dy > 0 else -3
                self.vx *= 0.78
                self.vy *= 0.78

        # Gremlins
        for enemy in game.enemies:
            if enemy.dead: continue
            dx = self.x - enemy.x
            dy = self.y - enemy.y
            rr = self.radius + enemy.radius
            if dx*dx + dy*dy <= rr*rr:
                speed = math.hypot(self.vx, self.vy)
                dmg = max(8, (speed - 50) * 0.35 * self.mass)
                killed = enemy.damage(dmg)
                game.register_enemy_hit(enemy, killed)
                nx, ny = normalized(dx, dy)
                self.vx += nx * 60
                self.vy += ny * 60
                self.vx *= -0.22
                self.vy *= -0.22

        speed = math.hypot(self.vx, self.vy)
        if speed < 35 and self.y + self.radius >= GROUND_Y - 2:
            self.rest_time += dt
        else:
            self.rest_time = 0.0

        if self.x > WORLD_WIDTH + 200 or self.x < -200 or self.y > HEIGHT + 500 or self.rest_time > 1.3:
            self.finished = True
            self.active = False

    def draw(self, surf, camera):
        if self.finished:
            return
        sx, sy = camera.world_to_screen(self.x, self.y)
        color = BIRD_COLORS.get(self.kind, (230,80,80))
        pygame.draw.circle(surf, color, (sx, sy), self.radius)
        pygame.draw.circle(surf, (255,255,245), (sx+6, sy-6), max(4,self.radius//4))
        pygame.draw.circle(surf, (30,30,35), (sx+8, sy-7), max(2,self.radius//8))
        pygame.draw.polygon(surf, (245,165,45), [(sx+self.radius-3,sy),(sx+self.radius+12,sy+4),(sx+self.radius-3,sy+8)])
        pygame.draw.line(surf, (45,45,50), (sx-8,sy-self.radius+5),(sx-2,sy-self.radius-5),3)
        pygame.draw.line(surf, (45,45,50), (sx+1,sy-self.radius+5),(sx+7,sy-self.radius-5),3)

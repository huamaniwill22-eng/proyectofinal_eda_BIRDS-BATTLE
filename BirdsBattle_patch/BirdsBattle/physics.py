import math
import pygame
from settings import GRAVITY

def clamp(value, low, high):
    return max(low, min(high, value))

def length(x, y):
    return math.hypot(x, y)

def normalized(x, y):
    l = math.hypot(x, y)
    if l <= 1e-6:
        return 0.0, 0.0
    return x/l, y/l

def circle_rect_collision(cx, cy, radius, rect):
    nearest_x = clamp(cx, rect.left, rect.right)
    nearest_y = clamp(cy, rect.top, rect.bottom)
    dx = cx - nearest_x
    dy = cy - nearest_y
    return dx*dx + dy*dy <= radius*radius, dx, dy

def predicted_points(start, velocity, count=20, step=0.12):
    pts = []
    x0, y0 = start
    vx, vy = velocity
    for i in range(1, count+1):
        t = i * step
        x = x0 + vx * t
        y = y0 + vy * t + 0.5 * GRAVITY * t * t
        pts.append((x, y))
    return pts

def impact_energy(vx, vy, mass=1.0):
    return 0.5 * mass * (vx*vx + vy*vy)

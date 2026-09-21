from settings import WIDTH, WORLD_WIDTH

class Camera:
    def __init__(self):
        self.x = 0.0

    def follow(self, target_x, dt):
        desired = max(0, min(WORLD_WIDTH - WIDTH, target_x - WIDTH * 0.38))
        self.x += (desired - self.x) * min(1.0, 4.5 * dt)

    def return_home(self, dt):
        self.x += (0 - self.x) * min(1.0, 4.0 * dt)

    def world_to_screen(self, x, y):
        return int(x - self.x), int(y)

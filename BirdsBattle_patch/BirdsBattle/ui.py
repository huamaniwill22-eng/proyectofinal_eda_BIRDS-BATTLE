import pygame
from settings import WIDTH, HEIGHT, UI_DARK, UI_LIGHT, ACCENT

pygame.font.init()

def font(size, bold=False):
    return pygame.font.SysFont("arial", size, bold=bold)

def draw_text(surf, text, size, x, y, color=(255,255,255), center=False, bold=False):
    img = font(size, bold).render(str(text), True, color)
    rect = img.get_rect()
    if center: rect.center = (x,y)
    else: rect.topleft = (x,y)
    surf.blit(img, rect)
    return rect

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surf, mouse):
        hover = self.rect.collidepoint(mouse)
        color = (255,205,75) if hover else ACCENT
        shadow = self.rect.move(0,5)
        pygame.draw.rect(surf, (30,35,45), shadow, border_radius=12)
        pygame.draw.rect(surf, color, self.rect, border_radius=12)
        pygame.draw.rect(surf, (255,235,160), self.rect, 2, border_radius=12)
        draw_text(surf, self.text, 26, self.rect.centerx, self.rect.centery, UI_DARK, True, True)

    def hit(self, pos):
        return self.rect.collidepoint(pos)

def hud(surf, game):
    pygame.draw.rect(surf, (20,28,40), (0,0,WIDTH,66))
    draw_text(surf, f"NIVEL {game.level_num}", 24, 24, 18, UI_LIGHT, bold=True)
    draw_text(surf, f"PUNTOS: {int(game.score)}", 24, 190, 18, (255,220,90), bold=True)
    draw_text(surf, f"AVES: {len(game.bird_queue) + (1 if game.current_bird and not game.current_bird.finished else 0)}", 22, 410, 20)
    alive = sum(1 for e in game.enemies if not e.dead)
    draw_text(surf, f"GREMLINS: {alive}", 22, 555, 20)
    progress = 1 - alive/max(1,game.start_enemy_count)
    pygame.draw.rect(surf, (55,65,80), (760,23,260,18), border_radius=9)
    pygame.draw.rect(surf, (105,220,100), (760,23,int(260*progress),18), border_radius=9)
    pygame.draw.rect(surf, (245,245,250), (1190,14,50,38), 2, border_radius=8)
    draw_text(surf, "II", 22, 1215, 33, center=True, bold=True)

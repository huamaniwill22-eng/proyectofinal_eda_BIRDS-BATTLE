import pygame
from settings import WIDTH, HEIGHT, TITLE
from ui import Button, draw_text

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = "main"
        self.buttons = []

    def set_screen(self, name):
        self.screen = name

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        pos = event.pos
        if self.screen == "main":
            labels = ["JUGAR","SELECCIONAR NIVEL","INSTRUCCIONES","OPCIONES","SALIR"]
            for b,l in zip(self.buttons, labels):
                if b.hit(pos):
                    self.game.sounds.play("button")
                    if l == "JUGAR": self.game.start_level(self.game.progress.get("highest",1))
                    elif l == "SELECCIONAR NIVEL": self.screen="levels"
                    elif l == "INSTRUCCIONES": self.screen="instructions"
                    elif l == "OPCIONES": self.screen="options"
                    elif l == "SALIR": self.game.running=False
        elif self.screen == "levels":
            for i,b in enumerate(self.buttons[:10], start=1):
                if b.hit(pos) and i <= self.game.progress.get("highest",1):
                    self.game.start_level(i)
            if self.buttons[-1].hit(pos): self.screen="main"
        else:
            if self.buttons and self.buttons[-1].hit(pos): self.screen="main"

    def draw_bg(self, surf):
        surf.fill((112,192,245))
        pygame.draw.circle(surf,(255,235,115),(1050,130),70)
        for x,y in [(170,150),(430,95),(850,180)]:
            pygame.draw.ellipse(surf,(250,250,250),(x,y,150,45))
            pygame.draw.circle(surf,(250,250,250),(x+40,y),38)
            pygame.draw.circle(surf,(250,250,250),(x+85,y-5),45)
        pygame.draw.polygon(surf,(82,150,96),[(0,520),(220,310),(460,520)])
        pygame.draw.polygon(surf,(70,135,90),[(310,520),(610,270),(900,520)])
        pygame.draw.polygon(surf,(90,160,100),[(720,520),(1030,320),(1280,520)])
        pygame.draw.rect(surf,(93,180,78),(0,510,WIDTH,210))

    def draw(self, surf):
        self.draw_bg(surf)
        mouse=pygame.mouse.get_pos()
        self.buttons=[]
        if self.screen == "main":
            draw_text(surf, TITLE.upper(), 72, WIDTH//2, 105, (38,42,55), True, True)
            draw_text(surf, "Lanza. Destruye. Domina.", 24, WIDTH//2, 165, (55,70,75), True)
            for i,t in enumerate(["JUGAR","SELECCIONAR NIVEL","INSTRUCCIONES","OPCIONES","SALIR"]):
                b=Button((WIDTH//2-170,220+i*72,340,54),t); b.draw(surf,mouse); self.buttons.append(b)
        elif self.screen == "levels":
            draw_text(surf,"SELECCIONAR NIVEL",52,WIDTH//2,100,(35,40,50),True,True)
            highest=self.game.progress.get("highest",1)
            for i in range(10):
                col=i%5; row=i//5
                b=Button((250+col*160,210+row*120,110,72),str(i+1) if i+1<=highest else "🔒")
                b.draw(surf,mouse); self.buttons.append(b)
            back=Button((WIDTH//2-120,500,240,55),"VOLVER"); back.draw(surf,mouse); self.buttons.append(back)
        elif self.screen == "instructions":
            draw_text(surf,"INSTRUCCIONES",52,WIDTH//2,95,(35,40,50),True,True)
            lines=[
                "Arrastra el ave hacia atrás con el mouse y suelta para lanzar.",
                "Haz clic durante el vuelo para activar la habilidad especial.",
                "Speed: impulso | Bomb: explosión | Split: se divide en 3.",
                "Giant: gran masa y daño. Red: equilibrado.",
                "Destruye todos los Gremlins antes de quedarte sin aves.",
                "ESC pausa el juego."
            ]
            for i,l in enumerate(lines): draw_text(surf,l,25,WIDTH//2,200+i*48,(40,50,60),True)
            b=Button((WIDTH//2-120,530,240,55),"VOLVER"); b.draw(surf,mouse); self.buttons.append(b)
        elif self.screen == "options":
            draw_text(surf,"OPCIONES",52,WIDTH//2,120,(35,40,50),True,True)
            state="ACTIVADOS" if self.game.sounds.enabled else "DESACTIVADOS"
            draw_text(surf,f"Sonidos opcionales: {state}",28,WIDTH//2,250,(45,55,60),True)
            draw_text(surf,"Si no hay archivos de audio, el juego continúa normalmente.",22,WIDTH//2,305,(45,55,60),True)
            b=Button((WIDTH//2-120,470,240,55),"VOLVER"); b.draw(surf,mouse); self.buttons.append(b)

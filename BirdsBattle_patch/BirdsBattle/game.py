import pygame, json, os, math, random
from settings import *
from camera import Camera
from level import load_level
from particles import ParticleSystem
from player import SlingshotPlayer
from sounds import SoundManager
from menu import Menu
from ui import hud, draw_text, Button

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"
        self.camera = Camera()
        self.particles = ParticleSystem()
        self.sounds = SoundManager()
        self.progress = self.load_progress()
        self.menu = Menu(self)
        self.level_num = 1
        self.level_data = {}
        self.blocks=[]
        self.enemies=[]
        self.current_bird=None
        self.extra_birds=[]
        self.bird_queue=[]
        self.player=None
        self.score=0
        self.combo=1
        self.combo_timer=0
        self.blocks_destroyed=0
        self.enemies_defeated=0
        self.start_enemy_count=1
        self.level_end_timer=0
        self.time_s=0

    def load_progress(self):
        path=os.path.join(ROOT,SAVE_FILE)
        try:
            with open(path,"r",encoding="utf-8") as f: return json.load(f)
        except Exception:
            return {"highest":1,"stars":{},"scores":{}}

    def save_progress(self):
        path=os.path.join(ROOT,SAVE_FILE)
        try:
            with open(path,"w",encoding="utf-8") as f: json.dump(self.progress,f,indent=2)
        except OSError:
            pass

    def start_level(self, num):
        self.level_num=max(1,min(10,num))
        self.level_data,self.blocks,self.enemies=load_level(self.level_num)
        self.current_bird=None
        self.extra_birds=[]
        self.bird_queue=list(self.level_data["birds"])
        self.score=0
        self.combo=1
        self.combo_timer=0
        self.blocks_destroyed=0
        self.enemies_defeated=0
        self.start_enemy_count=len(self.enemies)
        self.level_end_timer=0
        self.camera.x=0
        self.particles=ParticleSystem()
        self.player=SlingshotPlayer(self)
        self.player.spawn_next()
        self.state="playing"

    def register_block_hit(self, block, broke, speed):
        self.sounds.play("impact")
        self.particles.burst(block.x+block.w/2,block.y+block.h/2,block.color,7,120,4)
        if broke:
            self.blocks_destroyed += 1
            gain = int(block.score * self.combo)
            self.score += gain
            self.combo = min(4.0, self.combo + 0.25)
            self.combo_timer = 2.0
            self.sounds.play("destroy")
            self.particles.burst(block.x+block.w/2,block.y+block.h/2,block.color,20,220,6)
            # nearby structures receive shock
            for other in self.blocks:
                if other is block or other.destroyed: continue
                dx=(other.x+other.w/2)-(block.x+block.w/2)
                dy=(other.y+other.h/2)-(block.y+block.h/2)
                d=math.hypot(dx,dy)
                if d<95: other.damage(max(0,25-d*0.15))

    def register_enemy_hit(self, enemy, killed):
        self.score += int((500 if killed else 120) * self.combo)
        self.combo = min(4.0, self.combo + (0.5 if killed else 0.1))
        self.combo_timer = 2.0
        self.particles.burst(enemy.x,enemy.y,(130,230,85),18 if killed else 8,200,5)
        if killed:
            self.enemies_defeated += 1
            self.sounds.play("destroy")

    def explode(self,x,y,radius,power):
        self.sounds.play("explosion")
        self.particles.burst(x,y,(255,150,55),36,320,8)
        for block in self.blocks:
            if block.destroyed: continue
            cx=block.x+block.w/2; cy=block.y+block.h/2
            d=math.hypot(cx-x,cy-y)
            if d<radius:
                broke=block.damage((1-d/radius)*power)
                self.register_block_hit(block,broke,power)
        for e in self.enemies:
            if e.dead: continue
            d=math.hypot(e.x-x,e.y-y)
            if d<radius:
                killed=e.damage(max(10,(1-d/radius)*170))
                self.register_enemy_hit(e,killed)

    def draw_world(self):
        self.screen.fill((135,206,250))
        # distant sun/clouds
        pygame.draw.circle(self.screen,(255,235,115),(1050-int(self.camera.x*0.08),125),58)
        for base in [180,650,1180,1700,2200]:
            sx=int(base-self.camera.x*0.25)
            pygame.draw.ellipse(self.screen,(245,250,255),(sx,125,150,42))
            pygame.draw.circle(self.screen,(245,250,255),(sx+45,125),34)
            pygame.draw.circle(self.screen,(245,250,255),(sx+90,118),40)
        # parallax mountains
        for base,h in [(50,190),(430,250),(900,175),(1320,235),(1850,210),(2300,260)]:
            sx=base-int(self.camera.x*0.45)
            pygame.draw.polygon(self.screen,(85,145,115),[(sx,GROUND_Y),(sx+180,GROUND_Y-h),(sx+380,GROUND_Y)])
        # ground
        pygame.draw.rect(self.screen,GROUND_COLOR,(0,GROUND_Y,WIDTH,HEIGHT-GROUND_Y))
        pygame.draw.rect(self.screen,(90,145,65),(0,GROUND_Y,WIDTH,12))
        # trees
        for tx in [80,480,880,1450,2050,2450]:
            sx=int(tx-self.camera.x)
            if -80<sx<WIDTH+80:
                pygame.draw.rect(self.screen,(105,72,45),(sx,GROUND_Y-80,18,80))
                pygame.draw.circle(self.screen,(70,150,70),(sx+10,GROUND_Y-95),40)
                pygame.draw.circle(self.screen,(85,170,75),(sx-14,GROUND_Y-75),30)
        for b in self.blocks: b.draw(self.screen,self.camera)
        for e in self.enemies: e.draw(self.screen,self.camera,self.time_s)
        self.player.draw(self.screen)
        if self.current_bird: self.current_bird.draw(self.screen,self.camera)
        for b in self.extra_birds: b.draw(self.screen,self.camera)
        self.particles.draw(self.screen,self.camera)
        hud(self.screen,self)
        if self.combo>1.01:
            draw_text(self.screen,f"COMBO x{self.combo:.1f}",22,1040,20,(255,220,100),bold=True)

    def finish_victory(self):
        bonus=(len(self.bird_queue) + (0 if not self.current_bird or self.current_bird.finished else 1))*1000
        self.score += bonus
        max_score=self.level_data.get("max_score",10000)
        ratio=self.score/max_score if max_score else 0
        stars=3 if ratio>=0.75 else (2 if ratio>=0.45 else 1)
        self.progress["highest"]=max(self.progress.get("highest",1), min(10,self.level_num+1))
        self.progress.setdefault("stars",{})[str(self.level_num)]=max(stars,self.progress.get("stars",{}).get(str(self.level_num),0))
        self.progress.setdefault("scores",{})[str(self.level_num)]=max(int(self.score),self.progress.get("scores",{}).get(str(self.level_num),0))
        self.save_progress()
        self.result_stars=stars
        self.state="victory"
        self.sounds.play("victory")

    def update_play(self,dt):
        self.time_s += dt
        self.combo_timer -= dt
        if self.combo_timer<=0: self.combo=max(1.0,self.combo-dt*1.5)
        for b in self.blocks: b.update(dt)
        for e in self.enemies: e.update(dt)
        if self.current_bird:
            self.current_bird.update(dt,self)
        for b in self.extra_birds:
            b.update(dt,self)
        self.extra_birds=[b for b in self.extra_birds if not b.finished]
        self.particles.update(dt)
        # Camera
        if self.current_bird and self.current_bird.active:
            self.camera.follow(self.current_bird.x,dt)
        else:
            self.camera.return_home(dt)

        if all(e.dead for e in self.enemies):
            self.level_end_timer += dt
            if self.level_end_timer>1.0: self.finish_victory(); return

        if self.current_bird and self.current_bird.finished and not self.extra_birds:
            self.current_bird=None
            if self.bird_queue:
                self.player.spawn_next()
            else:
                self.level_end_timer += dt
                if self.level_end_timer>1.2:
                    if any(not e.dead for e in self.enemies):
                        self.state="defeat"
                        self.sounds.play("defeat")

    def handle_play_event(self,event):
        if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
            self.state="pause"; return
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if pygame.Rect(1190,14,50,38).collidepoint(event.pos):
                self.state="pause"; return
            if self.current_bird and self.current_bird.active:
                self.current_bird.ability(self)
        self.player.handle_event(event)

    def modal(self,title,lines,buttons):
        overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); overlay.fill((15,20,30,185)); self.screen.blit(overlay,(0,0))
        panel=pygame.Rect(WIDTH//2-280,120,560,480)
        pygame.draw.rect(self.screen,(32,42,58),panel,border_radius=22)
        pygame.draw.rect(self.screen,(255,220,110),panel,3,border_radius=22)
        draw_text(self.screen,title,46,WIDTH//2,175,(255,225,90),True,True)
        for i,l in enumerate(lines): draw_text(self.screen,l,24,WIDTH//2,245+i*38,(240,245,255),True)
        mouse=pygame.mouse.get_pos(); out=[]
        start=410
        for i,t in enumerate(buttons):
            b=Button((WIDTH//2-170,start+i*62,340,48),t); b.draw(self.screen,mouse); out.append(b)
        return out

    def run(self):
        while self.running:
            dt=self.clock.tick(FPS)/1000.0
            events=pygame.event.get()
            for event in events:
                if event.type==pygame.QUIT: self.running=False
                elif self.state=="menu": self.menu.handle_event(event)
                elif self.state=="playing": self.handle_play_event(event)
                elif self.state in ("pause","victory","defeat") and event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                    pos=event.pos
                    # handled after draw with same layout
                    if self.state=="pause":
                        btns=[pygame.Rect(WIDTH//2-170,410+i*62,340,48) for i in range(3)]
                        if btns[0].collidepoint(pos): self.state="playing"
                        elif btns[1].collidepoint(pos): self.start_level(self.level_num)
                        elif btns[2].collidepoint(pos): self.state="menu"; self.menu.set_screen("main")
                    elif self.state=="victory":
                        btns=[pygame.Rect(WIDTH//2-170,410+i*62,340,48) for i in range(3)]
                        if btns[0].collidepoint(pos): self.start_level(min(10,self.level_num+1))
                        elif btns[1].collidepoint(pos): self.start_level(self.level_num)
                        elif btns[2].collidepoint(pos): self.state="menu"; self.menu.set_screen("main")
                    elif self.state=="defeat":
                        btns=[pygame.Rect(WIDTH//2-170,410+i*62,340,48) for i in range(2)]
                        if btns[0].collidepoint(pos): self.start_level(self.level_num)
                        elif btns[1].collidepoint(pos): self.state="menu"; self.menu.set_screen("main")

            if self.state=="menu":
                self.menu.draw(self.screen)
            else:
                if self.state=="playing": self.update_play(dt)
                self.draw_world()
                if self.state=="pause":
                    self.modal("PAUSA",["Elige una opción"],["CONTINUAR","REINICIAR","MENÚ PRINCIPAL"])
                elif self.state=="victory":
                    stars="★"*self.result_stars + "☆"*(3-self.result_stars)
                    self.modal("NIVEL COMPLETADO",[
                        f"Estrellas: {stars}",
                        f"Puntuación: {int(self.score)}",
                        f"Enemigos derrotados: {self.enemies_defeated}",
                        f"Bloques destruidos: {self.blocks_destroyed}",
                        f"Aves restantes: {len(self.bird_queue)}"
                    ],["SIGUIENTE NIVEL","REINTENTAR","MENÚ PRINCIPAL"])
                elif self.state=="defeat":
                    self.modal("NIVEL FALLIDO",[
                        f"Puntuación: {int(self.score)}",
                        "Aún quedan Gremlins en el escenario."
                    ],["REINTENTAR","MENÚ PRINCIPAL"])
            pygame.display.flip()
        pygame.quit()

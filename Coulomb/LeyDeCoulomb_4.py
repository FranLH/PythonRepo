import pygame
import math
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2




Constante = 8.99*math.pow(10,9) # 8.99
NanoCoulomb = math.pow(10,-9)
MicroCoulomb = math.pow(10,-6)
PARTICLESIZE = 8
POSITIONPARTICLEMULT = 120
FORCERENDERMULT = math.pow(12,8)
RENDERADDEDFORCES = False
RENDERINDIVIDUALFORCES = True 
ANGLEARCSIZE = 40

def TrueAngle(angle):
    if angle<0:
        return(360+angle)
    else:
        return(angle)
    
class Particula():
    def __init__(self, carga, pos:vec2):
        self.carga, self.pos, self.fuerza, self.angulo, self.positivo, self.fuerzas = carga, pos, vec2(0,0), 0, carga>0, []
    def CalculateForce(self, particles):
        FDir = vec2(0,0)
        self.fuerzas = []
        for particle in particles:
            if particle != self:
                try:
                    F = (Constante*abs(self.carga)*NanoCoulomb*abs(particle.carga)*NanoCoulomb)/math.pow(self.pos.Dist(particle.pos),2)
                    if self.positivo == particle.positivo:
                        Dir = (self.pos-particle.pos).Normalized()
                    else:
                        Dir = (particle.pos-self.pos).Normalized()
                    FDir+= Dir*F
                    self.fuerzas.append(Dir*F)
                except:
                    pass
                #print(Dir, F, Dir*F, self.pos.Dist(particle.pos))
        self.fuerza = FDir
        self.angulo = TrueAngle(FDir.Angle())
    def PrintForce(self):
        print("Fuerza: " + str(self.fuerza.Length()) + " Newtons")
    def PrintAngle(self):
        print("Angulo: " + str(self.angulo) + " Grados")
    def CampoElectrico(self, particles, lines, length):
        r = 360/lines
        for i in lines:
            l = 0
            direction = vec2(1,0)
            force = self.fuerza*direction
            pos = self.pos
            while l<length:
                
                l+=1
    def Render(self,surface, cam):
        if self.positivo:
            color = (0,0,255)
        else:
            color = (255,0,0)

        # Individual forces
        if RENDERINDIVIDUALFORCES:
            for f in self.fuerzas:
                pygame.draw.line(surface, (0,255,0), cam.ToScreen(self.pos*POSITIONPARTICLEMULT).ToList(), cam.ToScreen(self.pos*POSITIONPARTICLEMULT+(f*FORCERENDERMULT)).ToList())
        
        # Added up forces
        if RENDERADDEDFORCES:
            position = self.pos*POSITIONPARTICLEMULT
            for f in range(len(self.fuerzas)):
                if f>0:
                    pygame.draw.line(surface, (255,255,0), cam.ToScreen(position).ToList(), cam.ToScreen(position+(self.fuerzas[f]*FORCERENDERMULT)).ToList())
                position+=self.fuerzas[f]*FORCERENDERMULT
            fuerzas2 = list(reversed(self.fuerzas))
            position = self.pos*POSITIONPARTICLEMULT
            for f in range(len(self.fuerzas)):
                if f>0:
                    pygame.draw.line(surface, (255,255,0), cam.ToScreen(position).ToList(), cam.ToScreen(position+(fuerzas2[f]*FORCERENDERMULT)).ToList())
                position+=fuerzas2[f]*FORCERENDERMULT
        # Particle
        pygame.draw.circle(surface, color, cam.ToScreen(self.pos*POSITIONPARTICLEMULT).ToList(), cam.SizeZoom(PARTICLESIZE))
        # Total force
        pygame.draw.line(surface, (255,255,255), cam.ToScreen(self.pos*POSITIONPARTICLEMULT).ToList(), cam.ToScreen(self.pos*POSITIONPARTICLEMULT+(self.fuerza*FORCERENDERMULT)).ToList(), 3)
        #Draw angle
        ppos = cam.ToScreen(self.pos*POSITIONPARTICLEMULT)
        pygame.draw.line(surface, (255,50,255),ppos.ToList(),(ppos+vec2(cam.SizeZoom(ANGLEARCSIZE/2),0)).ToList())
        pygame.draw.arc(surface,(255,50,255),[(ppos+vec2(cam.SizeZoom(ANGLEARCSIZE/-2),cam.SizeZoom(ANGLEARCSIZE/-2))).ToList(),[cam.SizeZoom(ANGLEARCSIZE),cam.SizeZoom(ANGLEARCSIZE)]],0,math.radians(self.angulo),1)
        # Force text
        sizeFont1 = pygame.font.SysFont("arial", round(cam.SizeZoom(fontSize1)), False, False)
        sizeFont2 = pygame.font.SysFont("arial", round(cam.SizeZoom(fontSize2)), False, False)
        text1 = sizeFont2.render(f'{self.fuerza.Length():.3e}' + "N", True, (255,255,255))
        text1.set_alpha(250)
        text2 = sizeFont2.render(str(round(self.angulo,2)) + "°", True, (255,255,255))
        text2.set_alpha(250)
        text3 = sizeFont1.render(str(self.carga), True, (255,255,255))
        text3.set_alpha(240)
        window.surface.blit(text1, cam.ToScreen(self.pos*POSITIONPARTICLEMULT+(self.fuerza*FORCERENDERMULT)).ToList())
        window.surface.blit(text2, (cam.ToScreen(self.pos*POSITIONPARTICLEMULT+(self.fuerza*FORCERENDERMULT))+vec2(0,-cam.SizeZoom(fontSize2))).ToList())
        window.surface.blit(text3, (cam.ToScreen(self.pos*POSITIONPARTICLEMULT-vec2(PARTICLESIZE/2,-PARTICLESIZE))).ToList())

window = Window((800,800), "Coulomb", 60, pygame.HWSURFACE | pygame.SRCALPHA, vsync=1)
cam = Camera(vec2(0,0), 1, window.size)
MoveSpeed = 4

pygame.font.init()
fontSize1 = 15
fontSize2 = 8
arial = pygame.font.SysFont("arial", fontSize1, True , False)

# --PARTICULAS-- #
P1 = Particula(3, vec2(0,1))
P2 = Particula(6, vec2(0.5,0.5))
P3 = Particula(2, vec2(0,0))


Particulas = [P1,P2,P3]





running = True
selection = 0
MousePos = [400,400]
pygame.event.set_grab(True)
positive = True
while running:
    window.surface.fill((0,0,0))
    window.surface.blit(arial.render("WASD para mover la camara | ↑ y ↓ para hacer zoom | numeros 1-9 para crear particulas | 'F' desactiva las fuerzas ", True, (255,255,255)), [0,0])
    window.surface.blit(arial.render("click izquierdo para mover las cargas y click derecho para borrarlas | espacio para invertir la carga | Esc para salir", True, (255,255,255)), [0,20])
    MousePos = pygame.mouse.get_pos()
    pygame.draw.line(window.surface, (100,100,100), cam.ToScreen(vec2(-1000,0)).ToList(), cam.ToScreen(vec2(1000,0)).ToList())
    pygame.draw.line(window.surface, (100,100,100), cam.ToScreen(vec2(0,-1000)).ToList(), cam.ToScreen(vec2(0,1000)).ToList())
    for p in Particulas:
        p.CalculateForce(Particulas)
        p.Render(window.surface, cam)
    if selection != 0:
        selection.CampoElectrico(Particulas,8, 50)
    pygame.display.flip()
    for event in pygame.event.get():
        MousePos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = cam.ToWorldSpace(vec2(MousePos[0],MousePos[1]))/POSITIONPARTICLEMULT
            if event.button == 1:
                
                selection = 0
                for p in Particulas:
                    if mouse.Dist(p.pos)<=PARTICLESIZE/POSITIONPARTICLEMULT:
                        selection = p
                        break
            if event.button == 3:
                for p in Particulas:
                    if mouse.Dist(p.pos)<=PARTICLESIZE/POSITIONPARTICLEMULT:
                        Particulas.remove(p)
                        break
                
        if event.type == pygame.MOUSEBUTTONUP:
            selection = 0
        if pygame.mouse.get_pressed()[0] and selection!=0:
            selection.pos = cam.ToWorldSpace(vec2(MousePos[0],MousePos[1]))/POSITIONPARTICLEMULT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if selection != 0:
                    selection.carga*=-1
                    selection.positivo= not selection.positivo
                else:
                    positive = not positive
            if event.key in [pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                carga = event.key-48
                if not positive:
                    carga*=-1
                Particulas.append(Particula(carga,cam.ToWorldSpace(vec2(MousePos[0],MousePos[1]))/POSITIONPARTICLEMULT))
            if event.key == pygame.K_f:
                RENDERINDIVIDUALFORCES = not RENDERINDIVIDUALFORCES
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_a]:
        cam.pos.x -= MoveSpeed*cam.zoom
    if keys[pygame.K_d]:
        cam.pos.x += MoveSpeed*cam.zoom
    if keys[pygame.K_w]:
        cam.pos.y += MoveSpeed*cam.zoom
    if keys[pygame.K_s]:
        cam.pos.y -= MoveSpeed*cam.zoom
    if keys[pygame.K_UP]:
        cam.zoom*=0.99
    if keys[pygame.K_DOWN]:
        cam.zoom/=0.99

        
    window.Tick()
pygame.display.quit()
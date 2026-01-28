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
RENDERINDIVIDUALFORCES = False
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
                F = (Constante*abs(self.carga)*NanoCoulomb*abs(particle.carga)*NanoCoulomb)/math.pow(self.pos.Dist(particle.pos),2)
                if self.positivo == particle.positivo:
                    Dir = (self.pos-particle.pos).Normalized()
                else:
                    Dir = (particle.pos-self.pos).Normalized()
                FDir+= Dir*F
                self.fuerzas.append(Dir*F)
                #print(Dir, F, Dir*F, self.pos.Dist(particle.pos))
        self.fuerza = FDir
        self.angulo = TrueAngle(FDir.Angle())
    def PrintForce(self):
        print("Fuerza: " + str(self.fuerza.Length()) + " Newtons")
    def PrintAngle(self):
        print("Angulo: " + str(self.angulo) + " Grados")
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
        text1 = arial.render(f'{self.fuerza.Length():.3e}' + "N", True, (255,255,255))
        text1.set_alpha(250)
        text2 = arial.render(str(round(self.angulo,2)) + "°", True, (255,255,255))
        text2.set_alpha(250)
        window.surface.blit(text1, cam.ToScreen(self.pos*POSITIONPARTICLEMULT+(self.fuerza*FORCERENDERMULT)).ToList())
        window.surface.blit(text2, (cam.ToScreen(self.pos*POSITIONPARTICLEMULT+(self.fuerza*FORCERENDERMULT))+vec2(0,-fontSize)).ToList())

window = Window((800,800), "Coulomb", 60, pygame.HWSURFACE | pygame.SRCALPHA, vsync=1)
cam = Camera(vec2(0,0), 1, window.size)
MoveSpeed = 4

pygame.font.init()
fontSize = 15
arial = pygame.font.SysFont("arial", fontSize, False, False)

# --PARTICULAS-- #
P1 = Particula(3, vec2(0,1))
P2 = Particula(2, vec2(0,0))
P3 = Particula(6, vec2(0.5,0.5))
P4 = Particula(-4, vec2(-0.5,0.5))

Particulas = [P1,P2,P3]
for p in Particulas:
    p.CalculateForce(Particulas)
    p.PrintForce()
    p.PrintAngle()

# P1.PrintAngle()
# P2.PrintAngle()
# P3.PrintAngle()

# print(P2.CalculateForce(Particulas))
# print(P3.CalculateForce(Particulas))


running = True
selection = 0
MousePos = [400,400]
pygame.event.set_grab(True)
while running:
    window.surface.fill((0,0,0))
    MousePos = pygame.mouse.get_pos()
    pygame.draw.line(window.surface, (100,100,100), cam.ToScreen(vec2(-1000,0)).ToList(), cam.ToScreen(vec2(1000,0)).ToList())
    pygame.draw.line(window.surface, (100,100,100), cam.ToScreen(vec2(0,-1000)).ToList(), cam.ToScreen(vec2(0,1000)).ToList())
    for p in Particulas:
        p.CalculateForce(Particulas)
        p.Render(window.surface, cam)
    pygame.display.flip()
    for event in pygame.event.get():
        MousePos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = cam.ToWorldSpace(vec2(MousePos[0],MousePos[1]))/POSITIONPARTICLEMULT
            selection = 0
            for p in Particulas:
                if mouse.Dist(p.pos)<=PARTICLESIZE/POSITIONPARTICLEMULT:
                    selection = p
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            selection = 0
        if pygame.mouse.get_pressed()[0] and selection!=0:
            selection.pos = cam.ToWorldSpace(vec2(MousePos[0],MousePos[1]))/POSITIONPARTICLEMULT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if selection != 0:
                    selection.positivo= not selection.positivo
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_a]:
        cam.pos.x -= MoveSpeed
    if keys[pygame.K_d]:
        cam.pos.x += MoveSpeed
    if keys[pygame.K_w]:
        cam.pos.y += MoveSpeed
    if keys[pygame.K_s]:
        cam.pos.y -= MoveSpeed
    if keys[pygame.K_UP]:
        cam.zoom*=0.99
    if keys[pygame.K_DOWN]:
        cam.zoom/=0.99
#     if keys[pygame.K_SPACE]:
#         if selection != 0:
#             selection.positivo= not selection.positivo
        
    window.Tick()
pygame.display.quit()
exit()
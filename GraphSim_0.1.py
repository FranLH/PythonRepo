import pygame
import math


pygame.init()
WindowSize = (400,400)
window = pygame.display.set_mode(WindowSize,pygame.RESIZABLE)
pygame.display.set_caption("Game")

Cam = [0,0,0.2]



class LinearFunc:
    def __init__(self,pend,oo):
        self.pend = 0-pend
        self.oo = oo
    def y(self,x):
        return(x*self.pend + self.oo)
class QuadFunc:
    def __init__(self,quad,oo):
        self.quad = quad
        self.oo = oo
    def y(self,x):
        return(math.pow(x, self.quad) + self.oo)

f1 = LinearFunc(2,10)
f2 = LinearFunc(0,50)
f3 = LinearFunc(0,100)
f4 = QuadFunc(2,-50)
Graphs = [f1,f2,f3,f4]

def Render(funcs):
    pygame.draw.line(window, (255,0,0), (201,201),(200,200))
    global Cam
    w = pygame.display.get_surface().get_width()
    h = pygame.display.get_surface().get_height()
    for func in funcs:
        lastpos = 0
        for x in range(round(0-w/2),round(w/2)):
            pos = (x+w/2, Cam[2]*(func.y(x/Cam[2]+Cam[0])+Cam[1])+h/2)
            try:
                pygame.draw.line(window, (0,0,0), (pos),(lastpos))
            except:
                pass
            lastpos = pos
            
            





CamSpeed = 1
running = True
while running:
    window.fill((255, 255, 255))
    Render(Graphs)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        Cam[1] += CamSpeed
    if keys[pygame.K_RIGHT]:
        Cam[0] += CamSpeed    
    if keys[pygame.K_LEFT]:
        Cam[0] -= CamSpeed
    if keys[pygame.K_DOWN]:
        Cam[1] -= CamSpeed
    if keys[pygame.K_w]:
        Cam[2] *= 1.001
    if keys[pygame.K_s]:
        Cam[2] /= 1.001        
pygame.display.quit()
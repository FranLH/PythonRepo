import pygame
import math


pygame.init()
WindowSize = (800,800)
window = pygame.display.set_mode(WindowSize,pygame.RESIZABLE)
pygame.display.set_caption("Game")

Cam = [0,0,4]



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
    global Cam
    w = pygame.display.get_surface().get_width()
    h = pygame.display.get_surface().get_height()
    for func in funcs:
        lastpos = 0
        for x in range(round(w/Cam[2])):
            pos = (round(Cam[2]*(x-w/2))+w/2, round(Cam[2]*func.y((x-w/2)+Cam[0])+Cam[1]))
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
        Cam[1] += CamSpeed/Cam[2]
    if keys[pygame.K_RIGHT]:
        Cam[0] += CamSpeed/Cam[2]     
    if keys[pygame.K_LEFT]:
        Cam[0] -= CamSpeed/Cam[2]
    if keys[pygame.K_DOWN]:
        Cam[1] -= CamSpeed/Cam[2]
    if keys[pygame.K_w]:
        Cam[2] += 0.01
    if keys[pygame.K_s]:
        Cam[2] -= 0.01        
pygame.display.quit()
import pygame
import math
import copy

running = True

pygame.init()
WindowSize = 500
window = pygame.display.set_mode((WindowSize, WindowSize), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("")

cam = [0,0,0]
Drawing = []

Drawing = pygame.Surface((WindowSize, WindowSize), pygame.SRCALPHA, 32)
Drawing.fill((0,0,0,0))
Axles = pygame.Surface((WindowSize, WindowSize), pygame.SRCALPHA, 32)
class axle:
    def __init__(self,pos,startPos,rotation,angle,length,ID):
        self.pos = pos
        self.startPos = startPos
        self.rotation = rotation
        self.angle = angle
        self.length = length
        self.ID = ID
    def calcNewPos(self):
        if self.ID != 0:
            self.startPos = Objects[self.ID-1].pos
        self.angle = self.angle + self.rotation
        self.pos = [self.startPos[0]+math.cos(math.radians(self.angle))*self.length,self.startPos[1]+math.sin(math.radians(self.angle))*self.length]
        scalePos = (self.pos[0]+WindowSize/2, self.pos[1]+WindowSize/2)
        if self.ID == len(Objects)-1:
            pygame.draw.line(Drawing, (255,255,255,255), scalePos, scalePos, 1)
            #if scalePos not in Drawing:
            #   Drawing.append(scalePos)
ax0 = axle([0,0],[0,0], 0.01 ,180,100,0)
ax = axle([0,0],[0,0], 0.2,180,50,1)
ax1 = axle([0,0],[0,0],-1,90,10,2)
ax2 = axle([0,0],[0,0],0,90,100,3)
ax3 = axle([0,0],[0,0],-0.7,180,10,4)
Objects = [ax0, ax, ax1, ax2]


def Render():
    window.fill((0, 0, 0))
    Axles.fill((0,0,0,0))
    for axl in Objects:
        pygame.draw.line(Axles, (255,0,0,255), (axl.startPos[0]+WindowSize/2,axl.startPos[1]+WindowSize/2), (axl.pos[0]+WindowSize/2, axl.pos[1]+WindowSize/2), 3)
    window.blits(((Drawing, (0,0)), (Axles, (0,0))))
    #for pixel in Drawing:
    #    pygame.draw.line(window, (255,255,255), pixel, pixel, 1)

#for i in Objects:
#    atts = vars(i)
#    print(atts)
its = 0
while running == True:
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        cam[0] -= MoveSpeed
    if keys[pygame.K_RIGHT]:
        cam[0] += MoveSpeed
    if keys[pygame.K_UP]:
        cam[1] -= MoveSpeed
    if keys[pygame.K_DOWN]:
        cam[1] += MoveSpeed
    if keys[pygame.K_s]:
        cam[2] *= 0.999
    if keys[pygame.K_w]:
        cam[2] /= 0.999

    

    for obj in Objects:
        obj.calcNewPos()
    its += 1
    Render()
    pygame.display.flip()








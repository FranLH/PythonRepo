import pygame, time
import math
import random


pygame.init()
pygame.font.init()
arial = pygame.font.SysFont("arial", 10, False, False)
WindowW = 800
WindowH = 500
SpaceWidth = 800
SpaceHeight = 500
FPSCap = 1000
dt = 0
MINdist = 10
MAXvel = 50
Pushback = 0.5
window = pygame.display.set_mode((WindowW, WindowH), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()

objects = []
class Body:
    def __init__(self, pos, vel, mass):
        self.pos = pos
        self.vel = vel
        self.acc = [0,0]
        self.mass = mass
    def CalculateAcceleration(self,objects):
        acceleration = 0
        self.acc = [0,0]
        for obj in objects:
            if obj != self:
                angle = math.atan2(obj.pos[0]-self.pos[0],obj.pos[1]-self.pos[1])
                distance = math.dist(obj.pos,self.pos)
                acceleration = (obj.mass*self.mass)/(max(distance,MINdist)*max(distance,MINdist))
                if distance<MINdist:
                    self.acc[0]-=(MINdist/distance)*Pushback*math.sin(angle)
                    self.acc[1]-=(MINdist/distance)*Pushback*math.cos(angle)                    
                self.acc[0]+=acceleration*math.sin(angle)
                self.acc[1]+=acceleration*math.cos(angle)

            else:
                continue
def NewObj():
    pos = [random.randint(0,800),random.randint(0,500)]
    angle = math.radians(random.random()*180)
    vel = [math.cos(angle),math.sin(angle)]
    objects.append(Body(pos,vel,random.randint(0,20)))    
for i in range(100):
    NewObj()
    
# objects.append(Body([420,260],[0,0],200))
# objects.append(Body([380,200],[3,0],40))

def Render():
    
    window.fill((0,0,0))
    for obj in objects:
        pygame.draw.line(window, (100,100,100), (20,20),(FPS*2,20))        
        pygame.draw.line(window, (100,100,100), (obj.pos[0]/SpaceWidth*WindowW,obj.pos[1]/SpaceHeight*WindowH), ((obj.pos[0]+obj.vel[0])/SpaceWidth*WindowW, (obj.pos[1]+obj.vel[1])/SpaceHeight*WindowH))
        pygame.draw.line(window, (0,100,0), (obj.pos[0]/SpaceWidth*WindowW,obj.pos[1]/SpaceHeight*WindowH), ((obj.pos[0]+obj.acc[0])/SpaceWidth*WindowW, (obj.pos[1]+obj.acc[1])/SpaceHeight*WindowH))
        pygame.draw.circle(window, (random.randint(0,100),random.randint(0,255),random.randint(150,255)), (obj.pos[0]/SpaceWidth*WindowW, obj.pos[1]/SpaceHeight*WindowH), round(math.sqrt(obj.mass)))
    text = arial.render("FPS: " + str(round(FPS,2)), True, (255,0,0), (0,0,0))
    text2 = arial.render("Objects: " + str(len(objects)), True, (255,0,0), (0,0,0))
    window.blits([(text,(0,0)),(text2, (0,10))])
    pygame.display.flip()

def Tick():
    for obj in objects:
       obj.CalculateAcceleration(objects)
    for obj in objects:
        obj.vel[0]+=obj.acc[0]*dt
        obj.vel[1]+=obj.acc[1]*dt
        obj.vel = [min(obj.vel[0],MAXvel),min(obj.vel[1],MAXvel)]
        obj.pos[0]+=obj.vel[0]*dt
        obj.pos[1]+=obj.vel[1]*dt
        if obj.pos[0]>SpaceWidth:
            obj.pos[0]=obj.pos[0]-SpaceWidth
        if obj.pos[0]<0:
            obj.pos[0]=SpaceWidth+obj.pos[0]
        if obj.pos[1]>SpaceHeight:
            obj.pos[1]=obj.pos[1]-SpaceHeight
        if obj.pos[1]<0:
            obj.pos[1]=SpaceHeight+obj.pos[1]
def Step():
    Tick()
    Render()
   
running = True
its = 1
FPS = 200

while running:
    dt = clock.tick(FPSCap)/100
    FPS = clock.get_fps()
    Step()
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False
    its+=1
pygame.display.quit()
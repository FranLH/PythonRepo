import pygame
import math
import copy
import numpy as np

pygame.init()
WindowSize = (600,600)
window = pygame.display.set_mode(WindowSize)
pygame.display.set_caption("Game")

res = 0.5
WallHeight = 200
heightMult = 20
Width = 600
CamDist = 1

def Hipotenuse(vec):
    return(math.sqrt(vec[0]*vec[0]+vec[1]*vec[1]))
def Normal(vec):
    hipotenuse = math.sqrt(vec[0]*vec[0]+vec[1]*vec[1])
    return([vec[0]/hipotenuse,vec[1]/hipotenuse])
def LimitRotation(angle):
    if angle > 360:
        return(LimitRotation(angle-360))
    elif angle < 0:
        return(LimitRotation(angle+360))
    else:
        return(angle)

class RectWall:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color
    def Collision(self, point):
        return self.vertices[1][0] > point[0] > self.vertices[0][0] and self.vertices[1][1] > point[1] > self.vertices[0][1]
#    def Dist(self, point):
#        vertDist = []
#        vertDist.append((math.dist(self.vertices[0],point),self.vertices[0]),(math.dist(self.vertices[1],point),self.vertices[1]),(math.dist([self.vertices[0][0],self.vertices[1][1]],point),[self.vertices[0][0],self.vertices[1][1]]),(math.dist([self.vertices[1][0],self.vertices[0][1]],point),[self.vertices[1][0],self.vertices[0][1]]))
#        vertDist.sort()
#        r = vertDist[0][1]
#        s = vertDist[1][1]
#        Pend = (s[1]-r[1])/(s[0]-r[0])
#        Oo = s[1] - Pend*s[0]
class CircleWall:
    def __init__(self, pos, Radius, color):
        self.pos = pos
        self.Radius = Radius
        self.color = color
    def Collision(self, point):
        return math.dist(self.pos, point) < self.Radius
    
def Ray(Start,Dir,RendDist, detail, StepDist):
    iterations = 0
    pos = copy.deepcopy(Start)
    NormDir = Normal(Dir)
    NormDir[0] *= StepDist
    NormDir[1] *= StepDist
    StepLength = Hipotenuse(NormDir)
    while iterations*StepLength<RendDist:
        pos[0] += NormDir[0]
        pos[1] += NormDir[1]
        for obj in Level:
            if obj.Collision(pos):
                #print("collided")
                #print(math.dist(Start,pos))
                while obj.Collision(pos):
                    pos[0] -=NormDir[0]*detail
                    pos[1] -= NormDir[1]*detail
                pos[0] +=  NormDir[0]*detail
                pos[1] +=  NormDir[1]*detail
                return(obj.color,iterations*StepLength,[Dir[0]/StepDist,Dir[1]/StepDist])
        iterations+=1
    return((0,0,0),iterations*StepLength,Dir)

def Render(pixels):
    window.fill((0, 0, 0))
    definition = WindowSize[0]/len(pixels)
    for x in range(len(pixels)):
        try:
            height = (WallHeight/pixels[x][1])*Hipotenuse(pixels[x][2])
        except:
            height = WindowSize[0]
        height = height*heightMult
        pygame.draw.line(window, pixels[x][0], (x*definition,WindowSize[1]/2-height/2), (x*definition,WindowSize[1]/2+height/2), 1)
    
class Player:
    def __init__(self, pos, orientation, fov, RenderDist, detail, StepDist):
        self.pos = pos
        self.orientation = orientation
        self.fov = fov
        self.RenderDist = RenderDist
        self.StepDist = StepDist
        self.detail = detail
    def Raycast(self):
        results = []
        A = CamDist * np.array([self.StepDist*math.cos(math.radians(self.orientation-self.fov/2)),self.StepDist*math.sin(math.radians(self.orientation-self.fov/2))])
        B = CamDist * np.array([self.StepDist*math.cos(math.radians(self.orientation+self.fov/2)),self.StepDist*math.sin(math.radians(self.orientation+self.fov/2))])
        for pixel in range(int(Width*res)):
        #for pixel in range(round(self.orientation-(self.fov*res)/2), round(self.orientation+(self.fov*res)/2)):
            direction = A + ((B-A)/Width/res)*pixel
            results.append(Ray(copy.deepcopy(self.pos), direction, self.RenderDist, self.detail, self.StepDist))
        Render(results)
r1 = RectWall([[20,-100],[40,150]], (255,255,255))
r2 = RectWall([[-100,100],[20,150]], (255,0,0))
c1 = CircleWall([-50,-50],30, (0,255,0))
Level = [c1,r2,r1]
player = Player([0,0],90,90,200,0.1,1)





running = True
PlayerSpeed = 1
PlayerDirVec = [0,0]
while running:
    iterations = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pass

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.orientation -= 0.5
        PlayerDirVec = Normal([math.cos(math.radians(player.orientation)),math.sin(math.radians(player.orientation))]) * PlayerSpeed
    if keys[pygame.K_d]:
        player.orientation += 0.5
        PlayerDirVec = Normal([math.cos(math.radians(player.orientation)),math.sin(math.radians(player.orientation))]) * PlayerSpeed
    player.orientation = LimitRotation(player.orientation)
    if keys[pygame.K_UP]:
        player.pos[0] += PlayerDirVec[0]
        player.pos[1] += PlayerDirVec[1]
        print(math.dist(player.pos,c1.pos))
    if keys[pygame.K_RIGHT]:
        CamDist+=0.5
        
    if keys[pygame.K_LEFT]:
        CamDist-=0.5
    if pygame.mouse.get_pressed()[0] == True:
        pass
    if pygame.mouse.get_pressed()[2] == True:
        pass
    if iterations % 5 == 0:
        
        player.Raycast()
        pygame.display.flip()     
    iterations += 1
pygame.display.quit()
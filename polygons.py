#polygons


import pygame
import math
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2

class Circle:
    def __init__(self,pos:vec2, radius:float, color):
        self.pos, self.radius, self.color = pos, radius, color
    def GetPoint(self, n:float):
        value = 2*n*math.pi
        return ( self.pos + vec2(self.radius*math.cos(value), self.radius*math.sin(value)) ) # Any point in the circle
    def Render(self, points):
        segmentSize = 1/points
        for i in range(points):
            n = segmentSize*i
            pygame.draw.circle(window.surface, self.color, cam.ToScreen(self.GetPoint(n)).ToList(), 1)
class Polygon:
        def __init__(self,pos:vec2, edges:int, radius:float, color, rotation:float=0):
            self.pos, self.radius, self.edges, self.rotation, self.color = pos, radius, edges, rotation, color
        def GetPoint(self, n:float):
            i = math.floor(self.edges * n) % self.edges
            u = n * self.edges - math.floor(n * self.edges)
            
            angleX = self.rotation + 2*math.pi*i/self.edges
            angleY = self.rotation + 2*math.pi*(i+1)/self.edges
            
            return(self.pos + vec2(math.cos(angleX)*(1-u) + math.cos(angleY)*u, math.sin(angleX)*(1-u) + math.sin(angleY)*u) * self.radius)
        def Render(self, points):
            segmentSize = 1/points
            for i in range(points):
                n = segmentSize*i
                pygame.draw.circle(window.surface, self.color, cam.ToScreen(self.GetPoint(n)).ToList(), 1)
                
def RenderSum(polygons, points, color, sizeMult):
    segmentSize = 1/points
    for i in range(points):
        n = segmentSize*i
        point = cam.ToScreen(sum(list(map(lambda a:a.GetPoint(n), polygons)),vec2(0,0))*sizeMult).ToList()
        pygame.draw.circle(window.surface, color, point, 1)
def RenderMult(polygons, points, color, sizeMult):
    segmentSize = 1/points
    for i in range(points):
        n = segmentSize*i
        points = list(map(lambda a:complex(a.GetPoint(n)), polygons))
        point = 1+0j
        for p in points:
            point*=p
        point=vec2(point.real, point.imag)
        pygame.draw.circle(window.surface, color, cam.ToScreen(point*sizeMult).ToList(), 2)
            
C = Polygon(vec2(0,0), 7, 40, (0,255,0))
S = Polygon(vec2(0,0), 3, 40, (0,255,0))
T = Polygon(vec2(0,0), 3, 40, (0,255,0))
D = Circle(vec2(0,0), 40, (0,255,0))
polygons = [C,S]



window = Window((800,800), "Polygons", 60, pygame.HWSURFACE, vsync=1)
cam = Camera(vec2(0,0), 1, window.size)
MoveSpeed = 4


DEFINITION = 1200
running = True
its=0
while running:
    #S.rotation-=0.02
    its = its+1/600 if its<1 else 0
    window.surface.fill((0,0,0))
    for polygon in polygons:
        polygon.Render(DEFINITION)
    RenderMult([C,C,C,S], DEFINITION, (0,0,255), 0.00015)
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
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
        
    window.Tick()
pygame.display.quit()
exit()
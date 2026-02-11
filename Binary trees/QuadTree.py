# Quad tree
import pygame
import sys
import math
import random
sys.path.append("/Users/Francisco/Desktop/Coding/PythonRepo/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2

objects = []

def sortFunction(particle):
    return([particle.pos.x, particle.pos.y])

class Particle:
    def __init__(self, pos:vec2):
        self.pos = pos
    def Render(self):
        pygame.draw.circle(window.surface, (0,0,255), cam.ToScreen(self.pos).ToList(), 1)
    def ConsoleLog(self, ind):
        print("  "*ind + "  >" + "PARTICLE")
    

class QuadTree:
    def __init__(self, pos:vec2, size, minSize, sortFunct):
        self.pos, self.size, self.minSize, self.sortFunct = pos, size, minSize, sortFunct
        self.data = []
    def ConsoleLog(self, ind):
        indent = int(8-math.log(self.size, self.minSize))
        print("  "*indent +"\quadTree:")
        for element in self.data:
            element.ConsoleLog(indent)
    def Subdivide(self):
        if self.size > self.minSize and len(self.data) > 4:
            newSize = self.size/2
            newTrees = [
            QuadTree(self.pos, newSize, self.minSize, self.sortFunct),
            QuadTree(self.pos+vec2(newSize, 0), self.size/2, self.minSize, self.sortFunct),
            QuadTree(self.pos+vec2(0, newSize), self.size/2, self.minSize, self.sortFunct),
            QuadTree(self.pos+vec2(newSize, newSize), self.size/2, self.minSize, self.sortFunct)]
            for element in self.data:
                value = self.sortFunct(element)
                if value[0] < self.pos.x+newSize:
                    if value[1] < self.pos.y+newSize:
                        newTrees[0].data.append(element)
                    else:
                        newTrees[2].data.append(element)
                else:
                    if value[1] < self.pos.y+newSize:
                        newTrees[1].data.append(element)
                    else:
                        newTrees[3].data.append(element)
            self.data=newTrees
            for tree in self.data:
                tree.Subdivide()
                        
            
    def Render(self):
        pygame.draw.rect(window.surface, (255,0,0), [cam.ToScreen(self.pos+vec2(0,self.size)).ToList(), [round(cam.SizeZoom(self.size)), round(cam.SizeZoom(self.size))]], 1)
        for element in self.data:
            if element != None:
                element.Render()
        
window = Window((600,600), "quadTree", 60, pygame.HWSURFACE, vsync=1)
cam = Camera(vec2(128,128), 1, window.size)
cam.zoom = 0.5

particles = QuadTree(vec2(0,0), 1024, 2, sortFunction)
for i in range(400):
    particles.data.append(Particle(vec2(random.randint(0,1024), random.randint(0,1024))))
#particles.data.extend([Particle(vec2(20, 38)), Particle(vec2(200, 180)), Particle(vec2(220, 30)), Particle(vec2(60, 190)), Particle(vec2(120, 90))])

particles.Subdivide()
#particles.ConsoleLog(0)

running = True
MousePos = [400,400]
MoveSpeed = 1
ZoomSpeed = 1.01
#pygame.event.set_grab(True)
while running:
    window.surface.fill((255,255,255))
    particles.Render()
    MousePos = pygame.mouse.get_pos()

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
    if keys[pygame.K_UP]:
        cam.zoom /= ZoomSpeed
    if keys[pygame.K_DOWN]:
        cam.zoom *= ZoomSpeed
        
    window.Tick()
pygame.display.quit()
exit()
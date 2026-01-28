import pygame
import math
import copy
import random
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2



class Triangle:
    def __init__(self, Ypoint, color, height, IsInverted, HasDivided):
        self.Ypoint, self.color, self.height, self.IsInverted, self.HasDivided = Ypoint, color, height, IsInverted, HasDivided
        self.sideLength = self.height/math.sin(math.radians(60))
        if not self.IsInverted:
            self.left = self.Ypoint - vec2(self.sideLength/2,self.height)
            self.right = self.Ypoint - vec2(self.sideLength/-2,self.height)
        else:
            self.left = self.Ypoint + vec2(self.sideLength/-2,self.height)
            self.right = self.Ypoint + vec2(self.sideLength/2,self.height)
            
    def Render(self, surface, camera):
        if camera.IsInScreen(self.Ypoint) or camera.IsInScreen(self.left) or camera.IsInScreen(self.right):
            pygame.draw.polygon(surface, self.color, [camera.ToScreen(self.Ypoint).ToList(),camera.ToScreen(self.left).ToList(),camera.ToScreen(self.right).ToList()], 1)
    def Divide(self, List:list["Triangle"]):
        if self.IsInverted:
            NewTop = Triangle(self.Ypoint+vec2(0,self.height),self.color,self.height/2, True, False)
            NewLeft = Triangle(self.left-vec2(0,self.height),self.color,self.height/2, True, False)
            NewRight = Triangle(self.right-vec2(0,self.height),self.color,self.height/2, True, False)
            return([NewTop, NewLeft, NewRight])
        else:
            return([Triangle(vec2(self.Ypoint.x,self.Ypoint.y-self.height), self.color, self.height/2, True, False)])

T = Triangle(vec2(0,300), (255,255,255), 500, False, False)
TrianglesList = [T]
for i in range(4):
    newList = []
    for triangle in TrianglesList:
        if not triangle.HasDivided:
            newList.extend(triangle.Divide(TrianglesList))
    TrianglesList.extend(newList)
print(len(TrianglesList))

window = Window((600,600), "Sierpinsky", 60, pygame.HWSURFACE, vsync=1)
cam = Camera(vec2(100,0), 1, window.size)
MoveSpeed = 4


running = True
MousePos = [300,300]
pygame.event.set_grab(True)
while running:
    window.surface.fill((0,0,0))
    for triangle in TrianglesList:
        triangle.Render(window.surface, cam)
    #cam.zoom-=0.01
    pygame.display.flip()
    MousePos = pygame.mouse.get_pos()

    
    for event in pygame.event.get():
        MousePos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
        
    window.Tick()
pygame.display.quit()
exit()

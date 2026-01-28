import pygame
import math
import copy
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2



class Triangle:
    def __init__(self, top, color, height):
        self.top, self.color, self.height = top, color, height
        self.sideLength = self.height/math.sin(math.radians(60))
        self.left = self.top - vec2(self.sideLength/2,self.height)
        self.right = self.top - vec2(self.sideLength/-2,self.height)
        
    def Render(self, surface, camera):
        if camera.IsInScreen(self.top) or camera.IsInScreen(self.left) or camera.IsInScreen(self.right):
            pygame.draw.polygon(surface, self.color, [camera.ToScreen(self.top).ToList(),camera.ToScreen(self.left).ToList(),camera.ToScreen(self.right).ToList()], 0)
    def Divide(self, List:list["Triangle"]):
        NewTop = Triangle(self.top,self.color,self.height/2)
        NewLeft = Triangle(NewTop.left,self.color,self.height/2)
        NewRight = Triangle(NewTop.right,self.color,self.height/2)
        return([NewTop, NewLeft, NewRight])

T = Triangle(vec2(0,300), (255,255,255), 500)
TrianglesList = [T]
for i in range(4):
    newList = []
    for triangle in TrianglesList:
        newList.extend(triangle.Divide(TrianglesList))
    TrianglesList = newList
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

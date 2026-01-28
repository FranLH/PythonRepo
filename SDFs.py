import pygame
import math
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2
#SDFs



class Rect:
    def __init__(self, pos:vec2, size:vec2):
        self.pos = pos
        self.size = size
    def SD(self, p:vec2):
        d = abs(p-self.pos) -self.size
        return (vec2(max(d.x,0), max(d.y,0)).Length() + min(max(d.x, d.y), 0))
        #return max(abs(p) - self.size, ZERO).Length()
class Circ:
    def __init__(self, pos:vec2, radius:float):
        self.pos = pos
        self.radius = radius
    def SD(self, p:vec2):
        return (p-self.pos).Length()-self.radius

window = Window([400,400], "SDFs", 1, pygame.HWSURFACE | pygame.SRCALPHA, 1)
camera = Camera(vec2(0,0), 1, window.size)

R = Rect(vec2(40,40), vec2(80,80))
C = Circ(vec2(-50,-80), 100)
objects = [R, C]


running = True
while running:
    window.surface.fill((0,0,0))
    #Render pass
    regionSize = 6
    for x in range(0, window.size[0], regionSize):
        for y in range(0, window.size[1], regionSize):
            p = camera.ToWorldSpace(vec2(x,y))
            d = objects[0].SD(p)
            for obj in objects[1:]:
                d = min(d, obj.SD(p))
                #d = min(-d, obj.SD(p))
            color = (255,255,255)
            if d <= 10 and d >= -8:
                color = (0,0,0)
            pygame.draw.line(window.surface, color, camera.ToScreen(p).ToList(), camera.ToScreen(p).ToList())
    #pygame.draw.rect(window.surface, (255,0,0), [camera.ToScreen(vec2(-100,100)).ToList(), [200,200]], 2)
    pygame.display.flip()
    print("rendered")
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

        
    window.Tick()
pygame.display.quit()
import pygame
import math
import copy
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2


class SpriteRenderer:
    def __init__(self, pos:vec2, sprite:str, size=None, color=None):
        self.pos, self.sprite, self.size, self.color = pos, sprite, size, color
    def Render(self, surface, camera):
        match self.sprite:
            case "rectangle":
                pygame.draw.rect(surface, self.color, [camera.ToScreen(self.pos).ToList(),camera.SizeZoom(self.size).ToList()])

window = Window((600,600), "Zoom", 60, pygame.HWSURFACE, vsync=1)
cam = Camera(vec2(20,-20), 1, window.size)
MoveSpeed = 4

S = SpriteRenderer(vec2(0,0), "rectangle", vec2(40,40), (255,255,255))

running = True
MousePos = [300,300]
pygame.event.set_grab(True)
while running:
    window.surface.fill((0,0,0))
    S.Render(window.surface, cam)
    cam.zoom-=0.01
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

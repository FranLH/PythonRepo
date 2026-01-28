import pygame
import math
import copy
import random
import sys
sys.path.append("/Users/Francisco/Desktop/Coding/Python/MyClasses")
from camera import Camera
from win_display import Window
from vector2 import vec2


class Layer:
    def __init__(self, size, zPos):
        self.size, self.zPos = size, zPos
        self.surface = pygame.Surface(size.ToList(), pygame.SRCALPHA)
class Canvas:
    def __init__(self, size:vec2, layers=[]):
        self.size, self.layers = size, layers
        self.SelectedLayer = 0
        self.SelectedTool = 0
        self.BrushSize = 5
        self.SelectedColor = (255,0,0, 10)
        self.DrawingSurf = pygame.Surface(size.ToList(), pygame.SRCALPHA)
        self.LastMousePos = None
        if layers == []:
            self.layers = [Layer(size, 0)]
        self.SortLayers()
    def Render(self, surface, pos:vec2, camera):
        surfaces = []
        for layer in self.layers:
            surfaces.append([pygame.transform.flip(layer.surface, False, True), cam.ToScreen(pos).ToList()]) # Flips the surfaces on the Y axis
        surface.blits(surfaces)
    def SortLayers(self):
        self.layers.sort(key=lambda a : a.zPos)
    def DrawLine(self,startPos:vec2, endPos:vec2, color, width=1):
        pygame.draw.line(self.layers[self.SelectedLayer].surface, color, startPos.ToList(), endPos.ToList(), width)
    def DrawRect(self,startPos:vec2, endPos:vec2, color, width=0):
        pygame.draw.rect(self.layers[self.SelectedLayer].surface, color, [vec2(min(startPos.x, endPos.x), min(startPos.y, endPos.y)).ToList(), abs(startPos-endPos).ToList()], width)
    def DrawCircle(self, centerPos:vec2, radius, color, width=0):
        pygame.draw.circle(self.layers[self.SelectedLayer].surface, color, centerPos.ToList(), radius, width)
    def MouseHeld(self, mousePos):
        MOUSEPOS = cam.ToWorldSpace(vec2(mousePos[0], mousePos[1])) + vec2(0,self.size.y)
        match self.SelectedTool:
            case 0:
                self.DrawCircle(MOUSEPOS, self.BrushSize, self.SelectedColor)
                if str(type(self.LastMousePos)) != "<class 'NoneType'>":
                    self.DrawCircle(self.LastMousePos, self.BrushSize, self.SelectedColor)
                    self.DrawLine(self.LastMousePos, MOUSEPOS, self.SelectedColor, self.BrushSize*2)
                self.LastMousePos = MOUSEPOS

                                
                #self.DrawLine(MOUSEPOS,MOUSEPOS, self.SelectedColor, 1)
    def MouseDown(self, mousePos):
        MOUSEPOS = cam.ToWorldSpace(vec2(mousePos[0], mousePos[1])) + vec2(0,self.size.y)
        self.LastMousePos = MOUSEPOS
        match self.SelectedTool:
            case 0:
                #self.DrawCircle(MOUSEPOS, self.BrushSize, self.SelectedColor)
                pass
    def MouseUp(self, mousePos):
        MOUSEPOS = cam.ToWorldSpace(vec2(mousePos[0], mousePos[1])) + vec2(0,self.size.y)
        match self.SelectedTool:
            case 0:
                #self.DrawCircle(MOUSEPOS, self.BrushSize, self.SelectedColor)
                self.LastMousePos = None
window = Window((600,600), "Paint engine", 60, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.RESIZABLE, vsync=1)


# L1 = Layer(vec2(600,600), 1)
# L2 = Layer(vec2(600,600), 0)
canvas = Canvas(vec2(600,600), [])
cam = Camera(vec2(0+canvas.size.x/2,canvas.size.y/-2), 1, window.size)
MoveSpeed = 4

canvas.DrawLine(vec2(0,0),vec2(200,200), (255,0,0,200))
canvas.DrawRect(vec2(300,200), vec2(10,400), (0,255,0,200), 5)
canvas.DrawCircle(vec2(400,400), 40, (0,0,255,200), 0)


# pygame.draw.line(L1.surface, (255,255,255, 255), [30,30], [200, 200], 80)
# pygame.draw.line(L2.surface, (255,0,0), [30,30], [250, 200], 80)
running = True
MousePos = [300,300]
while running:
    window.surface.fill((255,255,255))
    canvas.Render(window.surface, vec2(0,0), cam)
    pygame.display.flip()
    MousePos = pygame.mouse.get_pos()

    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            canvas.MouseDown(MousePos)
        if event.type == pygame.MOUSEBUTTONUP:
            canvas.MouseUp(MousePos)
        if pygame.mouse.get_pressed(3)[0]:
#             MousePos = pygame.mouse.get_pos()
            canvas.MouseHeld(MousePos)
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

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
import pygame, time
import math


WindowW = 800
WindowH = 500

window = pygame.display.set_mode((WindowW, WindowH), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("GameBusTemplate.py")
clock = pygame.time.Clock()

class NewGameBus:
    def __init__(self, MaxFrameTime):
        self.Bus = []
        self.Clock = pygame.time.Clock()
        self.MaxFrameTime = MaxFrameTime
        self.FrameTime = 0
    def Step(self):
        if len(self.Bus) != 0:
            exec(self.Bus[0])
            self.Bus.pop(0)
        
    def Frame(self):
        self.FrameTime = 0
        self.Clock.tick()
        while self.FrameTime < self.MaxFrameTime:
            self.Step()
            self.FrameTime += self.Clock.tick()


     
running = True
FPSCap = 60
FPS = 0
dt = 0
GameBus = NewGameBus(1000/FPSCap)
while running:
    dt = clock.tick(FPSCap)
    FPS = clock.get_fps()
    GameBus.Frame()
    for event in pygame.event.get():
        

        if event.type == pygame.QUIT:
            running = False

pygame.display.quit()